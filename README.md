Here's the improved README.md:

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
- **Default Exclusions**: Automatically excludes common directories and files to avoid unnecessary content.

## Prerequisites

- **Python 3.7 or higher**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads)

## Directory Structure

```
repository-context-generator/
├── src/
│   ├── app.py                   # Main Streamlit application
│   ├── generate_repo_context.py # Context generation script
│   ├── config.yaml             # Configuration file
│   ├── requirements.txt        # Python dependencies
│   ├── global_files/           # Global files for all contexts
│   └── static_files/           # Static content files
│       ├── overview.txt        # Project overview
│       ├── important_info.txt  # Important information
│       └── to-do_list.txt     # Project to-do list
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd repository-context-generator
```

### 2. Create Required Directories and Files

```bash
mkdir -p src/static_files src/global_files
touch src/static_files/overview.txt
touch src/static_files/important_info.txt
touch src/static_files/to-do_list.txt
```

### 3. Set Up Virtual Environment

#### Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate using Command Prompt
venv\Scripts\activate.bat

# OR activate using PowerShell
.\venv\Scripts\Activate.ps1
```

#### macOS/Linux:

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:

```txt
streamlit
PyYAML
Flask
Flask-Cors
GitPython
pyperclip
```

## Running the Application

```bash
cd src
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

### 1. Initial Setup

- Create a basic `config.yaml` file in the src directory:

```yaml
exclude_dirs:
  - node_modules
  - venv
  - __pycache__
  - .git
  - dist
  - build
  - logs
  - .idea
  - .vscode

important_files: []
custom_sections: []
```

### 2. Select Repository

- Click "Choose Folder" in the sidebar
- Navigate to your target repository
- Select the folder

### 3. Configure Files

- Select directories to include in the "Include in Directory Tree" section
- Exclude specific files if needed
- Review the "Final Included Files" list

### 4. Generate Context

- Click "Generate Context File"
- Download or copy the generated context
- Save your configuration if desired

## Customization

### Modify Default Exclusions

Edit `DEFAULT_EXCLUDED_DIRS` and `DEFAULT_EXCLUDED_FILES` in `app.py`:

```python
DEFAULT_EXCLUDED_DIRS = [
    "node_modules",
    "venv",
    "__pycache__",
    ".git",
    "dist",
    "build",
    "logs",
    ".idea",
    ".vscode"
]

DEFAULT_EXCLUDED_FILES = ["repo-context.txt"]
```

### Add Custom Sections

Modify `config.yaml` to add custom sections:

```yaml
custom_sections:
  - file: changelog.txt
    section_title: "Changelog"
  - file: LICENSE.txt
    section_title: "License"
```

## Troubleshooting

### Common Issues

1. **Tcl_AsyncDelete Warning**

   ```
   Tcl_AsyncDelete: async handler deleted by the wrong thread
   ```

   This warning can be safely ignored; it doesn't affect functionality.

2. **Permission Denied When Creating Directories**

   - Run terminal/command prompt as administrator
   - Check folder permissions
   - Ensure you have write access to the installation directory

3. **Package Installation Failures**

   ```bash
   # If pip install fails, try:
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Streamlit Port Already in Use**
   - Kill any running Streamlit processes
   - Change the port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For issues and feature requests, please create an issue in the GitHub repository.
