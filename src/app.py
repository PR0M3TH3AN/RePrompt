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
SCRIPT_DIR = Path(__file__).parent

# Default exclusions
DEFAULT_EXCLUDED_DIRS = ["node_modules", "venv", "__pycache__", ".git", "dist", "build", "logs", ".idea", ".vscode"]
DEFAULT_EXCLUDED_FILES = [
    "repo-context.txt",
    "package-lock.json",
    "yarn.lock",
    ".gitattributes",
    ".gitignore",
    ".dockerignore",
    ".env",
    "*.pem",
    "*.crt",
    "*.key",
    ".eslintrc",
    ".prettierrc",
    ".browserslistrc",
    ".editorconfig",
    "client.crt",
    "client-key.pem",
    "docker-compose.yml",
    ".env.local",
    ".env.development",
    ".env.production"
]

# Load saved configuration from repository directory
def load_saved_config(repo_path):
    saved_config_path = repo_path / "saved_config.yaml"
    try:
        if saved_config_path.exists():
            with open(saved_config_path, "r") as f:
                saved_config = yaml.safe_load(f)
                return saved_config if saved_config else {}
        return {}
    except Exception:
        return {}

# Save configuration to repository directory
def save_config(config, repo_path):
    try:
        if not config:  # Don't save empty configs
            return
        saved_config_path = repo_path / "saved_config.yaml"
        with open(saved_config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception:
        pass

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

# Clear config.yaml
def clear_config():
    config_path = SCRIPT_DIR / CONFIG_FILE
    with open(config_path, "w") as f:
        yaml.dump({}, f)

app_config = load_config()
exclude_dirs = app_config.get("exclude_dirs", DEFAULT_EXCLUDED_DIRS)

# Initialize session state for selected_repo_path if not present
if "selected_repo_path" not in st.session_state:
    st.session_state["selected_repo_path"] = None

# Streamlit App
st.title("RePrompt: A Context Generator")

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
    current_config = load_saved_config(repo_path)  # Load config from repo directory

    st.subheader("File Filtering")
    # Retrieve directories and files in the repository
    all_directories = []
    all_files = []
    for root_dir, dirs, files in os.walk(repo_path):
        rel_root = Path(root_dir).relative_to(repo_path)
        # Exclude default directories
        dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDED_DIRS]
        
        # Add directories
        for d in dirs:
            all_directories.append(str(rel_root / d) + "/")
        
        # Add files (including root files)
        for f in files:
            # Skip files that match any of the default excluded patterns
            if any(f.endswith(excluded.replace('*', '')) for excluded in DEFAULT_EXCLUDED_FILES if '*' in excluded) or \
               f in DEFAULT_EXCLUDED_FILES:
                continue
                
            file_path = str(rel_root / f)
            if file_path.startswith('.'):  # Handle root files
                file_path = file_path[2:]  # Remove './'
            all_files.append(file_path)

    # Directory selection for Directory Tree
    # Filter out any saved directories that don't exist in current options
    saved_directories = current_config.get("selected_directories", [])
    valid_saved_directories = [d for d in saved_directories if d in all_directories]
    
    selected_directories = st.multiselect(
        "Include in Directory Tree",
        options=all_directories,
        default=valid_saved_directories
    )

    # Include all files in selected directories AND root files
    included_files = [
        f for f in all_files if (
            any(str(Path(f).parent) in d for d in selected_directories) or  # Files in selected directories
            str(Path(f).parent) == '.' or  # Root files
            str(Path(f).parent) == ''      # Also handles root files
        )
    ]

    # File exclusions
    available_files = [f for f in included_files if f not in DEFAULT_EXCLUDED_FILES]
    saved_exclusions = [f for f in current_config.get("excluded_files", [])
                       if f in available_files and f not in DEFAULT_EXCLUDED_FILES]
    
    excluded_files = st.multiselect(
        "Exclude Specific Files",
        options=available_files,
        default=saved_exclusions
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
                "custom_sections": app_config.get("custom_sections", [])
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

            # Clear config.yaml after generation
            clear_config()

            st.success("Context file generated successfully.")
            st.write(f"Script output:\n{result.stdout}")

            # Check if the file was created in script directory first
            generated_file = SCRIPT_DIR / "repo-context.txt"
            if generated_file.exists():
                # Read content
                with open(generated_file, "r", encoding="utf-8") as f:
                    context_content = f.read()

                # Copy file to repository directory
                repo_context_file = repo_path / "repo-context.txt"
                with open(repo_context_file, "w", encoding="utf-8") as f:
                    f.write(context_content)
                
                # Delete the file from script directory
                generated_file.unlink()

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

                    st.success(f"Context file saved to: {repo_context_file}")
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
        }, repo_path)
        st.success("Configuration saved successfully.")
else:
    st.write("Please select a folder to begin.")