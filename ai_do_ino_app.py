import streamlit as st
import openai
import os
from fpdf import FPDF
import zipfile
from PIL import Image

# Load and display logo
st.set_page_config(page_title="AIdoino", page_icon="🤖", layout="centered")
# Centered logo + title
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <img src="https://raw.githubusercontent.com/NikolaElectronics/ai-do-ino-deploy/main/logo.png" width="220">
        <h1 style="font-size: 3.2rem; margin-bottom: 0.4rem; margin-top: 1rem;">AIdoino</h1>
        <p style="font-size: 1.35rem; color: #bbb;">Your AI-based Arduino Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)




with st.expander("📌 Example prompts"):
    st.markdown(
        "- Blink an LED every second\n"
        "- Control a 220V bulb using a relay\n"
        "- Send temperature data to the cloud with ESP32"
    )

board = st.selectbox(
    "🧰 Select your development board:",
    ["Arduino Uno", "Arduino Uno R4 (Renesas)", "Arduino Nano", "ESP32", "ESP8266", "Raspberry Pi"]
)

allow_ac_control = st.checkbox("⚡ I want to control high-voltage (AC) devices using relays or optocouplers")

user_prompt = st.text_area(
    "💬 Describe your microcontroller project:",
    placeholder="Ex: Control a 220V light bulb using a relay"
)

if st.button("⚡ Generate Code"):
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
                    "Generate the appropriate embedded code with setup() and loop() (if Arduino/ESP). "
                    "Comment each major step clearly."
                )

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ]
                )

                generated_code = response.choices[0].message["content"]
                st.success("✅ Code generated successfully!")
                st.code(generated_code, language="cpp")

                # === Create files ===
                code_file = "arduino_sketch.ino"
                doc_file = "project_description.md"
                pdf_file = "high_voltage_confirmation.pdf"
                zip_file = "aidoino_project_bundle.zip"

                # Save .ino
                with open(code_file, "w") as f:
                    f.write(generated_code)

                # Save .md (project doc)
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

                # Create PDF confirmation if AC is enabled
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
                        "components requires proper safety precautions, including the use of relays, optocouplers, and isolation.\n\n"
                        "The user takes full responsibility for the application and consequences of the code generated."
                    ))
                    pdf.output(pdf_file)

                # Create ZIP
                with zipfile.ZipFile(zip_file, "w") as zipf:
                    zipf.write(code_file)
                    zipf.write(doc_file)
                    if allow_ac_control:
                        zipf.write(pdf_file)

                # Download ZIP
                with open(zip_file, "rb") as f:
                    st.download_button("📦 Download project ZIP", f, file_name=zip_file)

            except Exception as e:
                st.error(f"❌ Error: {e}")
