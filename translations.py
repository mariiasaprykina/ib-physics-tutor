
import streamlit as st


LANGUAGES = {
    "en": "English",
    "sk": "Slovenčina",
    "uk": "Українська",
    "cs": "Čeština",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "pl": "Polski",
    "hu": "Magyar",
    "it": "Italiano",
    "ru": "Русский",
    "zh": "中文",
    "ja": "日本語",
    "pt": "Português",
    "ar": "العربية",
}


LANGUAGE_NAMES = {
    "en": "English",
    "sk": "Slovak",
    "uk": "Ukrainian",
    "cs": "Czech",
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "pl": "Polish",
    "hu": "Hungarian",
    "it": "Italian",
    "ru": "Russian",
    "zh": "Simplified Chinese",
    "ja": "Japanese",
    "pt": "Portuguese",
    "ar": "Arabic",
}


KEYS = [
    "practice",
    "exam",
    "diagnostic",
    "progress",
    "new_chat",
    "chat_history",
    "chat_input",
    "logout",
    "settings",
    "interface_language",
    "ai_language",
    "auto_language",
    "english_terms",
]


TEXTS = {
    "en": [
        "Practice",
        "Exam preparation",
        "Diagnostic test",
        "My progress",
        "New chat",
        "Chat history",
        "Enter your physics question...",
        "Log out",
        "Settings",
        "Interface language",
        "AI explanation language",
        "Automatic detection",
        "Keep English physics terminology",
    ],

    "sk": [
        "Precvičovanie",
        "Príprava na skúšku",
        "Diagnostický test",
        "Môj pokrok",
        "Nový chat",
        "História konverzácií",
        "Zadajte otázku z fyziky...",
        "Odhlásiť sa",
        "Nastavenia",
        "Jazyk rozhrania",
        "Jazyk vysvetlenia AI",
        "Automatické rozpoznanie",
        "Zachovať anglickú fyzikálnu terminológiu",
    ],

    "uk": [
        "Практика",
        "Підготовка до іспиту",
        "Діагностичний тест",
        "Мій прогрес",
        "Новий чат",
        "Історія чатів",
        "Введіть запитання з фізики...",
        "Вийти",
        "Налаштування",
        "Мова інтерфейсу",
        "Мова пояснення ШІ",
        "Автоматичне визначення",
        "Зберігати англійську фізичну термінологію",
    ],

    "cs": [
        "Procvičování",
        "Příprava na zkoušku",
        "Diagnostický test",
        "Můj pokrok",
        "Nový chat",
        "Historie konverzací",
        "Zadejte otázku z fyziky...",
        "Odhlásit se",
        "Nastavení",
        "Jazyk rozhraní",
        "Jazyk vysvětlení AI",
        "Automatické rozpoznání",
        "Zachovat anglickou fyzikální terminologii",
    ],

    "de": [
        "Übungen",
        "Prüfungsvorbereitung",
        "Diagnosetest",
        "Mein Fortschritt",
        "Neuer Chat",
        "Chatverlauf",
        "Gib deine Physikfrage ein...",
        "Abmelden",
        "Einstellungen",
        "Sprache der Benutzeroberfläche",
        "Sprache der KI-Erklärungen",
        "Automatische Erkennung",
        "Englische Physikbegriffe beibehalten",
    ],

    "es": [
        "Práctica",
        "Preparación para el examen",
        "Prueba diagnóstica",
        "Mi progreso",
        "Nuevo chat",
        "Historial de chats",
        "Escribe tu pregunta de física...",
        "Cerrar sesión",
        "Configuración",
        "Idioma de la interfaz",
        "Idioma de las explicaciones de IA",
        "Detección automática",
        "Mantener la terminología física en inglés",
    ],

    "fr": [
        "Entraînement",
        "Préparation à l'examen",
        "Test diagnostique",
        "Mes progrès",
        "Nouvelle conversation",
        "Historique des conversations",
        "Saisissez votre question de physique...",
        "Se déconnecter",
        "Paramètres",
        "Langue de l'interface",
        "Langue des explications de l'IA",
        "Détection automatique",
        "Conserver la terminologie physique anglaise",
    ],

    "pl": [
        "Ćwiczenia",
        "Przygotowanie do egzaminu",
        "Test diagnostyczny",
        "Moje postępy",
        "Nowy czat",
        "Historia czatów",
        "Wpisz pytanie z fizyki...",
        "Wyloguj się",
        "Ustawienia",
        "Język interfejsu",
        "Język wyjaśnień AI",
        "Automatyczne wykrywanie",
        "Zachowaj angielską terminologię fizyczną",
    ],

    "hu": [
        "Gyakorlás",
        "Vizsgafelkészítés",
        "Diagnosztikai teszt",
        "Fejlődésem",
        "Új beszélgetés",
        "Beszélgetési előzmények",
        "Írd be a fizikai kérdésedet...",
        "Kijelentkezés",
        "Beállítások",
        "Felület nyelve",
        "AI-magyarázatok nyelve",
        "Automatikus felismerés",
        "Angol fizikai szakkifejezések megtartása",
    ],

    "it": [
        "Esercitazione",
        "Preparazione all'esame",
        "Test diagnostico",
        "I miei progressi",
        "Nuova chat",
        "Cronologia delle chat",
        "Inserisci la tua domanda di fisica...",
        "Esci",
        "Impostazioni",
        "Lingua dell'interfaccia",
        "Lingua delle spiegazioni IA",
        "Rilevamento automatico",
        "Mantieni la terminologia fisica inglese",
    ],

    "ru": [
        "Практика",
        "Подготовка к экзамену",
        "Диагностический тест",
        "Мой прогресс",
        "Новый чат",
        "История чатов",
        "Введите вопрос по физике...",
        "Выйти",
        "Настройки",
        "Язык интерфейса",
        "Язык объяснений ИИ",
        "Автоматическое определение",
        "Сохранять английскую физическую терминологию",
    ],

    "zh": [
        "练习",
        "考试准备",
        "诊断测试",
        "我的学习进度",
        "新对话",
        "聊天记录",
        "请输入你的物理问题...",
        "退出登录",
        "设置",
        "界面语言",
        "AI 讲解语言",
        "自动检测",
        "保留英文物理术语",
    ],

    "ja": [
        "練習",
        "試験対策",
        "診断テスト",
        "学習の進捗",
        "新しいチャット",
        "チャット履歴",
        "物理の質問を入力してください...",
        "ログアウト",
        "設定",
        "表示言語",
        "AIの解説言語",
        "自動検出",
        "英語の物理用語を保持する",
    ],

    "pt": [
        "Prática",
        "Preparação para o exame",
        "Teste diagnóstico",
        "Meu progresso",
        "Nova conversa",
        "Histórico de conversas",
        "Digite sua pergunta de física...",
        "Sair",
        "Configurações",
        "Idioma da interface",
        "Idioma das explicações da IA",
        "Detecção automática",
        "Manter a terminologia de física em inglês",
    ],

    "ar": [
        "التدريب",
        "التحضير للامتحان",
        "اختبار تشخيصي",
        "تقدمي",
        "محادثة جديدة",
        "سجل المحادثات",
        "أدخل سؤالك في الفيزياء...",
        "تسجيل الخروج",
        "الإعدادات",
        "لغة الواجهة",
        "لغة شرح الذكاء الاصطناعي",
        "الكشف التلقائي",
        "الاحتفاظ بالمصطلحات الفيزيائية الإنجليزية",
    ],
}


TRANSLATIONS = {
    lang: dict(zip(KEYS, values))
    for lang, values in TEXTS.items()
}


def init_languages():
    if "ui_language" not in st.session_state:
        st.session_state.ui_language = "en"

    if "ai_language" not in st.session_state:
        st.session_state.ai_language = "auto"

    if "keep_english_terms" not in st.session_state:
        st.session_state.keep_english_terms = True


def t(key):
    lang = st.session_state.get("ui_language", "en")

    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(
        key,
        TRANSLATIONS["en"].get(key, key)
    )


def get_language_instruction():
    lang = st.session_state.get("ai_language", "auto")

    if lang == "auto":
        instruction = (
            "Automatically detect the student's language "
            "and respond in that language."
        )
    else:
        language = LANGUAGE_NAMES.get(lang, "English")

        instruction = (
            f"Respond in {language}, regardless of the "
            "language of the original physics question."
        )

    if st.session_state.get("keep_english_terms", True):
        instruction += (
            " Include important IB Physics terminology "
            "in English in parentheses when useful."
        )

    instruction += (
        " Preserve the original wording of quoted exam questions. "
        "Use accurate scientific terminology, SI units, "
        "standard mathematical notation and LaTeX formulas. "
        "Maintain all pedagogical tutoring instructions."
    )

    return instruction



def show_language_settings(on_change=None):
    init_languages()

    with st.sidebar.expander(
        "🌐 " + t("settings"),
        expanded=False
    ):
        st.selectbox(
            t("interface_language"),
            options=list(LANGUAGES.keys()),
            format_func=lambda code: LANGUAGES[code],
            key="ui_language",
            on_change=on_change,
        )

        st.selectbox(
            t("ai_language"),
            options=["auto"] + list(LANGUAGES.keys()),
            format_func=lambda code: (
                t("auto_language")
                if code == "auto"
                else LANGUAGES[code]
            ),
            key="ai_language",
            on_change=on_change,
        )

        st.checkbox(
            t("english_terms"),
            key="keep_english_terms",
            on_change=on_change,
        )
