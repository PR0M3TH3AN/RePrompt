```python
import streamlit as st
from pathlib import Path
import subprocess
import yaml
from generate_repo_context import main as generate_context_main
import shutil
import os
import tempfile

# Configuration
CONFIG_FILE = "config.yaml"
OUTPUT_FILE = "repo-context.txt"
STATIC_FILES_DIR = Path(__file__).parent / "static_files"
GLOBAL_FILES_DIR = Path(__file__).parent / "global_files"
REPOS_DIR = Path(__file__).parent / "repositories"

# Ensure necessary directories exist
REPOS_DIR.mkdir(exist_ok=True)
GLOBAL_FILES_DIR.mkdir(exist_ok=True)
STATIC_FILES_DIR.mkdir(exist_ok=True)

# Load configuration
def load_config():
    config_path = Path(__file__).parent / CONFIG_FILE
    if not config_path.exists():
        st.error(f"Configuration file {CONFIG_FILE} not found.")
        st.stop()
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        st.error(f"Error parsing configuration file: {e}")
        st.stop()

config = load_config()
exclude_dirs = config.get("exclude_dirs", [])
important_files = config.get("important_files", [])
custom_sections = config.get("custom_sections", [])

# Streamlit App
st.title("Repository Context Generator")

st.sidebar.header("Clone Repository")
repo_url = st.sidebar.text_input("Repository URL", "")
repo_name = st.sidebar.text_input("Repository Name", "")
if st.sidebar.button("Clone Repository"):
    if repo_url and repo_name:
        repo_path = REPOS_DIR / repo_name
        if repo_path.exists():
            st.sidebar.warning("Repository already cloned.")
        else:
            try:
                subprocess.run(['git', 'clone', repo_url, str(repo_path)], check=True)
                st.sidebar.success("Repository cloned successfully.")
            except subprocess.CalledProcessError as e:
                st.sidebar.error(f"Error cloning repository: {e}")
    else:
        st.sidebar.error("Please provide both Repository URL and Name.")

st.header("Select Repository")
available_repos = [d.name for d in REPOS_DIR.iterdir() if d.is_dir()]
selected_repo = st.selectbox("Choose a repository", available_repos)

if selected_repo:
    repo_path = REPOS_DIR / selected_repo

    st.subheader("File Filtering")
    # Retrieve all files in the repository
    file_list = []
    for root, dirs, files in os.walk(repo_path):
        rel_root = Path(root).relative_to(repo_path)
        for d in dirs:
            file_list.append(str(rel_root / d) + "/")
        for f in files:
            file_list.append(str(rel_root / f))

    # File inclusion and exclusion
    include_prompt = st.multiselect("Include in Prompt", options=file_list)
    exclude_prompt = st.multiselect("Exclude from Prompt", options=file_list)
    include_tree = st.multiselect("Include in Directory Tree", options=file_list)
    exclude_tree = st.multiselect("Exclude from Directory Tree", options=file_list)

    st.subheader("Global Files")
    st.write("Files in the `global_files/` directory are included in every context.")

    # Display current global files
    global_files = [f.name for f in GLOBAL_FILES_DIR.iterdir() if f.is_file()]
    st.write("### Current Global Files:")
    for gf in global_files:
        st.write(f"- {gf}")

    # Upload new global files
    uploaded_file = st.file_uploader("Add Global File", type=["txt", "xml", "md"])
    if uploaded_file:
        save_path = GLOBAL_FILES_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Global file `{uploaded_file.name}` added.")

    # Generate Context File
    if st.button("Generate Context File"):
        try:
            # Create a temporary directory to store the output
            with tempfile.TemporaryDirectory() as tmpdirname:
                temp_output = Path(tmpdirname) / OUTPUT_FILE

                # Prepare parameters
                generate_context_main(
                    config_path=Path(__file__).parent / CONFIG_FILE,
                    source_dir=config.get("source_directory", "src"),
                    start_path=repo_path,
                    exclude_dirs=exclude_dirs,
                    important_files=important_files,
                    custom_sections=custom_sections,
                    include_prompt=include_prompt,
                    exclude_prompt=exclude_prompt,
                    include_tree=include_tree,
                    exclude_tree=exclude_tree,
                    global_files_dir=GLOBAL_FILES_DIR,
                    output_file=temp_output
                )

                # Read the generated context file
                with open(temp_output, 'r', encoding='utf-8') as f:
                    context_content = f.read()

                # Provide download link
                st.download_button(
                    label="Download repo-context.txt",
                    data=context_content,
                    file_name='repo-context.txt',
                    mime='text/plain'
                )
                st.success("Context file generated successfully.")
        except Exception as e:
            st.error(f"Error generating context file: {e}")
