# Haitian Creole Dictionary Chatbot

This project is a bilingual Haitian Creole-English dictionary chatbot. 
It provides definitions, translations, and optional image lookups for words and phrases. 
The chatbot is designed to assist users in understanding Haitian Creole and English vocabulary interactively.

## Features

- **Translation**: Translates between Haitian Creole and English using the `facebook/nllb-200-distilled-600M` model.
- **Definitions**: Retrieves word definitions from a preloaded Haitian Creole dictionary or WordNet for English words.
- **Image Lookup**: Optionally fetches images for nouns to enhance understanding.
- **Interactive Chatbot**: A user-friendly chatbot interface built with React and TypeScript.
- **API Integration**: A FastAPI backend that processes user queries and serves the frontend.

---

## Project Structure

### **Backend**
Located in the `backend/` directory:
- **`main.py`**: The entry point for the FastAPI server.
- **`chatter.py`**: Handles chatbot logic, including query parsing and response formatting.
- **`back_translation.py`**: Manages translation pipelines using the NLLB model.
- **`definition.py`**: Retrieves word definitions from the dictionary or WordNet.
- **`image_lookup.py`**: Fetches images for nouns using external APIs.
- **`models.py`**: Defines Pydantic models for API requests and responses.
- **`ml_models/translation.py`**: Implements the translation logic.

### **Frontend**
Located in the `frontend/` directory:
- **`src/App.tsx`**: The main React component for the chatbot interface.
- **`src/index.css`**: Global styles using Tailwind CSS.
- **`vite.config.ts`**: Configuration for the Vite build tool.
- **`public/`**: Static assets for the frontend.

### **Resources**
Located in the `resources/` directory:
- **`haitian_creole_monolingual_dictionary.json`**: A JSON file containing Haitian Creole words and their definitions.

---

## Installation

### Prerequisites
- Docker
- Node.js (for local frontend development)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd creole_dictionary
   ```

2. Build and run the Docker container:
   ```bash
   ./runner.sh
   ```

3. Access the application:
   - Frontend: [http://localhost:8000](http://localhost:8000)
   - API: [http://localhost:8000/api/chat](http://localhost:8000/api/chat)

---

## Usage

### Chatbot Interface
1. Enter a word or phrase in Haitian Creole or English.
2. The chatbot will respond with:
   - Definitions
   - Translations
   - Optional images (if enabled)

### API
- **Endpoint**: `/api/chat`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "message": "pen"
  }
  ```
- **Response**:
  ```json
  {
    "reply": "Mo 'pen' vle di 'pen'. (Sous: local dictionary)",
    "definitions": [
      {
        "word": "pen",
        "definition": "pen",
        "source": "local dictionary",
        "image_url": "https://example.com/image.jpg"
      }
    ]
  }
  ```

---

## Tools and Libraries

### Backend
- **FastAPI**: For building the API.
- **Transformers**: For using the NLLB translation model.
- **NLTK**: For retrieving English definitions from WordNet.

### Frontend
- **React**: For building the chatbot interface.
- **Vite**: For fast development and build processes.
- **Tailwind CSS**: For styling.

---

## Future Improvements
- **Language Detection**: Automatically detect the input language.
- **Context Awareness**: Support multi-turn conversations.
- **Enhanced Error Handling**: Provide more descriptive error messages.
- **Accessibility**: Improve ARIA support for better accessibility.
- **And Many More**