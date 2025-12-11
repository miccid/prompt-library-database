# Prompt Library Database

A professional Streamlit application for managing a comprehensive library of AI prompts with advanced tagging, local-first data storage, and a user-friendly web interface. Perfect for organizing, searching, and managing prompts for various AI models and use cases.

**Version:** 2.0
**License:** MIT
**Author:** Michael Cid

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Setup on Linux](#setup-on-linux)
  - [Setup on macOS](#setup-on-macos)
  - [Setup on Windows](#setup-on-windows)
- [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)

---

## Features

- **Browse & Search**: View all prompts in your library with real-time search functionality
- **Add New Prompts**: Create new prompts with structured data and custom tags
- **Edit Prompts**: Modify existing prompts to refine and improve them over time
- **Delete Prompts**: Remove prompts you no longer need
- **Advanced Tagging System**: Organize prompts with categorized tags for better organization
- **Copy to Clipboard**: Quickly copy prompt text to your clipboard with a single click
- **Authentication**: Secure access with username and password protection
- **Local-First Storage**: All data stored locally in an SQLite database for privacy and reliability
- **Professional UI**: Clean, intuitive web interface built with Streamlit

---

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **Git** (optional, but recommended) ([Download Git](https://git-scm.com/))
- A terminal application (Terminal on Mac/Linux, Command Prompt or PowerShell on Windows)
- A modern web browser (Chrome, Firefox, Safari, or Edge)

To check if Python is installed, open your terminal and run:
```bash
python --version
```

---

## Installation & Setup

Follow the instructions for your operating system below.

### Setup on Linux

#### Step 1: Navigate to Your Project Directory

Open a terminal and navigate to where you want to store the project:

```bash
cd ~/projects
```

#### Step 2: Clone or Download the Repository

If you have Git installed:
```bash
git clone https://github.com/miccid/prompt-library-database.git
cd prompt-library-database
```

Or download the ZIP file from GitHub and extract it, then navigate to the folder.

#### Step 3: Create a Virtual Environment

A virtual environment keeps this project's dependencies separate from your system Python:

```bash
python3 -m venv .venv
```

#### Step 4: Activate the Virtual Environment

```bash
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your terminal line, indicating the virtual environment is active.

#### Step 5: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install Streamlit and other necessary libraries.

#### Step 6: Configure Environment Variables (Optional)

Create a `.env` file in the project directory:

```bash
nano .env
```

Add the following variables:

```
USERNAME=admin
PASSWORD=admin
PROMPT_DB_FILE=prompts.db
```

Press `Ctrl+O`, then `Enter` to save, and `Ctrl+X` to exit.

#### Step 7: Run the Application

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`. If not, copy and paste this URL into your browser.

---

### Setup on macOS

#### Step 1: Navigate to Your Project Directory

Open Terminal (press `Cmd + Space`, type "Terminal", then press Enter) and navigate to your desired location:

```bash
cd ~/Documents
```

#### Step 2: Clone or Download the Repository

If you have Git installed:
```bash
git clone https://github.com/miccid/prompt-library-database.git
cd prompt-library-database
```

Or download the ZIP file from GitHub and extract it, then navigate to the folder.

#### Step 3: Create a Virtual Environment

```bash
python3 -m venv .venv
```

#### Step 4: Activate the Virtual Environment

```bash
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your terminal line.

#### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 6: Configure Environment Variables (Optional)

Create a `.env` file:

```bash
nano .env
```

Add the following:

```
USERNAME=admin
PASSWORD=admin
PROMPT_DB_FILE=prompts.db
```

Save with `Ctrl+O`, `Enter`, then `Ctrl+X`.

#### Step 7: Run the Application

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`.

---

### Setup on Windows

#### Step 1: Open Command Prompt or PowerShell

Press `Windows Key + R`, type `cmd` or `powershell`, and press Enter.

#### Step 2: Navigate to Your Project Directory

```bash
cd Documents
```

#### Step 3: Clone or Download the Repository

If you have Git installed:
```bash
git clone https://github.com/miccid/prompt-library-database.git
cd prompt-library-database
```

Or download the ZIP file from GitHub and extract it, then navigate to the folder using File Explorer.

#### Step 4: Create a Virtual Environment

```bash
python -m venv .venv
```

#### Step 5: Activate the Virtual Environment

**For Command Prompt:**
```bash
.venv\Scripts\activate
```

**For PowerShell:**
```bash
.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of your terminal line.

> **Note:** If you get an error in PowerShell about execution policy, run:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 7: Configure Environment Variables (Optional)

Create a `.env` file in the project directory. Open Notepad, add the following lines:

```
USERNAME=admin
PASSWORD=admin
PROMPT_DB_FILE=prompts.db
```

Save the file as `.env` (not `.env.txt`) in the project directory. You may need to change the file type to "All Files" when saving.

#### Step 8: Run the Application

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`. If not, copy and paste this URL into your address bar.

---

## Docker Setup

If you prefer to run the application in Docker, follow these steps:

### Prerequisites for Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Running with Docker

#### Step 1: Build the Docker Image

Navigate to the project directory and run:

```bash
docker build -t prompt-library-database .
```

#### Step 2: Run the Docker Container

```bash
docker run -p 8501:8501 -v $(pwd):/app prompt-library-database
```

**For Windows (Command Prompt):**
```bash
docker run -p 8501:8501 -v %cd%:/app prompt-library-database
```

**For Windows (PowerShell):**
```bash
docker run -p 8501:8501 -v ${PWD}:/app prompt-library-database
```

#### Step 3: Access the Application

Open your browser and navigate to `http://localhost:8501`

### Using Docker Compose

Alternatively, you can use Docker Compose for easier management:

```bash
docker-compose up
```

To stop the container:
```bash
docker-compose down
```

---

## Environment Variables

The application uses environment variables for configuration. You can set these in a `.env` file or as system environment variables.

### Available Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USERNAME` | `admin` | Default login username |
| `PASSWORD` | `admin` | Default login password |
| `PROMPT_DB_FILE` | `prompts.db` | Path to the SQLite database file |

### Creating a `.env` File

Create a file named `.env` in the project root directory with your desired configuration:

```env
USERNAME=your_username
PASSWORD=your_secure_password
PROMPT_DB_FILE=prompts.db
```

The application will automatically load these values on startup.

> **Security Note:** Never commit the `.env` file to version control. It's already included in `.gitignore`.

---

## Running the Application

### Standard Method (with activated virtual environment)

```bash
streamlit run app.py
```

### With Environment Variables

If your `.env` file is configured, the app will automatically load the settings:

```bash
streamlit run app.py
```

### First Run

When you run the application for the first time:
- A SQLite database file (`prompts.db`) will be created automatically in the project directory
- You'll see the login page; use the default credentials (username: `admin`, password: `admin`) or your configured credentials
- The database is ready to use—no additional setup required

### Stopping the Application

Press `Ctrl+C` in your terminal to stop the Streamlit server.

---

## File Structure

```
prompt-library-database/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python package dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore rules
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── prompts.db              # SQLite database (auto-created on first run)
└── README.md               # This file
```

### Key Files Explained

- **app.py**: The main Python application containing all Streamlit UI components and database logic
- **requirements.txt**: Lists all Python packages needed (Streamlit, clipboard support, etc.)
- **.env**: Configuration file for sensitive data (usernames, passwords)
- **prompts.db**: Your local SQLite database where all prompts are stored
- **Dockerfile & docker-compose.yml**: Configuration for running the app in Docker containers

---

## Troubleshooting

### Issue: "Python is not recognized as an internal or external command"

**Solution (Windows):**
- Python is not installed or not added to your system PATH
- Download and install Python from [python.org](https://www.python.org/downloads/)
- During installation, **check the box** that says "Add Python to PATH"
- Restart your computer and try again

**Solution (Mac/Linux):**
- Try `python3` instead of `python`
- Install Python 3 using Homebrew (Mac): `brew install python3`

### Issue: "No module named 'streamlit'"

**Solution:**
- Make sure your virtual environment is activated (you should see `(.venv)` in your terminal)
- Run `pip install -r requirements.txt` again
- If issues persist, try: `pip install --upgrade streamlit`

### Issue: Virtual environment is not activating

**Windows:**
- If using PowerShell and you get an execution policy error, run:
  ```bash
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Try `cmd` (Command Prompt) instead of PowerShell

**Mac/Linux:**
- Ensure you're in the correct project directory
- Try: `source .venv/bin/activate`

### Issue: "Address already in use" (port 8501)

**Solution:**
- Another application is using port 8501
- Either stop the other application or run Streamlit on a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

### Issue: Database file (prompts.db) is not created

**Solution:**
- The app creates the database automatically on first run
- Ensure the project directory has write permissions
- Check that you're running the app from the correct directory
- If using Docker, ensure the volume is mounted correctly: `-v $(pwd):/app`

### Issue: Cannot access the application at localhost:8501

**Solution:**
- Make sure Streamlit is running (check terminal for the "Streamlit is running" message)
- Try opening `http://127.0.0.1:8501` instead
- Check if a firewall is blocking port 8501
- Restart the Streamlit application

### Issue: Login fails with default credentials

**Solution:**
- Default credentials are: username `admin`, password `admin`
- If you changed the credentials in `.env`, use those instead
- Ensure the `.env` file is in the project root directory
- Restart the Streamlit application after modifying `.env`

### Issue: Docker container won't start

**Solution:**
- Ensure Docker is running (Docker Desktop on Windows/Mac should be open)
- Check for port conflicts: another app may be using port 8501
- Try: `docker ps` to see running containers
- View logs: `docker logs <container-id>`
- Rebuild the image: `docker build -t prompt-library-database .`

### Issue: Clipboard copy feature not working

**Solution:**
- The clipboard feature requires the `st-copy-to-clipboard` package
- It's already in `requirements.txt`, so it should be installed
- Some browsers may block clipboard access—this is a browser security feature
- Restart the application and try again

### Need More Help?

- Check the Streamlit documentation: [https://docs.streamlit.io](https://docs.streamlit.io)
- Review the main application file (`app.py`) for configuration details
- Ensure all dependencies from `requirements.txt` are installed: `pip list`
