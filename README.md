# Dental Presentation & Research Tool

This is a comprehensive AI-powered application for dental researchers, students, and professionals.
Built with **Streamlit** and **Google Gemini AI**.

## 🚀 Deployment (GitHub & Streamlit Cloud)
**The easiest way to share this app is via Streamlit Community Cloud:**

### Step 1: Push properly to GitHub
1.  **Create a New Repository** on GitHub (e.g. `dental-research-tool`).
2.  Open your terminal in this folder and run:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    # Replace the URL below with your actual GitHub repo URL!
    git remote add origin https://github.com/YOUR_USERNAME/dental-research-tool.git
    git push -u origin main
    ```

### Step 2: Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your GitHub repository (`dental-research-tool`).
4.  Set the **Main file path** to `app.py`.
5.  Click **"Deploy!"**.

### Step 3: Add Secrets (Important!)
Your API keys are safe in `.gitignore` and won't be uploaded. You must add them to Streamlit Cloud manually:
1.  In your deployed app dashboard, go to **Settings** > **Secrets**.
2.  Add your keys like this:
    ```toml
    GOOGLE_API_KEY = "your-gemini-key"
    OPENAI_API_KEY = "your-openai-key"
    ```
3.  Save, and the app will restart.

## 💻 Installation (Local)
1.  Install Python 3.10+.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    streamlit run app.py
    ```

## 🛠️ Features
*   **Presentation Generator**: Converts topics/PDFs to PowerPoint slides.
*   **Results Writer**: Generates "SPSS-like" results sections and APA tables.
*   **Social Media Tool**: Creates Instagram-ready JPG posts.
*   **Thesis & Study Aids**: Generates chapters, essays, and mind maps.

## ⚠️ Important
*   **API Key**: Requires a Google Gemini API Key.
*   **Privacy**: Do not upload patient data to public cloud deployments.
