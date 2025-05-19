import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI-do-ino", page_icon="🤖")
st.title("🤖 AI-do-ino - Let AI do Arduino")
st.caption("Build faster with the power of AI + Arduino")

with st.expander("📌 Example prompts"):
    st.markdown("- Blink an LED every second\n- Turn on LED when motion is detected")

user_input = st.text_area("💬 Describe your Arduino project:")

if st.button("⚡ Generate Code"):
    if user_input.strip() == "":
        st.warning("Please enter a project description.")
    else:
        with st.spinner("Generating code..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You generate Arduino code from descriptions."},
                        {"role": "user", "content": f"Generate Arduino code for: {user_input}"}
                    ],
                    max_tokens=500,
                    temperature=0.4
                )
                code = response.choices[0].message.content.strip()
                st.code(code, language="cpp")
                st.text_input("📋 Click below and press Cmd+C to copy:", value=code, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
