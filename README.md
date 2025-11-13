# 📄 PDF Document Assistant

An intelligent assistant application that lets you upload PDF files and ask questions about their content.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1-green.svg)

## 🌟 Features

### Core Features
- ✅ **PDF Upload**: Accepts only PDF files (max 10MB)
- ✅ **Text Extraction**: Reliable extraction using PyPDF2
- ✅ **Q&A System**: Smart answers using LLMs
- ✅ **Conversation History**: Maintains context across the chat
- ✅ **Modern UI**: Chat-like, user-friendly interface

### Additional Features
- 🎯 **Model Selection**: Choose between available LLMs
- 📊 **Text Statistics**: Page, word and character counts
- 👁️ **PDF Preview**: View the beginning of the extracted text
- 🗑️ **Clear Chat**: Reset conversation history with one click
- 💾 **Export History**: Download chat history as TXT or JSON

## 📋 Requirements

```bash
Python 3.8 or later
Google Gemini API Key (or configured provider key)
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/eskarasu/document-asistant.git
cd belge-asistani
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**How to get an API key**
1. Visit Google AI Studio (or your provider's console)
2. Sign in with your account
3. Create or get an API key and copy it
4. Put the key in your `.env` as shown above

## 💻 Usage

Start the app:

```bash
streamlit run app.py
```

Your browser should open `http://localhost:8501`.

### Step-by-step

1. **Upload a PDF**
   - Click the "Select PDF File" button in the left sidebar
   - Choose a PDF file (max 10MB)
   - Click the "Process PDF" button

2. **Ask Questions**
   - Type your question in the chat input at the bottom
   - Press Enter or click send
   - The assistant will answer based on the PDF content

3. **Manage Chat**
   - Scroll up to view the conversation history
   - Click "Clear Chat" to start fresh
   - Use the download buttons to save history as TXT or JSON

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Chat Example
![Chat](screenshots/chat-example.png)

## 🏗️ Project Structure

```
belge-asistani/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env.example           # API key template
├── README.md              # Original README (Turkish)
├── README_en.md           # English translation (this file)
├── .gitignore             # Git ignore rules
└── screenshots/           # Optional screenshots
```

## 🔧 Technical Details

### Technologies Used

- **Streamlit**: Web UI
- **LangChain**: LLM orchestration (if used)
- **Google Gemini** (or configured LLM provider)
- **PyPDF2**: PDF text extraction
- **python-dotenv**: Environment variable management

### Code Highlights

- Clean, modular functions
- Docstrings and error handling
- Session-state based UI state

## 🎓 Learning Outcomes

With this project you will learn:

1. **Streamlit basics and advanced usage**
   - File uploader, session state, chat UI, sidebar layout
2. **PDF processing**
   - PyPDF2 text extraction and file size validation
3. **LLM integration**
   - Prompt engineering, chat history handling
4. **Python best practices**
   - Modular code, docstrings, environment safety

## ⚠️ Notes

- **API Costs**: Using LLM APIs may incur costs — monitor usage.
- **File Size**: Large PDFs may cause token limits to be reached; a 10MB limit is recommended.
- **Security**: Never commit your `.env` to public repositories.

## 🐛 Troubleshooting

### "API Key not found"
- Ensure `.env` is in the project root and contains the key.
- Restart the application after adding the key.

### "PDF could not be read"
- Verify the PDF is not corrupted or password-protected.
- Try another PDF to isolate the issue.

### Slow responses
- Try a smaller model to reduce latency and cost.
- Reduce PDF size or ask more specific questions.

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/my-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Contact

Project maintainer - [@eskarasu](https://github.com/eskarasu)

Project: https://github.com/eskarasu/belge-asistani

---

If you found this project useful, please give it a star! ⭐
