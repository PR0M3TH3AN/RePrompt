# RePrompt: A Context Generator

This app is to be used in conjunction with [mckaywrigley's xml parser](https://github.com/mckaywrigley/o1-xml-parser/tree/main).

The **RePrompt** is a tool designed to create a comprehensive context file (`repo-context.txt`) for AI coding assistants like ChatGPT. The context file aggregates essential information from your repository, including an overview, directory tree, excluded and included files, highlighted file contents, and additional static sections like a to-do list.

## Features

- **Streamlit Web App**: Intuitive interface to select folders, configure file inclusions/exclusions, and generate the context file.
- **Context File Generation**: Produces a `repo-context.txt` file tailored for AI assistants.
- **Configurable Directory Tree**: Exclude specified directories and files from the context.
- **File Content Integration**: Includes syntax-highlighted contents of key files.
- **Static Content Integration**: Adds static sections from files such as `overview.txt` and `to-do_list.txt`.
- **Save & Load Configurations**: Retain file inclusion/exclusion preferences for future sessions.
- **Default Exclusions**: Automatically excludes `node_modules`, `venv`, `__pycache__`, and `repo-context.txt` to avoid unnecessary content in the context.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Set Up a Python Virtual Environment](#step-2-set-up-a-python-virtual-environment)
  - [Step 3: Install Required Packages](#step-3-install-required-packages)
  - [Step 4: Run the Streamlit Application](#step-4-run-the-streamlit-application)
- [How to Use](#how-to-use)
  - [Selecting a Folder](#selecting-a-folder)
  - [Configuring Inclusions and Exclusions](#configuring-inclusions-and-exclusions)
  - [Generating the Context File](#generating-the-context-file)
  - [Saving and Loading Configurations](#saving-and-loading-configurations)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

---

## Prerequisites

- **Python 3.7 or higher**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/downloads/).
- **Streamlit**: The tool is built using the Streamlit web framework.
- **Git**: To clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).

---

## Setup Guide

### Step 1: Clone the Repository

Clone this repository to your local machine using Git:

```bash
git clone <repository-url>
cd <repository-directory>
```

_Replace `<repository-url>` with the actual repository URL._

---

### Step 2: Set Up a Python Virtual Environment

A virtual environment helps isolate dependencies:

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - **macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

---

### Step 3: Install Required Packages

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

---

### Step 4: Run the Streamlit Application

Start the application with the following command:

```bash
streamlit run app.py
```

The application will open in your default web browser. If not, follow the link provided in the terminal (e.g., `http://localhost:8501`).

---

## How to Use

### Selecting a Folder

1. Use the **Choose Folder** button in the sidebar to open a folder selection dialog.
2. Select the root folder of the repository for which you want to generate the context file.

---

### Configuring Inclusions and Exclusions

1. **Directory Tree**: Use the directory multiselect to include specific directories in the context file.
2. **File Exclusions**: Automatically include files within selected directories but exclude specific files if needed.
3. **Default Exclusions**:
   - The following are excluded by default: `node_modules`, `venv`, `__pycache__`, `.git`, `dist`, `build`, `logs`, `.idea`, `.vscode`, and `repo-context.txt`.

---

### Generating the Context File

1. After configuring inclusions and exclusions, click the **Generate Context File** button.
2. The context file will be created, and a **Download** button will appear for you to save the `repo-context.txt`.

---

### Saving and Loading Configurations

- **Save Configuration**: Use the "Save Configuration" button to save your current settings (selected directories and excluded files).
- **Load Configuration**: The app automatically loads the saved configuration at startup.

---

## Customization

### Modifying Default Exclusions

To modify the default exclusions, edit the `DEFAULT_EXCLUDED_DIRS` and `DEFAULT_EXCLUDED_FILES` lists in `app.py`:

```python
DEFAULT_EXCLUDED_DIRS = ["node_modules", "venv", "__pycache__", ".git", "dist", "build", "logs", ".idea", ".vscode"]
DEFAULT_EXCLUDED_FILES = ["repo-context.txt"]
```

---

### Using the Configuration File

The `config.yaml` file allows further customization:

1. **Exclude Directories**:
   ```yaml
   exclude_dirs:
     - node_modules
     - venv
     - __pycache__
   ```
2. **Important Files**:
   ```yaml
   important_files:
     - main.py
     - app.py
   ```

---

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for bug fixes, enhancements, or feature requests.

---

## License

This project is licensed under the [MIT License](LICENSE).
