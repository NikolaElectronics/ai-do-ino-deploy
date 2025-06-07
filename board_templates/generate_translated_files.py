translations = {
    "en": {
        "tech_specs": "Technical Specifications",
        "label_microcontroller": "Microcontroller",
        "label_clock": "Clock speed",
        "label_voltage": "Operating voltage",
        "label_pins": "I/O Pins",
        "label_usb": "USB interface",
        "usage": "Usage",
        "usage_phrase": "is suitable for beginner and intermediate Arduino projects"
    },
    "ro": {
        "tech_specs": "Specificații Tehnice",
        "label_microcontroller": "Microcontroler",
        "label_clock": "Frecvență de ceas",
        "label_voltage": "Tensiune de operare",
        "label_pins": "Pinuri I/O",
        "label_usb": "Interfață USB",
        "usage": "Utilizare",
        "usage_phrase": "este potrivită pentru proiecte Arduino de nivel începător și mediu"
    },
    "hi": {
        "tech_specs": "तकनीकी विनिर्देश",
        "label_microcontroller": "माइक्रोकंट्रोलर",
        "label_clock": "क्लॉक स्पीड",
        "label_voltage": "ऑपरेटिंग वोल्टेज",
        "label_pins": "I/O पिन",
        "label_usb": "USB इंटरफेस",
        "usage": "उपयोग",
        "usage_phrase": "शुरुआती और मध्यम स्तर की Arduino परियोजनाओं के लिए उपयुक्त है"
    }
}

def generate_board_info(board_data, lang_code):
    with open("board_info_template.md", "r", encoding="utf-8") as f:
        template = f.read()

    t = translations.get(lang_code, translations["en"])  # fallback to English

    # Înlocuiește traducerile
    for key, value in t.items():
        template = template.replace(f"{{{{{key}}}}}", value)

    # Înlocuiește datele tehnice
    for key, value in board_data.items():
        template = template.replace(f"{{{{{key}}}}}", value)

    return template

board_data = {
    "board_name": "Arduino Uno",
    "microcontroller": "ATmega328P",
    "clock_speed": "16 MHz",
    "voltage": "5V",
    "pins": "14 digital / 6 analog",
    "usb": "Type-B USB"
}

# Generează fișiere în 3 limbi
for lang in ["en", "ro", "hi"]:
    result = generate_board_info(board_data, lang)
    with open(f"board_info_{lang}.md", "w", encoding="utf-8") as f:
        f.write(result)
