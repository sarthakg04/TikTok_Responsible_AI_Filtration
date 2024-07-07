# TikTok_Responsible_AI_Filtration

This guide provides step-by-step instructions to set up and run a Python application using the Anthropic SDK.

## Prerequisites

- Python 3.7+
- An API key from Anthropic

## Project Structure

Ensure your project directory has the following structure:

your-project

    compute_engine.py

    requirements.txt

    .env

    venv


### `.env` File

Your `.env` file should contain your API key:

ANTHROPIC_API_KEY='your-api-key-here'


## Step 1: Create and Activate a Virtual Environment

1. Open your terminal or command prompt.
2. Navigate to your project directory.

   ```sh
   cd path/to/your/project

Create a virtual environment.

    python -m venv venv

Activate the virtual environment.

    source claude-env/bin/activate

## Step 2: Install Dependencies

    pip install -r requirements.txt

## Step 3: Run the Python Script

    python compute_engine.py


