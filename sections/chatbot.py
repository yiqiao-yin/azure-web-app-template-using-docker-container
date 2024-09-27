def run_chatbot():
    import os
    from datetime import datetime

    import streamlit as st
    from dotenv import load_dotenv
    from openai import OpenAI

    # Load environment variables from .env file
    load_dotenv()

    # Access the API key from environment variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    class ChatBot:
        def __init__(self):
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.history = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]

        def generate_response(self, prompt: str) -> str:
            self.history.append({"role": "user", "content": prompt})

            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # NOTE: feel free to change it to gpt-4, or gpt-4o
                messages=self.history,
            )

            response = completion.choices[0].message.content
            self.history.append({"role": "assistant", "content": response})

            return response

        def get_history(self) -> list:
            return self.history

    # Credit: Time
    def current_year():
        now = datetime.now()
        return now.year

    # st.set_page_config(layout="wide")
    st.title("Just chat! 🤖")

    with st.sidebar:
        with st.expander("Instruction Manual"):
            st.markdown(
                """
                ## OpenAI GPT-4 🤖 Chatbot
                This Streamlit app allows you to chat with GPT-4 model. The model GPT-4o is deprecated due to high cost and will only be turned on for special occasions.
                ### How to Use:
                1. **Input**: Type your prompt into the chat input box labeled "What is up?".
                2. **Response**: The app will display a response from GPT-4.
                3. **Chat History**: Previous conversations will be shown on the app.
                ### Credits:
                - **Developer**: [Yiqiao Yin](https://www.y-yin.io/) | [App URL](https://huggingface.co/spaces/eagle0504/gpt-4o-demo) | [LinkedIn](https://www.linkedin.com/in/yiqiaoyin/) | [YouTube](https://youtube.com/YiqiaoYin/)
                Enjoy chatting with OpenAI's GPT-4 model!
            """
            )

        # Example:
        with st.expander("Examples"):
            st.success("Example: Explain what is supervised learning.")
            st.success("Example: What is large language model?")
            st.success("Example: How to conduct an AI experiment?")
            st.success(
                "Example: Write a tensorflow flow code with a 3-layer neural network model."
            )

        # Add a button to clear the session state
        if st.button("Clear Session"):
            st.session_state.messages = []
            st.experimental_rerun()

        # Credit:
        current_year = current_year()  # This will print the current year
        st.markdown(
            f"""
                <h6 style='text-align: left;'>Copyright © 2010-{current_year} Present Yiqiao Yin</h6>
            """,
            unsafe_allow_html=True,
        )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Ensure messages are a list of dictionaries
    if not isinstance(st.session_state.messages, list):
        st.session_state.messages = []
    if not all(isinstance(msg, dict) for msg in st.session_state.messages):
        st.session_state.messages = []

    # Display chat messages from history on app rerun, excluding system messages
    for message in st.session_state.messages:
        if message["role"] != "system":  # Skip displaying system messages
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(
        "😉 Ask any question or feel free to use the examples provided in the left sidebar."
    ):

        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)

        # Add a system message to the chat history, but don't display it
        st.session_state.messages.append(
            {
                "role": "system",
                "content": f"You are a helpful assistant. Year now is {current_year}",
            }
        )

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # API Call
        bot = ChatBot()
        bot.history = st.session_state.messages.copy()  # Update history from messages
        response = bot.generate_response(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
