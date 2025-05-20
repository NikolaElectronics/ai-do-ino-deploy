import streamlit as st
import openai
import os

# Configurare pagină
st.set_page_config(page_title="AI-do-ino", page_icon="🤖")

# Titlu
st.title("🤖 AI-do-ino - Let AI do Arduino")
st.markdown("Generate clean Arduino code with the help of AI")

# Exprimare prompturi utile
with st.expander("📌 Example prompts"):
    st.markdown(
        "- Blink an LED every second\n"
        "- Control a fan with a temperature sensor\n"
        "- Turn on a light using a relay when motion is detected"
    )

# Selectare placă
board = st.selectbox(
    "🧰 Select your development board:",
    ["Arduino Uno", "Arduino Nano", "Arduino Mega", "Arduino Leonardo"]
)

# Atenționare AC
allow_ac_control = st.checkbox("⚡ I want to control high-voltage (AC) devices using relays or optocouplers")

# Prompt utilizator
user_prompt = st.text_area(
    "💬 Describe your Arduino project:",
    placeholder="Ex: Control a 220V light bulb using a relay"
)

# Buton de generare
if st.button("⚡ Generate Code"):
    if not user_prompt.strip():
        st.warning("Please describe your project before generating code.")
    else:
        with st.spinner("Generating code..."):
            try:
                openai.api_key = os.getenv("OPENAI_API_KEY")

                # Prompt AI sigur
                safety_notice = (
                    "You are an embedded systems expert. "
                    "Never suggest connecting Arduino directly to AC voltage. "
                    "Only control AC using relays or optocouplers. "
                )

                if not allow_ac_control:
                    safety_notice += "Avoid generating code for high-voltage (AC) control. Use only low-voltage components."

                full_prompt = (
                    f"{safety_notice}\n"
                    f"Board: {board}\n"
                    f"Task: {user_prompt}\n"
                    "Generate Arduino C++ code with setup() and loop(), plus clear comments."
                )

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional Arduino developer."},
                        {"role": "user", "content": full_prompt}
                    ]
                )

                generated_code = response.choices[0].message["content"]
                st.success("✅ Code generated successfully!")
                st.code(generated_code, language="cpp")

            except Exception as e:
                st.error(f"❌ Error: {e}")
