import streamlit as st
import openai
import os
from fpdf import FPDF
import zipfile
from PIL import Image

st.set_page_config(page_title="AIdoino", page_icon="🤖", layout="centered")

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <img src="https://raw.githubusercontent.com/NikolaElectronics/ai-do-ino-deploy/main/logo.png"
             style="width: 280px; max-width: 100%; height: auto; margin-bottom: 1rem;">
        <h1 style="font-size: 3.5rem; margin: 0;">AIdoino</h1>
        <p style="font-size: 1.4rem; color: #aaa; margin-top: 0.3rem;">
            Your AI-based Arduino Assistant
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

language = st.selectbox("🌍 Choose explanation language:", [
    "English", "Română", "Español", "Français", "Deutsch", "Português",
    "हिन्दी (Hindi)", "বাংলা (Bengali)", "العربية (Arabic)", "中文 (Chinese)",
    "日本語 (Japanese)", "한국어 (Korean)", "ไทย (Thai)", "Türkçe", "Italiano", "Русский (Russian)"
])

lang_map = {
    "English": "en",
    "Română": "ro",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Português": "pt",
    "हिन्दी (Hindi)": "hi",
    "বাংলা (Bengali)": "bn",
    "العربية (Arabic)": "ar",
    "中文 (Chinese)": "zh",
    "日本語 (Japanese)": "ja",
    "한국어 (Korean)": "ko",
    "ไทย (Thai)": "th",
    "Türkçe": "tr",
    "Italiano": "it",
    "Русский (Russian)": "ru"
}
lang_code = lang_map.get(language, "en")

board = st.selectbox("🧰 Select your development board:", [
    "Arduino Uno", "Arduino Uno R4 (Renesas)", "Arduino Nano", "ESP32", "ESP8266", "Raspberry Pi"
])

board_map = {
    "Arduino Uno": "uno",
    "Arduino Uno R4 (Renesas)": "uno_r4",
    "Arduino Nano": "nano",
    "ESP32": "esp32",
    "ESP8266": "esp8266",
    "Raspberry Pi": "raspberrypi"
}
board_code = board_map.get(board, "uno")

allow_ac_control = st.checkbox("⚡ I want to control high-voltage (AC) devices using relays or optocouplers")

user_prompt = st.text_area("💬 Describe your microcontroller project:", placeholder="Ex: Control a 220V light bulb using a relay")

if st.button("⚡ Generate Code"):
    if "generation_count" not in st.session_state:
        st.session_state.generation_count = 0

    MAX_FREE_GENERATIONS = 3
    if st.session_state.generation_count >= MAX_FREE_GENERATIONS:
        st.warning("🛘 You've reached the free generation limit.")
        st.info("Support AIdoino to unlock unlimited access 💡")
        st.stop()

    if not user_prompt.strip():
        st.warning("Please describe your project before generating code.")
    else:
        with st.spinner("Generating code..."):
            try:
                openai.api_key = os.getenv("OPENAI_API_KEY")

                system_prompt = (
                    "You are an embedded systems engineer with 15+ years of experience working with "
                    "Arduino (including Uno R4 with Renesas), ESP32, ESP8266, and Raspberry Pi. "
                    "You write safe, well-commented code for microcontroller projects using best practices. "
                    "Always avoid direct control of AC voltage. Use relays or optocouplers instead. "
                    "Adapt the code to the board specified. If the board is Raspberry Pi, use Python. "
                    "Otherwise, use C++ (Arduino-style)."
                )

                if not allow_ac_control:
                    system_prompt += " Never generate code for AC control unless explicitly allowed."

                full_prompt = (
                    f"Board: {board}\n"
                    f"Task: {user_prompt}\n"
                    f"Language: {language}\n"
                    f"Generate the embedded code with setup() and loop() (if Arduino/ESP).\n"
                    f"Include inline comments and a short explanation in {language}.\n"
                    "Avoid English unless explicitly selected."
                )

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ]
                )

                st.session_state.generation_count += 1
                generated_code = response.choices[0].message["content"]
                st.success("✅ Code generated successfully!")
                st.code(generated_code, language="cpp")

                code_file = "arduino_sketch.ino"
                doc_file = "project_description.md"
                pdf_file = "high_voltage_confirmation.pdf"
                zip_file = "aidoino_project_bundle.zip"

                with open(code_file, "w") as f:
                    f.write(generated_code)

                project_doc = (
                    "# AIdoino Project\n\n"
                    f"**Board:** {board}\n"
                    f"**AC control enabled:** {'Yes' if allow_ac_control else 'No'}\n\n"
                    "---\n\n"
                    "**User Prompt:**\n"
                    f"{user_prompt}\n\n"
                    "---\n\n"
                    "**Generated Code:**\n"
                    "```\n"
                    f"{generated_code}\n"
                    "```"
                )
                with open(doc_file, "w") as f:
                    f.write(project_doc)

                if allow_ac_control:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=(
                        "AIdoino - High Voltage Responsibility Confirmation\n\n"
                        f"Board selected: {board}\n"
                        f"User prompt: {user_prompt}\n"
                        "AC Control Option: ENABLED\n\n"
                        "By generating this code, the user confirms they understand that working with high-voltage (AC) "
                      