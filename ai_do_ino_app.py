import streamlit as st
import openai
import os

# Set page configuration
st.set_page_config(page_title="AI-do-ino", page_icon="🤖")

# Title and description
st.title("🤖 AI-do-ino - Let AI do Arduino")
st.markdown("Build faster with the power of AI + Arduino")

# Example prompts
with st.expander("📌 Example prompts"):
    st.markdown("- Blink an LED every second\n- Turn on LED when motion is detected")

# Board selection
board = st.selectbox(
    "🧰 Select your development board:",
    ["Arduino Uno", "Arduino Nano", "Arduino Mega", "Arduino Leonardo"]
)

# User input
user_prompt = st.text_area(
    "💬 Describe your Arduino project:",
    placeholder="Turn on lightbulb"
)

# Generate code button
if st.button("⚡ Generate Code"):
    if not user_prompt.strip():
        st.warning("Please enter a project description before generating code.")
    else:
        with st.spinner("Generating code..."):
            try:
                # Load API key from environment variable
                openai.api_key = os.getenv("OPENAI_API_KEY")

                # GPT prompt
                prompt = (
                    f"Write complete and well-commented Arduino C++ code for a {board}.\n"
                    f"Task: {user_prompt}\n"
                    "Include setup() and loop(). Use clear and concise comments."
                )

                # OpenAI API call
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert in Arduino programming."},
                        {"role": "user", "content": prompt}
                    ]
                )

                # Display generated code
                generated_code = response.choices[0].message["content"]
                st.success("✅ Code generated successfully!")
                st.code(generated_code, language="cpp")

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
