import streamlit as st
import openai
import os
from fpdf import FPDF
import zipfile
from PIL import Image

# ✅ Aceasta trebuie să fie PRIMA comandă Streamlit
st.set_page_config(page_title="AIdoino", page_icon="🤖", layout="centered")

# ✅ DEBUG temporar (poate fi scos după test)
#st.text(f"user_password: {repr(user_password)} | current_password: {repr(current_password)}")

# 🧠 Titlu și logo
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

# ☕ Buy Me a Coffee button
st.markdown(
    """
    <div style="text-align: center; margin-top: 2rem;">
        <a href="https://buymeacoffee.com/nikolaelectronics" target="_blank" 
           style="
               display: inline-block;
               background-color: #FFDD00;
               color: black;
               font-weight: bold;
               padding: 12px 24px;
               text-decoration: none;
               border-radius: 8px;
               box-shadow: 0 4px 6px rgba(0,0,0,0.1);
               font-size: 16px;
               margin-top: 10px;
           ">
            ☕ Buy Me a Coffee
        </a>
        <p style="color: gray; font-size: 0.9rem; margin-top: 0.5rem;">
            Support AIdoino to keep it free and evolving ⚡
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
# 🔐 Autentificare Premium cu parolă
def get_current_password():
    try:
        with open("premium_password.txt", "r") as f:
            return f.read().strip()
    except:
        return None

current_password = get_current_password()
user_password = st.text_input("🔑 Enter Premium password:", type="password")
is_premium = (user_password == current_password)

# ↺ Feedback vizual pentru parolă
if user_password:
    if is_premium:
        st.success("✅ Premium unlocked!")
    else:
        st.error("❌ Incorrect password.")

# 🌍 Selectare limbă
language = st.selectbox("🌍 Choose explanation language:", [
    "English", "Română", "Español", "Français", "Deutsch", "Português",
    "हिंदी (Hindi)", "বাংলা (Bengali)", "العربية (Arabic)", "中文 (Chinese)",
    "日本語 (Japanese)", "한국어 (Korean)", "ไทย (Thai)", "Türkçe", "Italiano", "Русский (Russian)"
])
lang_map = {
    "English": "en", "Română": "ro", "Español": "es", "Français": "fr", "Deutsch": "de",
    "Português": "pt", "हिंदी (Hindi)": "hi", "বাংলা (Bengali)": "bn", "العربية (Arabic)": "ar",
    "中文 (Chinese)": "zh", "日本語 (Japanese)": "ja", "한국어 (Korean)": "ko", "ไทย (Thai)": "th",
    "Türkçe": "tr", "Italiano": "it", "Русский (Russian)": "ru"
}
lang_code = lang_map.get(language, "en")

# 🧰 Selectare placă
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

# ⚡ Opțiune AC
allow_ac_control = st.checkbox("⚡ I want to control high-voltage (AC) devices using relays or optocouplers")

# 🧠 Prompt de la utilizator
user_prompt = st.text_area("💬 Describe your microcontroller project:", placeholder="Ex: Control a 220V light bulb using a relay")

# 🔁 Buton generare
if st.button("⚡ Generate Code"):
    if "generation_count" not in st.session_state:
        st.session_state.generation_count = 0

    MAX_FREE_GENERATIONS = 3
    if not is_premium and st.session_state.generation_count >= MAX_FREE_GENERATIONS:
        st.warning("🚫 You've reached the free generation limit.")
        st.markdown('[☕ Support AIdoino on Buy Me a Coffee](https://buymeacoffee.com/nikolaelectronics)', unsafe_allow_html=True)
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

                # Scriere fișiere
                code_file = "arduino_sketch.ino"
                doc_file = "project_description.md"
                pdf_file = "high_voltage_confirmation.pdf"
                zip_file = "aidoino_project_bundle.zip"

                with open(code_file, "w") as f:
                    f.write(generated_code)

                with open(doc_file, "w") as f:
                    f.write(
                        f"# AIdoino Project\n\n**Board:** {board}\n**AC control enabled:** {'Yes' if allow_ac_control else 'No'}\n\n"
                        f"---\n\n**User Prompt:**\n{user_prompt}\n\n---\n\n**Generated Code:**\n```\n{generated_code}\n```"
                    )

                if allow_ac_control:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=(
                        f"AIdoino - High Voltage Responsibility Confirmation\n\nBoard selected: {board}\n"
                        f"User prompt: {user_prompt}\nAC Control Option: ENABLED\n\n"
                        "By generating this code, the user confirms they understand that working with high-voltage (AC) "
                        "components requires proper safety precautions, including the use of relays, optocouplers, and isolation."
                    ))
                    pdf.output(pdf_file)

                # 🧾 board_info.md în funcție de placă și limbă
                board_info_path = f"board_templates/{board_code}_{lang_code}.md"
                if not os.path.exists(board_info_path):
                    board_info_path = f"board_templates/{board_code}_en.md"

                with zipfile.ZipFile(zip_file, "w") as zipf:
                    zipf.write(code_file)
                    zipf.write(doc_file)
                    if allow_ac_control:
                        zipf.write(pdf_file)
                    zipf.write(board_info_path, "board_info.md")

                # 🔐 Dacă utilizatorul e deja premium, oferim direct descărcarea
                if is_premium:
                    with open(zip_file, "rb") as f:
                        st.download_button("📦 Download full project ZIP (Premium)", f, file_name=zip_file)
                else:
                    # 👁️ Cerem parola direct aici, jos
                    st.warning("🔒 Enter the Premium password to unlock ZIP export:")
                    user_password = st.text_input("🔑 Premium password:", type="password", key="premium_zip_input")
                    current_password = get_current_password()
                    if user_password == current_password:
                        with open(zip_file, "rb") as f:
                            st.success("✅ Password correct. Download unlocked!")
                            st.download_button("📦 Download full project ZIP (Premium)", f, file_name=zip_file)
                    elif user_password:
                        st.error("❌ Incorrect password.")


            except Exception as e:
                st.error(f"❌ Error: {e}")
