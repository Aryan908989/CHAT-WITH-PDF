# PDF Chat App with Qdrant and Groq

A Retrieval-Augmented Generation (RAG) application that allows users to interact with PDF documents and get answers to their questions using AI.

The application uses **Qdrant** for vector storage and retrieval and **Groq** to generate responses using a large language model (LLM).

## 🚀 Features

- 📄 Ask questions about PDF documents.
- 🔍 Retrieve relevant information from documents using vector search.
- 🧠 Generate AI-powered answers using Groq.
- 🗄️ Store and search document embeddings using Qdrant.
- 🔐 Manage API keys through environment variables.
- ⚡ Built with Python and `uv` for dependency management.

## 🛠️ Tech Stack

- **Python** — Application logic
- **Qdrant** — Vector database for semantic search
- **Groq API** — AI-powered answer generation
- **RAG** — Retrieval-Augmented Generation
- **uv** — Python package and project management

## 📁 Project Structure

```text
pdf-chat/
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
│
├── app.py
│
├── rag/
│   ├── __init__.py
│   ├── config.py
│   ├── loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── store.py
│   └── generate.py
│
├── data/
│   └── uploads/
│       └── .gitkeep
│
├── qdrant_data/
│   └── .gitkeep
│
└── tests/
    └── test_chunker.py
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

Replace the placeholders with your actual repository URL and project folder name.

### 2. Install uv

If you don't already have `uv` installed, follow the official installation instructions:

https://docs.astral.sh/uv/getting-started/installation/

### 3. Install dependencies

Run this command from the project root:

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file by copying `.env.example`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add your required API keys and configuration values to `.env`. For example:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

Use the exact variable names expected by your application. If you're using a local Qdrant instance, your configuration may differ.

**Important:** Never upload your actual `.env` file or API keys to GitHub.

### 5. Run the application

If `app.py` is your application entry point, run:

```bash
uv run python app.py
```

Follow the instructions displayed by the application.

## 🔄 How It Works

1. **PDF Input:** The application receives a PDF document.
2. **Text Extraction:** Text is extracted from the document.
3. **Chunking:** The extracted text is divided into smaller chunks.
4. **Embedding:** Text chunks are converted into vector embeddings.
5. **Vector Storage:** Embeddings are stored in Qdrant.
6. **Retrieval:** When a user asks a question, relevant chunks are retrieved using vector search.
7. **Answer Generation:** The retrieved context is sent to Groq to generate a relevant answer.

## 🔑 Required API Services

- **Groq:** https://console.groq.com/
- **Qdrant Cloud:** https://cloud.qdrant.io/

You may need API keys and a configured Qdrant collection, depending on your implementation.

## 🧪 Testing

Run your project's tests with:

```bash
uv run pytest
```

This assumes that `pytest` is installed and your tests are written for it.

## 🔒 Security

- Store API keys in environment variables.
- Keep `.env` out of version control.
- Never expose database credentials in source code.
- Use appropriate access controls for your Qdrant database.

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## 📜 License

Choose an appropriate open-source license before distributing this project. If you haven't selected one, the project is currently shared without an explicitly specified license.

---

**Built with Python, Qdrant, Groq, and RAG.**
