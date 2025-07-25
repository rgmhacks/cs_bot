## macOS Setup (Detailed)

Follow these steps to download, configure, and run the RAG chatbot on macOS.

### 0. Verify and Choose Your Installer

Before you begin, check whether you have the `pip` or `pip3` installer:

```bash
pip --version || pip3 --version
```

- If `pip` is available, you may use it.
- Otherwise, use `pip3`.

> **Note:** In the commands below, we will use `pip3` consistently. If you prefer `pip`, replace `pip3` with `pip`.

### 1. Download the Code ZIP

1. Open your web browser and navigate to your GitHub repository page for the project.
2. In the top-left corner, click the green **Code** button.
3. From the dropdown, select **Download ZIP**.
4. Save the ZIP file (e.g., `rag-chatbot-main.zip`) to a folder such as `~/Downloads`.

### 2. Unzip the Downloaded Archive

1. Open **Finder** and go to the folder where you saved the ZIP (e.g., `~/Downloads`).
2. Double‑click `rag-chatbot-main.zip` to extract its contents.
3. A folder named `rag-chatbot-main` (or similar) will appear alongside the ZIP.

### 3. Open Terminal in the Project Directory

1. Open **Terminal** (press `⌘+Space`, type “Terminal”, and press Enter).
2. Navigate into the extracted folder:
   ```bash
   cd ~/Downloads/rag-chatbot-main
   ```

### 4. Install Python Dependencies

1. Change into the backend directory:
   ```bash
   cd backend
   ```
2. Upgrade your installer and install requirements:
   ```bash
   pip3 install --upgrade pip
   pip3 install -r requirements.txt
   ```

### 5. Create and Configure the `.env` File

1. From the project root (`rag-chatbot-main`), run:
   ```bash
   touch .env
   nano .env
   ```
2. In the editor, add your environment variables:
   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_ENVIRONMENT=your_pinecone_environment_here
   GOOGLE_API_KEY=your_google_api_key_here
   DB_URI=your_database_uri_here
   ```
3. Save and exit: `Ctrl+O`, `Enter`, then `Ctrl+X`.

### 6. Start the Server

1. In Terminal, ensure you’re in the `backend` folder (if not, `cd backend`).
2. Launch the FastAPI server on port 5000:
   ```bash
   python3 -m uvicorn main:app --reload --port 5000
   ```
   > If port 5000 is in use, you may choose an alternative like `5001` or `500000`.
3. You should see a startup log.:
   ```text
   http://localhost:5000
   ```

Your RAG chatbot backend is now running locally on macOS!

### 7. Frontend Setup

1. In a new Terminal window (or tab), navigate to the frontend folder:
   ```bash
   cd ~/Downloads/rag-chatbot-main/frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   - This will launch on port `3000` by default.
   - If port `3000` is already in use, start on an alternative port (e.g., `3001`):
     ```bash
     npm run dev -- --port 3001
     ```
4. Open your browser to:
   ```text
   http://localhost:3000
   ```
   (or `http://localhost:3001` if you used the alternate port)

Your full RAG chatbot (backend + frontend) is now running locally on macOS!  
Feel free to interact with the backend API at `/api/chat` or explore the frontend UI.
