# Conversational ChatBot

This project implements an interactive AI Chatbot using Streamlit, integrated with multiple language models such as GPT, Gemini, and Anthropic. The chatbot supports dynamic conversation management, session-based chat history retrieval, and model-specific configurations, providing a robust and context-aware AI-driven conversational experience.

## Features

- **Multi-Model Support:** Easily switch between different AI models (GPT, Gemini, Anthropic) with specific versions for each, providing flexibility in chatbot capabilities.
- **Session-Based Chat History:** Chat history is stored and retrieved using an SQL database, maintaining conversation continuity across different sessions.
- **Customizable User Interface:** The interface is built using Streamlit, featuring a responsive design with custom CSS for an enhanced user experience.
- **Secure API Handling:** Securely input and store API keys and session IDs for accessing different language models.
- **Dynamic Response Generation:** Uses LangChain framework to manage conversation flow, ensuring intelligent and contextually relevant responses from the chatbot.

### Running the Application

1. **Start the Streamlit App**

    ```bash
    streamlit run app.py
    ```

2. **Interact with the Chatbot**

   - Open the app in your web browser using the link provided by Streamlit.
   - Select a language model and version from the sidebar.
   - Enter your API key and session ID.
   - Start interacting with the chatbot by typing questions or statements in the chat input box.

## File Structure

- `app.py`: Main application file containing the Streamlit app code.
- `chats_data/`: Directory containing the SQLite database for storing chat history.
- `README.md`: Project documentation.

## Customization

- **Models and Versions:** One can modify the list of available models and versions in the sidebar configuration to include additional AI models.
- **Database Connection:** Update the `SQLChatMessageHistory` connection if using a different database or connection method.

## Technologies Used
- **Python:** Core programming language.
- **Streamlit:** For building the interactive web application.
- **LangChain:** Provides suite of products that helps you build, run, and manage applications with large language models (LLMs).
- **SQLite:** For storing and retrieving chat history in a SQLite database for different session ids.

