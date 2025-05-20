import streamlit as st
import openai
import os
from fpdf import FPDF
import zipfile

# Page config
st.set_page_config(page_title="AI-do-ino", page_icon="🤖")

# UI
st.title("🤖 AI-do-ino - Let AI do Arduino")
st.markdown("Generate professional, safe Arduino and microcontroller code with the help of AI")

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
                zip_file = "ai-do-ino_project_bundle.zip"

                # Save .ino
                with open(code_file, "w") as f:
                    f.write(generated_code)

                # Save .md
                project_doc = f"""# AI-do-ino Project

**Board:** {board}  
**AC control enabled:** {'Yes' if allow_ac_control else 'No'}

---

**User Prompt:**  
{user_prompt}

---

**Generated Code:**  
