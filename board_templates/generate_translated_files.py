import os

translations = {
    "en": {
        "tech_specs": "Technical specifications",
        "label_microcontroller": "Microcontroller",
        "label_clock": "Clock Speed",
        "label_voltage": "Operating Voltage",
        "label_pins": "Digital I/O Pins",
        "label_usb": "USB Interface",
        "usage": "Typical usage",
        "usage_phrase": "Ideal for learning, prototyping and hobby projects."
    },
    "ro": {
        "tech_specs": "Specificații tehnice",
        "label_microcontroller": "Microcontroler",
        "label_clock": "Frecvență ceas",
        "label_voltage": "Tensiune de operare",
        "label_pins": "Pini digitali I/O",
        "label_usb": "Interfață USB",
        "usage": "Utilizare tipică",
        "usage_phrase": "Ideal pentru învățare, prototipare și proiecte hobby."
    },
    "es": {"tech_specs": "Especificaciones técnicas", "label_microcontroller": "Microcontrolador", "label_clock": "Velocidad de reloj", "label_voltage": "Voltaje de operación", "label_pins": "Pines digitales I/O", "label_usb": "Interfaz USB", "usage": "Uso típico", "usage_phrase": "Ideal para aprender, hacer prototipos y proyectos de pasatiempo."},
    "fr": {"tech_specs": "Spécifications techniques", "label_microcontroller": "Microcontrôleur", "label_clock": "Fréquence d'horloge", "label_voltage": "Tension de fonctionnement", "label_pins": "Broches numériques I/O", "label_usb": "Interface USB", "usage": "Utilisation typique", "usage_phrase": "Idéal pour l'apprentissage, le prototypage et les projets amateurs."},
    "de": {"tech_specs": "Technische Daten", "label_microcontroller": "Mikrocontroller", "label_clock": "Taktfrequenz", "label_voltage": "Betriebsspannung", "label_pins": "Digitale I/O Pins", "label_usb": "USB-Schnittstelle", "usage": "Typische Verwendung", "usage_phrase": "Ideal zum Lernen, Prototyping und für Hobbyprojekte."},
    "nl": {"tech_specs": "Technische specificaties", "label_microcontroller": "Microcontroller", "label_clock": "Kloksnelheid", "label_voltage": "Bedrijfsspanning", "label_pins": "Digitale I/O-pinnen", "label_usb": "USB-interface", "usage": "Typisch gebruik", "usage_phrase": "Ideaal voor leren, prototyping en hobbyprojecten."},
    "pt": {"tech_specs": "Especificações técnicas", "label_microcontroller": "Microcontrolador", "label_clock": "Velocidade do clock", "label_voltage": "Tensão de operação", "label_pins": "Pinos digitais I/O", "label_usb": "Interface USB", "usage": "Uso típico", "usage_phrase": "Ideal para aprendizagem, prototipagem e projetos de hobby."},
    "hi": {"tech_specs": "तकनीकी विनिर्देश", "label_microcontroller": "माइक्रोकंट्रोलर", "label_clock": "क्लॉक स्पीड", "label_voltage": "संचालन वोल्टेज", "label_pins": "डिजिटल I/O पिन", "label_usb": "USB इंटरफेस", "usage": "आम उपयोग", "usage_phrase": "सीखने, प्रोटोटाइप और शौकिया परियोजनाओं के लिए आदर्श।"},
    "bn": {"tech_specs": "প্রযুক্তিগত বৈশিষ্ট্যাবলী", "label_microcontroller": "মাইক্রোকন্ট্রোলার", "label_clock": "ক্লক স্পিড", "label_voltage": "অপারেটিং ভোল্টেজ", "label_pins": "ডিজিটাল I/O পিন", "label_usb": "USB ইন্টারফেস", "usage": "সাধারণ ব্যবহার", "usage_phrase": "শেখা, প্রোটোটাইপিং এবং শখের প্রকল্পের জন্য আদর্শ।"},
    "ar": {"tech_specs": "المواصفات التقنية", "label_microcontroller": "الميكروكونترولر", "label_clock": "سرعة الساعة", "label_voltage": "جهد التشغيل", "label_pins": "دبابيس الإدخال / الإخراج الرقمية", "label_usb": "واجهة USB", "usage": "الاستخدام النموذجي", "usage_phrase": "مثالي للتعلم والنماذج الأولية والمشاريع الهواة."},
    "zh": {"tech_specs": "技术规格", "label_microcontroller": "微控制器", "label_clock": "时钟速度", "label_voltage": "工作电压", "label_pins": "数字 I/O 引脚", "label_usb": "USB 接口", "usage": "典型用途", "usage_phrase": "适用于学习、原型制作和业余项目。"},
    "ja": {"tech_specs": "技術仕様", "label_microcontroller": "マイクロコントローラ", "label_clock": "クロック周波数", "label_voltage": "動作電圧", "label_pins": "デジタルI/Oピン", "label_usb": "USBインターフェース", "usage": "一般的な使用法", "usage_phrase": "学習、試作、ホビープロジェクトに最適。"},
    "ko": {"tech_specs": "기술 사양", "label_microcontroller": "마이크로컨트롤러", "label_clock": "클록 속도", "label_voltage": "작동 전압", "label_pins": "디지털 I/O 핀", "label_usb": "USB 인터페이스", "usage": "일반적인 사용", "usage_phrase": "학습, 프로토타이핑 및 취미 프로젝트에 이상적입니다."},
    "th": {"tech_specs": "ข้อมูลจำเพาะทางเทคนิค", "label_microcontroller": "ไมโครคอนโทรลเลอร์", "label_clock": "ความเร็วสัญญาณนาฬิกา", "label_voltage": "แรงดันไฟฟ้าขณะทำงาน", "label_pins": "ขา I/O ดิจิตอล", "label_usb": "อินเทอร์เฟซ USB", "usage": "การใช้งานทั่วไป", "usage_phrase": "เหมาะสำหรับการเรียนรู้ การสร้างต้นแบบ และโครงการงานอดิเรก"},
    "tr": {"tech_specs": "Teknik özellikler", "label_microcontroller": "Mikrodenetleyici", "label_clock": "Saat Hızı", "label_voltage": "Çalışma Voltajı", "label_pins": "Dijital G/Ç Pinleri", "label_usb": "USB Arayüzü", "usage": "Tipik kullanım", "usage_phrase": "Öğrenme, prototipleme ve hobi projeleri için idealdir."},
    "ru": {"tech_specs": "Технические характеристики", "label_microcontroller": "Микроконтроллер", "label_clock": "Тактовая частота", "label_voltage": "Рабочее напряжение", "label_pins": "Цифровые пины I/O", "label_usb": "USB интерфейс", "usage": "Типичное использование", "usage_phrase": "Идеально подходит для обучения, прототипирования и хобби-проектов."}
}

board_specs = {
    "uno": {
        "board_name": "Arduino Uno",
        "microcontroller": "ATmega328P",
        "clock_speed": "16 MHz",
        "voltage": "5V",
        "digital_pins": "14 (6 PWM)",
        "usb": "USB-B"
    },
    "uno_r4": {
        "board_name": "Arduino Uno R4",
        "microcontroller": "RA4M1 (Renesas)",
        "clock_speed": "48 MHz",
        "voltage": "5V",
        "digital_pins": "14 (6 PWM)",
        "usb": "USB-C"
    },
    "nano": {
        "board_name": "Arduino Nano",
        "microcontroller": "ATmega328P",
        "clock_speed": "16 MHz",
        "voltage": "5V",
        "digital_pins": "22",
        "usb": "Mini-USB"
    },
    "esp32": {
        "board_name": "ESP32",
        "microcontroller": "Tensilica Xtensa LX6",
        "clock_speed": "240 MHz",
        "voltage": "3.3V",
        "digital_pins": "34",
        "usb": "Micro-USB"
    },
    "esp8266": {
        "board_name": "ESP8266",
        "microcontroller": "Tensilica L106",
        "clock_speed": "80 MHz",
        "voltage": "3.3V",
        "digital_pins": "17",
        "usb": "Micro-USB"
    },
    "raspberrypi": {
        "board_name": "Raspberry Pi",
        "microcontroller": "Broadcom BCM2711",
        "clock_speed": "1.5 GHz",
        "voltage": "5V",
        "digital_pins": "40 GPIO",
        "usb": "USB-C"
    }
}

output_dir = "board_templates"
os.makedirs(output_dir, exist_ok=True)

for board_code, spec in board_specs.items():
    for lang_code, t in translations.items():
        filename = f"{board_code}_{lang_code}.md"
        with open(os.path.join(output_dir, filename), "w") as f:
            f.write(f"# {spec['board_name']}\n\n")
            f.write(f"## {t['tech_specs']}\n\n")
            f.write(f"- {t['label_microcontroller']}: {spec['microcontroller']}\n")
            f.write(f"- {t['label_clock']}: {spec['clock_speed']}\n")
            f.write(f"- {t['label_voltage']}: {spec['voltage']}\n")
            f.write(f"- {t['label_pins']}: {spec['digital_pins']}\n")
            f.write(f"- {t['label_usb']}: {spec['usb']}\n\n")
            f.write(f"## {t['usage']}\n\n")
            f.write(f"{t['usage_phrase']}\n")

print("✅ All board info files generated successfully!")
