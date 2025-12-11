Streamlit Prompt Library ManagerThis is a simple, local-first application to manage a library of AI prompts. It's designed to be run from within a development environment like VS Code and uses an SQLite database for storage.🚀 How to Run1. PrerequisitesYou need to have Python 3.7+ installed.You need a terminal in VS Code (or any other terminal).2. SetupCreate a project folder and place the app.py file inside it.Open your terminal in the project folder and create a virtual environment (recommended):# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.venv\\Scripts\\activate
Install the required Python packages:pip install -r requirements.txt
3. Launch the ApplicationIn the same terminal (with the virtual environment activated), run the following command:streamlit run app.py
Your web browser should open with the application running, typically at http://localhost:8501.A new file called prompts.db will be created in your project folder the first time you run the app. This file is your database.📂 File Structureapp.py: The main Python script containing all the Streamlit application logic.prompts.db: An SQLite database file that stores your prompt library. It will be created automatically.requirements.txt: A list of Python dependencies needed for the project.README.md: This file.✨ FeaturesBrowse & Search: View all prompts in your library with a real-time search filter.Add New Prompts: Use a form to add new, structured prompts to your collection.Edit Prompts: Modify existing prompts to refine them over time.Delete Prompts: Remove prompts you no longer need.Local First & Robust: All data is stored locally in an SQLite database, providing faster and more reliable data handling than a plain text file.
