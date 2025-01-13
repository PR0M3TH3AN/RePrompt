Certainly! Below is the updated `README.md` for your **Repository Context Generator Web App**, which includes detailed run commands and clarifies the setup process. This update ensures that users can easily follow the steps to install, activate the virtual environment, install dependencies, and run the Streamlit application.

---

# Repository Context Generator Web App

The **Repository Context Generator** is a Streamlit-based web application designed to create a comprehensive context file (`repo-context.txt`) for AI coding assistants like ChatGPT. This context file aggregates essential information from your repository, including an overview, key details, a directory tree with exclusions, contents of important files with syntax highlighting, and a to-do list. Additionally, it supports the inclusion of global files that are incorporated into every generated context, regardless of the selected repository.

## **Features**

- **Repository Selection**: Choose from existing repositories or add new ones by providing their Git URLs.
- **File Filtering**: Select which files to include or exclude from the prompt and directory tree.
- **Global Files Management**: Add files that will be included in every generated context.
- **Context File Generation**: Generate and download a tailored `repo-context.txt` file.
- **XML Section Integration**: Automatically append an XML section adhering to specified formatting rules.

## **Prerequisites**

- **Python 3.7 or higher**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/downloads/).
- **Git**: To clone repositories. Download from [git-scm.com](https://git-scm.com/downloads).

## **Directory Structure**

```
repository-context-generator/
├── app.py
├── generate_repo_context.py
├── config.yaml
├── requirements.txt
├── global_files/
│   └── global.xml
├── static_files/
│   ├── overview.txt
│   ├── important_info.txt
│   └── to-do_list.txt
└── README.md
```

## **Setup Guide**

### **1. Clone the Repository**

Clone this repository to your local machine using Git:

```bash
git clone <repository-url>
cd repository-context-generator
```

_Replace `<repository-url>` with the actual URL of your repository._

### **2. Set Up Python Virtual Environment (Optional but Recommended)**

Using a virtual environment isolates your project's dependencies, preventing conflicts with other projects.

#### **a. Create a Virtual Environment**

```bash
python -m venv venv
```

#### **b. Activate the Virtual Environment**

- **On Windows (Command Prompt):**

  ```cmd
  venv\Scripts\activate.bat
  ```

- **On Windows (PowerShell):**

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

  **Note:** If you encounter an execution policy error in PowerShell, you may need to adjust the execution policy:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

  Then, try activating the virtual environment again.

- **On macOS and Linux:**

  ```bash
  source venv/bin/activate
  ```

**Successful Activation:**

Once activated, your terminal prompt should change to indicate that you're now working within the virtual environment, e.g., `(venv) $`.

### **3. Install Required Packages**

With the virtual environment activated, install the necessary Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### **4. Configure the Application**

Customize the `config.yaml` file to control which directories and files are included or excluded in the generated context.

1. **Locate `config.yaml`**: It's in the root directory of the cloned repository.

2. **Edit `config.yaml`**:
   - **Exclude Directories**: Modify the `exclude_dirs` section to exclude any directories you don't want in the context.
   - **Important Files**: List the key files under the `important_files` section that should be included with their content.
   - **Custom Sections**: Define any additional sections you want to include.

_Refer to the [Customization](#customization) section for detailed instructions._

### **5. Add Static and Global Files**

Ensure that the following files are present:

- **Static Files**: Place `overview.txt`, `important_info.txt`, and `to-do_list.txt` inside the `static_files/` directory.
- **Global Files**: Place any global files (e.g., `global.xml`) inside the `global_files/` directory.

### **6. Running the Application**

Launch the Streamlit web application:

```bash
streamlit run app.py
```

This command will open the application in your default web browser. If it doesn't open automatically, navigate to [http://localhost:8501](http://localhost:8501) in your browser.

**Additional Run Commands:**

- **Deactivate the Virtual Environment (When Done):**

  ```bash
  deactivate
  ```

- **Reactivating the Virtual Environment:**

  Navigate back to the project directory and activate the virtual environment as described in **Step 2b**.

## **Customization**

### **Modifying `config.yaml`**

The `config.yaml` file allows you to tailor the context generation process to your project's needs.

```yaml
# Configuration for Repository Context Generator

# Primary source directory containing the main codebase.
# Update this if your main code is not in 'src/'.
source_directory: src

# List of directories to exclude from the directory tree and file inclusions.
exclude_dirs:
  - node_modules # Node.js dependencies
  - venv # Python virtual environment
  - __pycache__ # Python bytecode cache
  - build # Build output directories
  - dist # Distribution packages
  - .git # Git repository metadata
  - .github # GitHub workflows and configurations
  - .vscode # Visual Studio Code settings
  - logs # Log files
  - tmp # Temporary files and directories

# List of important files to include in the context.
# Paths should be relative to the 'source_directory' specified above.
important_files:
  - main.py # Entry point of the application
  - app.py # Application configuration
  - config/settings.py # Configuration settings
  - utils/helpers.py # Utility helper functions
  - models/user.py # User model definitions
  - controllers/auth_controller.py # Authentication controller
  - services/email_service.py # Email service integration
  - routes/api_routes.py # API route definitions
  - database/db_connection.py # Database connection setup
  - tests/test_main.py # Main application tests

# Custom sections to include additional information.
custom_sections:
  - file: changelog.txt
    section_title: "Changelog"
  - file: LICENSE.txt
    section_title: "License"
```

**Instructions for Customization:**

1. **`source_directory`**:

   - Set this to the primary directory containing your source code.
   - Example: For a project with main code in `app/`, set `source_directory: app`.

2. **`exclude_dirs`**:

   - Review the list and remove any directories that are essential for your project context.
   - Add any additional directories you want to exclude by appending them to the list.
   - Example: If your project uses a `docs/` directory for documentation, you might choose to exclude it:
     ```yaml
     - docs
     ```

3. **`important_files`**:

   - Identify the key files in your project that define its core functionality.
   - Ensure the paths are relative to your `source_directory`.
   - Add or remove files as necessary to reflect your project's structure.
   - Example: For a JavaScript project, you might include:
     ```yaml
     - index.js
     - src/app.js
     - src/routes/index.js
     - src/controllers/userController.js
     ```

4. **`custom_sections`**:
   - Define additional sections by specifying the file and its corresponding section title.
   - Ensure the specified files exist in the `static_files/` directory or provide their paths accordingly.

## **Additional Notes**

- **Global Files**: Files placed in the `global_files/` directory are included in every generated context, regardless of the selected repository. For example, `global.xml` can be used to enforce specific formatting rules across all contexts.

- **Syntax Highlighting**: The script supports syntax highlighting for common file types like `.py`, `.js`, `.json`, etc. To add more file types, update the `LANGUAGE_MAP` in `generate_repo_context.py`.

- **Source Directory**: By default, the script assumes your main source code is in the `src/` directory. If your project uses a different structure, update the `source_directory` in `config.yaml`.

- **Error Handling**: The application includes basic error handling to notify users of missing files or configuration issues. Ensure all necessary files are present to avoid errors.

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Conclusion**

By following the above setup and utilizing the provided scripts, you can efficiently generate comprehensive context files for your repositories directly from your browser. The integration of global files ensures consistency across all generated contexts, while the interactive interface simplifies repository management and file filtering.

Feel free to customize and extend the application to better fit your specific requirements. Contributions and feedback are highly appreciated!

---
