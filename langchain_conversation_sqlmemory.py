import streamlit as st
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: pink;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Model and API Key")

model_list = ["GPT", "Gemini", "Anthropic"]
selected_model = st.sidebar.selectbox("Select LLM", model_list)

if selected_model == "GPT":
    gpt_models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-4-turbo", "gpt-4", "gpt-4o-mini", "gpt-4o"]  # Replace with actual GPT models
    selected_model_version = st.sidebar.selectbox("Select GPT Model", gpt_models)
elif selected_model == "Gemini":
    gemini_models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"]  # Replace with actual Gemini models
    selected_model_version = st.sidebar.selectbox("Select Gemini Model", gemini_models)
elif selected_model == "Anthropic":
    claude_models = ["claude-3-opus-20240229", "claude-3-5-sonnet-20240620", "claude-3-haiku-20240307"]  # Replace with actual Claude models
    selected_model_version = st.sidebar.selectbox("Select Claude Model", claude_models)

if selected_model:
    api_key = st.sidebar.text_input("Enter your API key", type="password")
    session_id = st.sidebar.text_input("Session id")

if selected_model and api_key and session_id:
    st.title("AI ChatBot")
    st.write(f"Conversation with session ID: {session_id}")
    st.chat_message("assistant").write("Hi, How may I help you?")
    
    @st.cache_resource
    def get_session_message_history_from_db(session_id):
        chat_message_history = SQLChatMessageHistory(
                                    session_id=session_id, 
                                    connection="sqlite:///chats_data/sqlite2.db"
                                )
        return chat_message_history.get_messages()
    
    messages = get_session_message_history_from_db(session_id)

    # Initialize session state for storing conversations if not already done
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
    
    # If the database contains the conversation for the session_id. Then display it.
    for message in messages:
        if isinstance(message, HumanMessage):
            st.chat_message("user").write(message.content)
        elif isinstance(message, AIMessage):
            st.chat_message("assistant").write(message.content)

    # Initialize session state for storing conversations if not already done
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

    # Retrieve or create a conversation for the current session_id
    if session_id not in st.session_state.conversations:
        st.session_state.conversations[session_id] = []

    # Display the conversation history for the current session_id
    for msg in st.session_state.conversations[session_id]:
        st.chat_message(msg["role"]).write(msg["content"])

    st.markdown("""
    <style>
    .stChatMessage.st-emotion-cache-1c7y2kd.eeusbqq4 {
        text-align: right;
        display: flex;
        flex-direction: row-reverse;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    @st.cache_resource
    def Initializing(selected_model, selected_model_version, api_key):
        from langchain_core.messages import SystemMessage
        from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
        from langchain_core.output_parsers import StrOutputParser

        ####################################################################################
        if selected_model == "GPT":
            from langchain_openai import ChatOpenAI
            chat_model = ChatOpenAI(api_key=api_key, model=selected_model_version)
        elif selected_model == "Gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            chat_model = ChatGoogleGenerativeAI(api_key=api_key, model=f"models/{selected_model_version}")
        elif selected_model == "Anthropic":
            from langchain_anthropic import ChatAnthropic
            chat_model = ChatAnthropic(api_key=api_key, model=selected_model_version)
        ###################################################################################### 

        chat_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an AI chatbot having a conversation with a human."),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ])

        output_parser = StrOutputParser()
        return chat_prompt_template, chat_model, output_parser

    def python_compiler(session_id, prompt):
        # Prompt Template, Chat Model, Output Parser
        chat_prompt_template, chat_model, output_parser = Initializing(selected_model, selected_model_version, api_key)

        # Chaining
        chain = chat_prompt_template | chat_model | output_parser

        # Initialize connection with database for the current session_id
        def get_session_message_history_from_db(session_id):
            chat_message_history = SQLChatMessageHistory(
                session_id=session_id, 
                connection="sqlite:///chats_data/sqlite2.db"
            )
            return chat_message_history

        # the RunnableWithMessageHistory class is used to handle the history of messages. 
        # It wraps a runnable and adds a history of messages to the input of the runnable. 
        # It uses a session history store to keep track of the messages for each session.
        conversation_chain = RunnableWithMessageHistory(
            chain, 
            get_session_message_history_from_db,
            input_messages_key="human_input", 
            history_messages_key="chat_history"
        )
        return conversation_chain

    prompt = st.chat_input("Ask a question...")
    if prompt:
        st.chat_message("user").write(prompt)
        st.session_state.conversations[session_id].append({"role": "user", "content": prompt})

        if prompt.lower() in ['bye', 'end']:
            st.chat_message("assistant").write("Goodbye!")
        else:
            conversation_chain= python_compiler(session_id, prompt)
            config = {"configurable": {"session_id": session_id}}
            input_prompt = {"human_input": prompt}
            answer = st.chat_message("assistant").write_stream(conversation_chain.stream(input_prompt,config))
            st.session_state.conversations[session_id].append({"role": "assistant", "content": answer})
