if st.button("⚡ Generate Code"):
    # Limita soft: 3 generații gratuite per sesiune
    if "generation_count" not in st.session_state:
        st.session_state.generation_count = 0

    MAX_FREE_GENERATIONS = 3

    if st.session_state.generation_count >= MAX_FREE_GENERATIONS:
        st.warning("🚫 You've reached the free generation limit.")
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

                # 🧠 Trimitere la OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ]
                )

                # ✅ Incrementăm contorul
                st.session_state.generation_count += 1

                # ✅ Afișăm codul
                generated_code = response.choices[0].message["content"]
                st.success("✅ Code generated successfully!")
                st.code(generated_code, language="cpp")

                # === Create files ===
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
                        "components requires proper safety precautions, including the use of relays, optocouplers, and isolation.\n\n"
                        "The user takes full responsibility for the application and consequences of the code generated."
                    ))
                    pdf.output(pdf_file)

                with zipfile.ZipFile(zip_file, "w") as zipf:
                    zipf.write(code_file)
                    zipf.write(doc_file)
                    if allow_ac_control:
                        zipf.write(pdf_file)

                with open(zip_file, "rb") as f:
                    st.download_button("📦 Download project ZIP", f, file_name=zip_file)

            except Exception as e:
                st.error(f"❌ Error: {e}")
