# soft-engg-project-sep-2024-se-sep-8

## Table of Contents
- [Introduction](#introduction)
- [Setup Instructions](#setup-instructions)
  - [Cloning the Repository](#cloning-the-repository)
  - [Creating a Virtual Environment](#creating-a-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Git Instructions](#git-instructions)
  - [Pulling the Repository](#pulling-the-repository)
  - [Editing Files](#editing-files)
  - [Committing Changes](#committing-changes)
  - [Pushing Changes](#pushing-changes)
  - [Integrating Changes from Branch to Main](#integrating-changes-from-branch-to-main)

## Introduction

This web application is designed to help instructors manage and track student project progress throughout the semester, especially in larger classes. The system allows projects to be broken down into clear milestones and integrates with GitHub to visualize commit histories for real-time coding insights. Leveraging Generative AI, the application also analyzes documents like proposals and reports to assist in evaluation. A centralized dashboard provides an overview of all teams, customizable milestones, and AI-powered progress predictions, making it a comprehensive tool for academic project management.

## Setup Instructions

### Cloning the Repository

1. Open terminal (VS recommended).
2. Navigate to the directory where to clone the repository:
   ```bash
   cd path/to/your/directory
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/the-y9/soft-engg-project-sep-2024-se-sep-8.git
   ```
4. Navigate into the cloned directory:
   ```bash
   cd soft-engg-project-sep-2024-se-sep-8
   ```

### Creating a Virtual Environment

1. Create a virtual environment named `.venv`:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - **On Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

### Installing Dependencies

Once the virtual environment is activated, install the required dependencies by running:
```bash
pip install -r requirements.txt
```
*Once the dependencies are installed from the requirements.txt file, there is a possibility that an error in loading a spacy model (en_core_web_sm) surfaces.
To handle it run the following command in the virtual environment:
```bash
python -m spacy download en_core_web_sm
```

## Git Instructions

### Pulling the Repository

To pull the latest changes from the remote repository, run:
```bash
git pull origin main
```
*Replace `main` with the name of branch if pulling from a different branch.*

### Editing Files

Edit files and update `requirements.txt`.
```
pip freeze > requirements.txt
```

### Committing Changes

After making changes, stage and commit them:

1. To stage all:
   ```
   git add .
   ```
   Or to stage specific files, replace . with the filename:
   ```
   git add filename
   ```

3. Commit changes with a message:
   ```
   git commit -m "commit message"
   ```

### Pushing Changes

To create a new branch  (e.g., `database_setup`)
```
git checkout -b database_setup
```
To push changes to a specific branch
```bash
git push origin database_setup
```
To push changes to the main branch
```bash
git push origin main
```

### Integrating Changes from Branch to Main

To integrate changes from branch (e.g., `database_setup`) to the main branch

1. Switch to the main branch:
   ```bash
   git checkout main
   ```

2. Pull the latest changes from the remote main branch:
   ```bash
   git pull origin main
   ```

3. Merge branch into the main branch:
   ```bash
   git merge database_setup
   ```

4. Push the updated main branch to the remote repository:
   ```bash
   git push origin main
   ```
