import streamlit as st
from pathlib import Path
import os
import yaml
from tkinter import Tk
from tkinter.filedialog import askdirectory
import subprocess
import sys 
import pyperclip

# Initialize session state variables
if 'copied' not in st.session_state:
    st.session_state.copied = False

# Configuration
CONFIG_FILE = "config.yaml"
OUTPUT_FILE = "repo-context.txt"
GLOBAL_FILES_DIR = Path(__file__).parent / "global_files"
SAVED_CONFIG_FILE = Path(__file__).parent / "saved_config.yaml"
SCRIPT_DIR = Path(__file__).parent

# Default exclusions
DEFAULT_EXCLUDED_DIRS = ["node_modules", "venv", "__pycache__", ".git", "dist", "build", "logs", ".idea", ".vscode"]
DEFAULT_EXCLUDED_FILES = ["repo-context.txt"]

# Ensure necessary directories exist
GLOBAL_FILES_DIR.mkdir(exist_ok=True)

# Load saved configuration
def load_saved_config():
    if SAVED_CONFIG_FILE.exists():
        try:
            with open(SAVED_CONFIG_FILE, "r") as f:
                return yaml.safe_load(f)
        except yaml.YAMLError:
            return {}
    return {}

# Save configuration
def save_config(config):
    with open(SAVED_CONFIG_FILE, "w") as f:
        yaml.dump(config, f)

# Load application configuration
def load_config():
    config_path = SCRIPT_DIR / CONFIG_FILE
    if not config_path.exists():
        st.error(f"Configuration file {CONFIG_FILE} not found.")
        st.stop()
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        st.error(f"Error parsing configuration file: {e}")
        st.stop()

app_config = load_config()
saved_config = load_saved_config()

exclude_dirs = app_config.get("exclude_dirs", DEFAULT_EXCLUDED_DIRS)

# Initialize session state for selected_repo_path if not present
if "selected_repo_path" not in st.session_state:
    st.session_state["selected_repo_path"] = None

# Streamlit App
st.title("Repository Context Generator")

# Folder Selection
st.sidebar.header("Select a Folder")

def select_folder():
    try:
        root = Tk()
        root.withdraw()  # Hide the main window
        root.wm_attributes('-topmost', True)  # Keep on top
        folder_path = askdirectory(parent=root)  # Specify parent window
        if folder_path:
            st.session_state["selected_repo_path"] = folder_path
            return True
        return False
    except Exception as e:
        st.error(f"Error selecting folder: {str(e)}")
        return False
    finally:
        try:
            root.destroy()  # Ensure window is destroyed
        except:
            pass  # Ignore any errors during cleanup

if st.sidebar.button("Choose Folder"):
    if select_folder():
        st.sidebar.success(f"Selected folder: {st.session_state['selected_repo_path']}")
    else:
        st.sidebar.error("No folder selected.")

# Load previously selected folder
selected_repo_path = st.session_state.get("selected_repo_path", None)

if selected_repo_path:
    st.header(f"Selected Repository: {selected_repo_path}")
    repo_path = Path(selected_repo_path)

    st.subheader("File Filtering")
    # Retrieve directories and files in the repository
    all_directories = []
    all_files = []
    for root_dir, dirs, files in os.walk(repo_path):
        rel_root = Path(root_dir).relative_to(repo_path)
        # Exclude default directories
        dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDED_DIRS]
        for d in dirs:
            all_directories.append(str(rel_root / d) + "/")
        for f in files:
            all_files.append(str(rel_root / f))

    # Directory selection for Directory Tree
    selected_directories = st.multiselect(
        "Include in Directory Tree",
        options=all_directories,
        default=saved_config.get("selected_directories", [])
    )

    # Automatically include files within selected directories unless explicitly excluded
    included_files = [
        f for f in all_files if any(str(Path(f).parent) in d for d in selected_directories)
    ]

    # File exclusions
    excluded_files = st.multiselect(
        "Exclude Specific Files",
        options=[f for f in included_files if f not in DEFAULT_EXCLUDED_FILES],
        default=[
            f for f in saved_config.get("excluded_files", [])
            if f in included_files and f not in DEFAULT_EXCLUDED_FILES
        ],
    )

    st.write("### Final Included Files")
    final_included_files = [f for f in included_files if f not in excluded_files]
    st.write(final_included_files)

    st.subheader("Generate Context File")
    if st.button("Generate Context File"):
        try:
            # Update config.yaml based on user selections
            updated_config = {
                "source_directory": str(repo_path),
                "exclude_dirs": DEFAULT_EXCLUDED_DIRS,
                "important_files": final_included_files,
                "custom_sections": app_config.get("custom_sections", []),
            }

            # Write updated config.yaml
            with open(SCRIPT_DIR / CONFIG_FILE, "w") as f:
                yaml.dump(updated_config, f)

            # Run the script as a subprocess
            result = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "generate_repo_context.py")],
                cwd=SCRIPT_DIR,
                check=True,
                capture_output=True,
                text=True,
            )

            st.success("Context file generated successfully.")
            st.write(f"Script output:\n{result.stdout}")

            # Check if the file was created
            generated_file = SCRIPT_DIR / OUTPUT_FILE
            if generated_file.exists():
                with open(generated_file, "r", encoding="utf-8") as f:
                    context_content = f.read()

                # Replace the current copy button section with this:
                if context_content.strip():  # Ensure content is not empty
                    # Add Download Button with unique key
                    st.download_button(
                        label="Download repo-context.txt",
                        data=context_content,
                        file_name="repo-context.txt",
                        mime="text/plain",
                        key="download_button_1"
                    )

                    st.info("To copy: Click in the text area, press Ctrl+A (Cmd+A on Mac) to select all, then Ctrl+C (Cmd+C on Mac) to copy.")

                    # Create a text area with the content
                    text_area = st.text_area(
                        "Generated Context File",
                        value=context_content,
                        height=400,
                        key="context_content"
                    )
                else:
                    st.error("Generated content is empty. Please review your repository and configurations.")
            else:
                st.error("Context file not found after script execution.")
        except subprocess.CalledProcessError as e:
            st.error("Error generating context file:")
            if e.stdout:
                st.text(f"Standard Output:\n{e.stdout}")
            if e.stderr:
                st.text(f"Standard Error:\n{e.stderr}")

    # Save configuration for future use
    if st.button("Save Configuration"):
        save_config({
            "selected_directories": selected_directories,
            "excluded_files": excluded_files,
        })
        st.success("Configuration saved successfully.")
else:
    st.write("Please select a folder to begin.")