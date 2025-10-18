# 🤖 Chatbot that Answers Questions from a PDF  

## 📘 Project Overview  
This project is an **AI-powered chatbot** that can answer questions directly from a **PDF file**.  

Here’s what it does:  
- The user uploads a PDF.  
- The system extracts and stores its text.  
- The user asks a question in the chat.  
- The chatbot searches for the most relevant paragraph or context and gives an intelligent answer.  

### 🧠 Key Technologies  
- **FastAPI** → Backend framework (Python)  
- **Supabase** → Database & cloud storage  
- **OpenAI / Sentence Transformers** → Understand and compare text meaning  
- **HTML + JavaScript (Frontend)** → File upload and chat interface  

---

## ⚙️ Project Workflow  

### 1️⃣ Frontend (User Interface)
- A simple web page where the user can:
  - Upload a PDF  
  - Ask questions in chat  
- Built using **HTML**, **CSS**, and **JavaScript (Fetch API)**  

### 2️⃣ Backend (FastAPI Server)
- Handles logic for file upload and chat response  
- Two main routes:
  - `/upload` → Receives PDF, extracts text using **pdfplumber**, and stores in **Supabase**  
  - `/chat` → Receives a question, fetches relevant chunks from the database, and uses AI to generate an answer  

### 3️⃣ Database (Supabase)
- Stores:
  - Extracted text chunks  
  - (Optional) Embeddings for semantic similarity search  
- Acts as a cloud-based **PostgreSQL** database  

### 4️⃣ AI Layer
- Uses **Sentence Transformers** or **OpenAI Embeddings** to understand meaning  
- When a user asks a question:
  - Finds the best-matching chunks from Supabase  
  - Sends them to the AI model to generate an accurate answer  

---

## 🗂 Folder Structure  

```
CHATBOT_NEW/
│
├── app/
│   ├── main.py                 # Starts the FastAPI app
│   ├── core/
│   │   └── database.py         # Connects to Supabase
│   ├── routers/
│   │   ├── upload_router.py    # Handles PDF upload route
│   │   └── chat_router.py      # Handles chat logic
│   └── utils/
│       └── pdf_utils.py        # Extracts text from PDF
│
├── frontend/
│   ├── index.html              # Frontend page
│   ├── style.css               # Styling
│   └── script.js               # Fetch API and user interaction
│
├── .env                        # Contains secrets (SUPABASE_URL, SUPABASE_KEY)
├── requirements.txt             # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Ignore .venv and sensitive files
```

---

## 📦 Libraries & Tools  

### 🐍 Python Libraries  
Add these to `requirements.txt`:
```
fastapi
uvicorn
pdfplumber
python-dotenv
supabase
numpy
sentence-transformers
openai
python-multipart
```

### 💻 Frontend Tools  
- HTML  
- CSS  
- JavaScript (Fetch API)  
- Bootstrap *(optional)* for styling  

### 🧰 Other Tools  
- **Supabase** → Database  
- **GitHub** → Version control  
- **VS Code** → Code editor  

---

## 🚀 Working Methodology  

### 🧩 Step 1: Setup the Environment  

1. **Install Python (latest version)**  
2. Create and activate virtual environment:  
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Create `.env` file** with the following:
   ```
   SUPABASE_URL=<your_supabase_url>
   SUPABASE_KEY=<your_supabase_key>
   ```

---

### 🌐 Step 2: Set Up GitHub Repository  

1. Create a new repo named **chatbot_new**  
2. Clone it:  
   ```bash
   git clone https://github.com/<your-team>/chatbot_new.git
   ```
3. Create two branches:  
   - `main` → Final stable code  
   - `dev` → All members commit here first  
4. Workflow:  
   ```bash
   git checkout dev
   git add .
   git commit -m "Added upload route"
   git push origin dev
   ```
5. **Murtuza** reviews pull requests and merges `dev → main`  

---

### 🗄 Step 3: Supabase Setup  

1. Go to [https://supabase.com](https://supabase.com)  
2. Create a new project  
3. In **Table Editor**, create a new table named **documents** with columns:
   | Column | Type  | Description |
   |--------|-------|-------------|
   | id | UUID (Primary Key) | Unique ID |
   | content | Text | Extracted text chunks |
   | embedding | Vector (optional) | For semantic search |

4. Copy your **Supabase Project API URL** and **Anon Key**  
5. Paste them into your `.env` file  

---

## 🎯 End Goal  

✅ User uploads a PDF file  
✅ Backend extracts and stores the text  
✅ User types a question → chatbot responds intelligently  
✅ All progress tracked via GitHub branches  

---

## 👥 Team Members  

- **Musaddiq**  
- **Sabera**  
- **Sidra**  
- **Murtuza**  

**Project Mentor:** *Miran Ahmed*  

---

## 🧪 Testing  

- Run the app locally:  
  ```bash
  uvicorn app.main:app --reload
  ```
- Open your browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
  - Use Swagger UI to test `/upload` and `/chat` APIs.  

---

## 🧭 Final Notes  

- Keep `.env` and `.venv` **excluded** from commits (`.gitignore` helps).  
- Always commit to **dev** branch first.  
- Regularly pull the latest updates before pushing changes.  
- Test endpoints before merging to main.  
- Once the system works end-to-end:
  - User uploads → Text stored → Chatbot answers questions ✅  

---

## 💡 Future Improvements  
- Add user authentication  
- Support multiple PDF uploads  
- Improve UI/UX with React or Streamlit  
- Add context memory for better chat flow  

---

**🧾 Author & Contributors**  
Team Members: **Musaddiq**, **Sabera**, **Sidra**, **Murtuza** 
