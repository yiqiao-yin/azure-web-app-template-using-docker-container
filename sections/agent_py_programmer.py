def run_agent_py_programmer():
    import os
    import re
    from datetime import datetime
    from typing import Any, Optional

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
                {
                    "role": "system",
                    "content": "You are a helpful programmer especialy good for writing python code and functions. When user asks you to write py code or py functions or python functions, you always use standard format which includes type hints, docstring, and comments.",
                }
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

    def isolate_and_save_python_code(
        input_string: str, file_path: str
    ) -> Optional[str]:
        """
        Extracts Python code from a given input string and saves it to a file.

        This function looks for a block of text that is enclosed within triple backticks (```),
        specifically targeting blocks that start with ```python.

        Args:
            input_string (str): The input string containing the Python code block.
            file_path (str): The path where the extracted Python code will be saved.

        Returns:
            Optional[str]: The path to the saved file if the Python code block is found and saved, else None.
        """
        # Define the pattern to match the Python code block
        pattern = r"```python\s*(.*?)\s*```"

        # Search for the pattern in the input string
        match = re.search(pattern, input_string, re.DOTALL)

        if match:
            # Extract the Python code
            python_code = match.group(1)

            # Write the Python code to the specified file
            with open(file_path, "w") as file:
                file.write(python_code)

            return file_path
        else:
            # Return None if no Python code block is found
            return None

    import random
    import string

    def generate_random_string(length: int = 20) -> str:
        """
        Generate a random string of specified length consisting of letters and digits.

        :param length: The length of the random string to generate (default is 20).
        :return: A random string of the specified length.
        """
        # Define the character set: digits, lowercase, and uppercase letters
        characters = string.ascii_letters + string.digits
        # Generate a random string by selecting from the character set
        random_string = "".join(random.choice(characters) for _ in range(length))
        return random_string

    from datetime import datetime

    def get_current_date_string() -> str:
        """
        Generate a string representing the current date in YYYY_MM_DD format.

        :return: A string of the current date in the format 'YYYY_MM_DD'.
        """
        # Get the current date
        current_date = datetime.now()
        # Format the date as 'YYYY_MM_DD'
        date_string = current_date.strftime("%Y_%m_%d")
        return date_string

    def create_download_button(file_path: str) -> None:
        """
        Create a download button for the saved Python code file.

        :param file_path: The path to the Python file to be downloaded.
        """
        # Read the content of the saved file
        with open(file_path, "r") as file:
            file_content = file.read()

        # Create a download button in Streamlit
        st.download_button(
            label="Download Python Script",
            data=file_content,
            file_name=file_path.split("/")[-1],  # Use the file name from the path
            mime="text/plain",
        )

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
        current_year = datetime.now().year  # This will print the current year
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

        # Check if we need to save py script
        if "```python" in response:
            random_string = generate_random_string().lower()
            date_string = get_current_date_string()
            this_py_script_name = f"{date_string}_{random_string}.py"
            isolate_and_save_python_code(
                input_string=response, file_path=this_py_script_name
            )

            # Create a download button
            create_download_button(this_py_script_name)
