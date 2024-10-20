# Repository Context Generator

The **Repository Context Generator** is a tool designed to create a comprehensive context file (`repo-context.txt`) for AI coding assistants like ChatGPT. This context file aggregates essential information from your repository, including an overview, key details, a directory tree with exclusions, contents of important files with syntax highlighting, and a to-do list. This facilitates more informed and efficient interactions with AI assistants regarding your codebase.

## Features

- **Context File Generation**: Creates a `repo-context.txt` file tailored for AI assistants.
- **Configurable Directory Tree**: Generates a directory tree with the ability to exclude specified directories.
- **Highlighted File Contents**: Incorporates important files with syntax highlighting based on their file types.
- **Static Content Integration**: Adds static sections from files such as `overview.txt`, `important_info.txt`, and `to-do_list.txt`.
- **Extensible Configuration**: Easily customize exclusions, important files, and additional sections via `config.yaml`.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Set Up Python Virtual Environment (Optional but Recommended)](#step-2-set-up-python-virtual-environment-optional-but-recommended)
  - [Step 3: Install Required Packages](#step-3-install-required-packages)
  - [Step 4: Configure the Script](#step-4-configure-the-script)
  - [Step 5: Running the Script](#step-5-running-the-script)
- [Output](#output)
- [Customization](#customization)
  - [Modifying `config.yaml`](#modifying-configyaml)
- [Additional Notes](#additional-notes)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- **Python 3.7 or higher**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: To clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).

## Setup Guide

### Step 1: Clone the Repository

Clone this repository to your local machine using Git:

```bash
git clone <repository-url>
cd <repository-directory>
```

*Replace `<repository-url>` with the actual URL of your repository and `<repository-directory>` with the cloned directory name.*

### Step 2: Set Up Python Virtual Environment (Optional but Recommended)

Using a virtual environment isolates your project's dependencies, preventing conflicts with other projects.

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:

   - **macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```
   
   - **Windows (Command Prompt)**:
     ```bash
     venv\Scripts\activate.bat
     ```
   
   - **Windows (PowerShell)**:
     ```bash
     venv\Scripts\Activate.ps1
     ```

### Step 3: Install Required Packages

Install the necessary Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Script

Customize the `config.yaml` file to control which directories and files are included or excluded in the generated context.

1. **Locate `config.yaml`**: It's in the root directory of the cloned repository.

2. **Edit `config.yaml`**:
   - **Exclude Directories**: Modify the `exclude_dirs` section to exclude any directories you don't want in the context.
   - **Important Files**: List the key files under the `important_files` section that should be included with their content.

*Refer to the [Customization](#customization) section for detailed instructions.*

### Step 5: Running the Script

Execute the script to generate the `repo-context.txt` file.

- **Unix-like Systems (macOS, Linux)**:
  
  ```bash
  chmod +x generate_repo-context.py  # Make the script executable (optional)
  ./generate_repo-context.py
  ```

  Or simply:

  ```bash
  python3 generate_repo-context.py
  ```

- **Windows**:

  ```bash
  python generate_repo-context.py
  ```

## Output

After running the script, a `repo-context.txt` file will be generated in the current directory. This file includes the following sections:

- **Overview**: Content from `overview.txt`
- **Important Information**: Content from `important_info.txt`
- **Directory Tree**: Structure of your project with specified exclusions
- **Important Files**: Contents of key files with syntax highlighting
- **To-Do List**: Content from `to-do_list.txt`

## Customization

### Modifying `config.yaml`

The `config.yaml` file allows you to tailor the context generation process to your project's needs.

#### 1. **Exclude Directories**

Specify directories that should be omitted from the directory tree and file inclusions.

```yaml
exclude_dirs:
  - node_modules          # Node.js dependencies
  - venv                  # Python virtual environment
  - __pycache__           # Python bytecode cache
  - build                 # Build output directories
  - dist                  # Distribution packages
  - .git                  # Git repository metadata
  - .github               # GitHub workflows and configurations
  - .vscode               # Visual Studio Code settings
  - logs                  # Log files
  - tmp                   # Temporary files and directories
```

*Add or remove directories as needed.*

#### 2. **Important Files**

List the crucial files whose content should be included in the context file. Paths should be relative to the main source directory (default is `src/`).

```yaml
important_files:
  - main.py                       # Entry point of the application
  - app.py                        # Application configuration
  - config/settings.py            # Configuration settings
  - utils/helpers.py              # Utility helper functions
  - models/user.py                # User model definitions
  - controllers/auth_controller.py# Authentication controller
  - services/email_service.py     # Email service integration
  - routes/api_routes.py          # API route definitions
  - database/db_connection.py     # Database connection setup
  - tests/test_main.py            # Main application tests
```

*Update the list based on your project's structure.*

#### 3. **Additional Configuration (Optional)**

Uncomment and customize additional sections for more advanced configurations.

```yaml
# List of file types to include based on extensions.
file_type_inclusions:
  - .js
  - .ts
  - .java
  - .rb
  - .go

# List of file types to exclude based on extensions.
file_type_exclusions:
  - .log
  - .tmp
  - .png
  - .jpg
  - .gif

# Custom sections to include additional information.
custom_sections:
  - file: changelog.txt
    section_title: "Changelog"
  - file: LICENSE.txt
    section_title: "License"
```

*Customize these sections as per your project requirements.*

## Additional Notes

- **Static Files**: Ensure that `overview.txt`, `important_info.txt`, and `to-do_list.txt` are present in the same directory as `generate_repo-context.py`.
- **Syntax Highlighting**: The script supports syntax highlighting for common file types like `.py`, `.js`, `.json`, etc. To add more file types, update the `LANGUAGE_MAP` in the script.
- **Source Directory**: By default, the script assumes your main source code is in the `src/` directory. If your project uses a different structure, update the `start_path` in the script or make it configurable.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

---
