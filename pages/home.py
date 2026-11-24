
import streamlit as st
import base64
from pathlib import Path
from html import escape


# ==========================================
# LANGUAGE SETTINGS
# ==========================================

language = st.session_state.get("ui_language", "en")
direction = "rtl" if language == "ar" else "ltr"


# ==========================================
# TRANSLATIONS
# ==========================================

HOME_TEXTS = {
    "en": [
        "Think physics.",
        "Beyond formulas.",
        "Understand concepts. Develop reasoning. Build confidence.",
        "Start learning",
        "Explore your workspace",
        "IB Exam",
        "Understand the structure and requirements of the IB Physics exam.",
        "Diagnostic",
        "Identify your knowledge gaps and learning needs.",
        "AI Tutor",
        "Develop problem-solving skills through guided reasoning.",
        "My Progress",
        "Track your learning development.",
        "Open",
        "The philosophy of learning",
        ""
    ],

    "sk": [
        "Mysli fyzikálne.",
        "Viac než vzorce.",
        "Porozumej konceptom. Rozvíjaj myslenie. Získaj istotu.",
        "Začať sa učiť",
        "Preskúmaj svoj vzdelávací priestor",
        "IB skúška",
        "Spoznaj štruktúru a požiadavky skúšky IB z fyziky.",
        "Diagnostika",
        "Odhaľ medzery vo vedomostiach.",
        "AI tútor",
        "Rozvíjaj schopnosť riešiť úlohy prostredníctvom usmerneného uvažovania.",
        "Môj pokrok",
        "Sleduj svoj vzdelávací pokrok.",
        "Otvoriť",
        "Filozofia učenia",
        "Čo nedokážem vytvoriť, tomu nerozumiem."
    ],

    "uk": [
        "Мисли фізично.",
        "Більше ніж формули.",
        "Розумій концепції. Розвивай мислення. Здобувай впевненість.",
        "Почати навчання",
        "Твій навчальний простір",
        "Іспит IB",
        "Дізнайся про структуру та вимоги іспиту IB з фізики.",
        "Діагностика",
        "Визнач прогалини у знаннях.",
        "AI-репетитор",
        "Розвивай навички розв’язування задач через спрямоване міркування.",
        "Мій прогрес",
        "Відстежуй свій навчальний розвиток.",
        "Відкрити",
        "Філософія навчання",
        "Те, чого я не можу створити, я не розумію."
    ],

    "ru": [
        "Мысли физически.",
        "Больше, чем формулы.",
        "Понимай концепции. Развивай мышление. Обретай уверенность.",
        "Начать обучение",
        "Твоё учебное пространство",
        "Экзамен IB",
        "Изучи структуру и требования экзамена IB по физике.",
        "Диагностика",
        "Определи пробелы в знаниях.",
        "AI-репетитор",
        "Развивай навыки решения задач через направленное рассуждение.",
        "Мой прогресс",
        "Отслеживай своё развитие.",
        "Открыть",
        "Философия обучения",
        "То, что я не могу создать, я не понимаю."
    ],

    "cs": [
        "Mysli fyzikálně.",
        "Více než vzorce.",
        "Porozuměj konceptům. Rozvíjej myšlení. Získej jistotu.",
        "Začít se učit",
        "Tvůj vzdělávací prostor",
        "IB zkouška",
        "Poznej strukturu a požadavky zkoušky IB.",
        "Diagnostika",
        "Odhal mezery ve znalostech.",
        "AI tutor",
        "Rozvíjej schopnost řešit úlohy.",
        "Můj pokrok",
        "Sleduj svůj pokrok.",
        "Otevřít",
        "Filozofie učení",
        "Čemu nedokážu dát vzniknout, tomu nerozumím."
    ],

    "de": [
        "Denke physikalisch.",
        "Mehr als Formeln.",
        "Verstehe Konzepte. Entwickle dein Denken.",
        "Lernen beginnen",
        "Dein Lernbereich",
        "IB-Prüfung",
        "Verstehe die Struktur der IB-Prüfung.",
        "Diagnostik",
        "Erkenne deine Wissenslücken.",
        "KI-Tutor",
        "Entwickle deine Problemlösungsfähigkeiten.",
        "Mein Fortschritt",
        "Verfolge deinen Lernfortschritt.",
        "Öffnen",
        "Die Philosophie des Lernens",
        "Was ich nicht erschaffen kann, verstehe ich nicht."
    ],

    "fr": [
        "Pense physique.",
        "Au-delà des formules.",
        "Comprends les concepts. Développe ton raisonnement.",
        "Commencer",
        "Ton espace d’apprentissage",
        "Examen IB",
        "Comprends la structure de l’examen IB.",
        "Diagnostic",
        "Identifie tes lacunes.",
        "Tuteur IA",
        "Développe tes compétences en résolution de problèmes.",
        "Mes progrès",
        "Suis tes progrès.",
        "Ouvrir",
        "La philosophie de l’apprentissage",
        "Ce que je ne peux pas créer, je ne le comprends pas."
    ],

    "es": [
        "Piensa en física.",
        "Más allá de las fórmulas.",
        "Comprende conceptos. Desarrolla tu razonamiento.",
        "Empezar",
        "Tu espacio de aprendizaje",
        "Examen IB",
        "Comprende la estructura del examen IB.",
        "Diagnóstico",
        "Identifica tus lagunas de conocimiento.",
        "Tutor IA",
        "Desarrolla tus habilidades para resolver problemas.",
        "Mi progreso",
        "Sigue tu progreso.",
        "Abrir",
        "La filosofía del aprendizaje",
        "Lo que no puedo crear, no lo entiendo."
    ],

    "it": [
        "Pensa in termini fisici.",
        "Oltre le formule.",
        "Comprendi i concetti. Sviluppa il ragionamento.",
        "Inizia",
        "Il tuo spazio di apprendimento",
        "Esame IB",
        "Comprendi la struttura dell’esame IB.",
        "Diagnostica",
        "Individua le lacune.",
        "Tutor IA",
        "Sviluppa le capacità di risoluzione dei problemi.",
        "I miei progressi",
        "Segui i tuoi progressi.",
        "Apri",
        "La filosofia dell’apprendimento",
        "Ciò che non posso creare, non lo comprendo."
    ],

    "pl": [
        "Myśl fizycznie.",
        "Więcej niż wzory.",
        "Rozumiej pojęcia. Rozwijaj rozumowanie.",
        "Rozpocznij naukę",
        "Twoja przestrzeń edukacyjna",
        "Egzamin IB",
        "Poznaj strukturę egzaminu IB.",
        "Diagnostyka",
        "Zidentyfikuj luki w wiedzy.",
        "Tutor AI",
        "Rozwijaj umiejętność rozwiązywania problemów.",
        "Moje postępy",
        "Śledź swoje postępy.",
        "Otwórz",
        "Filozofia uczenia się",
        "Czego nie potrafię stworzyć, tego nie rozumiem."
    ],

    "hu": [
        "Gondolkodj fizikusként.",
        "Több mint képletek.",
        "Értsd meg a fogalmakat. Fejleszd a gondolkodásodat.",
        "Tanulás indítása",
        "A tanulási tered",
        "IB vizsga",
        "Ismerd meg a vizsga felépítését.",
        "Diagnosztika",
        "Azonosítsd a tudáshiányokat.",
        "AI tutor",
        "Fejleszd a problémamegoldó képességedet.",
        "Fejlődésem",
        "Kövesd a fejlődésed.",
        "Megnyitás",
        "A tanulás filozófiája",
        "Amit nem tudok létrehozni, azt nem értem."
    ],

    "pt": [
        "Pensa em física.",
        "Além das fórmulas.",
        "Compreende conceitos. Desenvolve o raciocínio.",
        "Começar",
        "O teu espaço de aprendizagem",
        "Exame IB",
        "Compreende a estrutura do exame IB.",
        "Diagnóstico",
        "Identifica lacunas no conhecimento.",
        "Tutor IA",
        "Desenvolve competências de resolução de problemas.",
        "O meu progresso",
        "Acompanha o teu progresso.",
        "Abrir",
        "A filosofia da aprendizagem",
        "O que não consigo criar, não compreendo."
    ],

    "zh": [
        "用物理思维思考。",
        "超越公式。",
        "理解概念，发展推理能力，建立信心。",
        "开始学习",
        "你的学习空间",
        "IB 考试",
        "了解 IB 物理考试结构。",
        "诊断评估",
        "发现知识盲点。",
        "AI 导师",
        "培养解决物理问题的能力。",
        "我的进度",
        "追踪学习进展。",
        "打开",
        "学习哲学",
        "我无法创造的东西，我就不理解。"
    ],

    "ja": [
        "物理的に考える。",
        "公式を超えて。",
        "概念を理解し、推論力を育てよう。",
        "学習を始める",
        "あなたの学習スペース",
        "IB 試験",
        "IB 物理試験の構成を理解する。",
        "診断テスト",
        "知識の不足を見つける。",
        "AI チューター",
        "問題解決能力を育てる。",
        "学習進捗",
        "学習の進捗を確認する。",
        "開く",
        "学習の哲学",
        "自分で作り出せないものは、理解していない。"
    ],

    "ar": [
        "فكر بطريقة فيزيائية.",
        "ما وراء المعادلات.",
        "افهم المفاهيم وطوّر مهارات الاستدلال.",
        "ابدأ التعلم",
        "مساحة التعلم الخاصة بك",
        "امتحان IB",
        "افهم بنية امتحان الفيزياء.",
        "التقييم التشخيصي",
        "حدد الفجوات المعرفية.",
        "مدرس الذكاء الاصطناعي",
        "طوّر مهارات حل المسائل.",
        "تقدمي",
        "تابع تقدمك في التعلم.",
        "فتح",
        "فلسفة التعلم",
        "ما لا أستطيع ابتكاره، لا أفهمه."
    ]
}


# ==========================================
# HERO SLOGAN TRANSLATIONS
# ==========================================

HERO_TEXTS = {
    "en": [
        "Physics starts",
        "with understanding.",
        "Explore concepts, connect ideas and prepare for your IB Physics exam."
    ],

    "sk": [
        "Fyzika sa začína",
        "porozumením.",
        "Objavuj fyzikálne koncepty, hľadaj súvislosti a priprav sa na skúšku IB z fyziky."
    ],

    "uk": [
        "Фізика починається",
        "з розуміння.",
        "Досліджуй фізичні концепції, знаходь взаємозв’язки та готуйся до іспиту IB з фізики."
    ],

    "ru": [
        "Физика начинается",
        "с понимания.",
        "Изучай физические концепции, находи взаимосвязи и готовься к экзамену IB по физике."
    ],

    "cs": [
        "Fyzika začíná",
        "porozuměním.",
        "Objevuj fyzikální koncepty, hledej souvislosti a připrav se na zkoušku IB z fyziky."
    ],

    "de": [
        "Physik beginnt",
        "mit Verstehen.",
        "Entdecke physikalische Konzepte, erkenne Zusammenhänge und bereite dich auf deine IB-Physikprüfung vor."
    ],

    "fr": [
        "La physique commence",
        "par la compréhension.",
        "Explore les concepts, relie les idées et prépare ton examen de physique de l’IB."
    ],

    "es": [
        "La física comienza",
        "con la comprensión.",
        "Explora conceptos, conecta ideas y prepárate para tu examen de Física del IB."
    ],

    "it": [
        "La fisica inizia",
        "con la comprensione.",
        "Esplora i concetti, collega le idee e preparati all’esame di fisica IB."
    ],

    "pl": [
        "Fizyka zaczyna się",
        "od zrozumienia.",
        "Poznawaj pojęcia, dostrzegaj zależności i przygotuj się do egzaminu IB z fizyki."
    ],

    "hu": [
        "A fizika",
        "a megértéssel kezdődik.",
        "Fedezd fel a fizikai fogalmakat, ismerd fel az összefüggéseket és készülj fel az IB fizikavizsgára."
    ],

    "pt": [
        "A física começa",
        "com a compreensão.",
        "Explora conceitos, relaciona ideias e prepara-te para o exame de Física do IB."
    ],

    "zh": [
        "物理学始于",
        "理解。",
        "探索物理概念，建立知识联系，为 IB 物理考试做好准备。"
    ],

    "ja": [
        "物理学は",
        "理解から始まる。",
        "物理の概念を探究し、知識を結びつけ、IB物理試験に備えよう。"
    ],

    "ar": [
        "تبدأ الفيزياء",
        "بالفهم.",
        "استكشف المفاهيم، واربط الأفكار، واستعد لامتحان الفيزياء في البكالوريا الدولية."
    ]
}


T = HOME_TEXTS.get(
    language,
    HOME_TEXTS["en"]
).copy()

T[:3] = HERO_TEXTS.get(
    language,
    HERO_TEXTS["en"]
)


# ==========================================
# HOME PAGE STYLES
# ==========================================

st.html("""
<style>

.home-hero {
    background: #C6F432;
    color: #202420;
    padding: 42px;
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 25px;
    margin-bottom: 20px;
    overflow: hidden;
}

.home-hero-content {
    flex: 1;
    min-width: 220px;
}

.home-eyebrow {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}

.home-hero-title {
    font-size: clamp(32px, 5vw, 58px);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -2px;
    margin: 24px 0 20px;
}

.home-hero-description {
    font-size: 17px;
    line-height: 1.6;
    max-width: 620px;
}

.home-atom {
    flex: 0 1 210px;
    min-width: 120px;
}

.home-card {
    padding: 10px;
    min-height: 185px;
}

.home-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.home-card-icon {
    background: #E9F3D5;
    color: #202420;
    width: 52px;
    height: 52px;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.home-card-number {
    color: #687064;
    font-size: 13px;
    font-weight: 500;
}

.home-card-title {
    color: #202420;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 10px;
}

.home-card-description {
    color: #687064;
    font-size: 15px;
    line-height: 1.6;
}

.quote-banner {
    background: #202420;
    color: #FFFFFF;
    padding: 40px;
    border-radius: 24px;
    margin-top: 30px;
    overflow: hidden;
}

.quote-layout {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 35px;
}

.quote-content {
    flex: 3;
    min-width: 220px;
}

.quote-symbol {
    color: #C6F432;
    font-size: 100px;
    line-height: 0.8;
    margin-top: 20px;
}

.quote-text {
    color: #FFFFFF;
    font-size: clamp(25px, 4vw, 40px);
    font-weight: 600;
    line-height: 1.3;
    letter-spacing: -0.8px;
}

.quote-translation {
    color: #A8B0A3;
    font-size: 16px;
    line-height: 1.6;
    margin-top: 20px;
}

.quote-photo {
    flex: 1;
    min-width: 160px;
    max-width: 260px;
}

.quote-photo img {
    width: 100%;
    border-radius: 16px;
    filter: grayscale(100%);
    object-fit: cover;
}

.quote-credit {
    font-size: 10px;
    color: #A8B0A3;
    margin-top: 8px;
    text-align: center;
}

.quote-author {
    color: #C6F432;
    font-size: 20px;
    font-weight: 600;
}

.quote-bio {
    color: #A8B0A3;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 8px;
}

@media (max-width: 768px) {

    .home-hero {
        padding: 24px;
    }

    .home-atom {
        max-width: 130px;
        margin: auto;
    }

    .home-hero-title {
        letter-spacing: -1px;
    }

    .quote-banner {
        padding: 25px;
    }

    .quote-photo {
        max-width: 200px;
        margin: auto;
    }

    .home-card {
        min-height: auto;
    }
}

</style>
""")


# ==========================================
# ATOM GRAPHIC
# ==========================================

ATOM_SVG = """
<svg viewBox="0 0 220 220"
     xmlns="http://www.w3.org/2000/svg">

    <g transform="translate(110 110)"
       fill="none"
       stroke="#202420"
       stroke-width="1.5">

        <circle r="105"
                stroke-opacity="0.15"/>

        <circle r="92"
                stroke-opacity="0.15"
                stroke-dasharray="3 6"/>

        <ellipse rx="88" ry="30"/>

        <ellipse rx="88" ry="30"
                 transform="rotate(45)"/>

        <ellipse rx="88" ry="30"
                 transform="rotate(90)"/>

        <ellipse rx="88" ry="30"
                 transform="rotate(135)"/>

        <circle r="9" fill="#202420"/>

        <circle cx="88" cy="0"
                r="5" fill="#202420"/>

        <circle cx="0" cy="-88"
                r="5" fill="#202420"/>

        <circle cx="-62" cy="62"
                r="5" fill="#202420"/>

    </g>

</svg>
"""


# ==========================================
# HERO BANNER
# ==========================================

st.html(f"""
<div class="home-hero" dir="{direction}">

    <div class="home-hero-content">

        <div class="home-eyebrow">
            SCIENCEHUB / IB PHYSICS
        </div>

        <div class="home-hero-title">
            {escape(T[0])}<br>
            {escape(T[1])}
        </div>

        <div class="home-hero-description">
            {escape(T[2])}
        </div>

    </div>

    <div class="home-atom">
        {ATOM_SVG}
    </div>

</div>
""")


if st.button(
    T[3] + " ↗",
    type="primary",
    key="home_start"
):
    st.switch_page("pages/practice.py")


st.write("")


# ==========================================
# NAVIGATION ICONS
# ==========================================

ICONS = {

    "exam": """
    <svg width="26" height="26"
         viewBox="0 0 24 24"
         fill="none"
         stroke="currentColor"
         stroke-width="1.7"
         stroke-linecap="round"
         stroke-linejoin="round">

        <path d="M4 19V5a2 2 0 0 1 2-2h14v16H6a2 2 0 0 0 0 4h14"/>
        <path d="M8 7h8M8 11h6"/>

    </svg>
    """,

    "diagnostic": """
    <svg width="26" height="26"
         viewBox="0 0 24 24"
         fill="none"
         stroke="currentColor"
         stroke-width="1.7"
         stroke-linecap="round"
         stroke-linejoin="round">

        <rect x="5" y="4"
              width="14" height="18"
              rx="2"/>

        <rect x="9" y="2"
              width="6" height="4"
              rx="1"/>

        <path d="m8 14 3 3 5-6"/>

    </svg>
    """,

    "practice": """
    <svg width="26" height="26"
         viewBox="0 0 24 24"
         fill="none"
         stroke="currentColor"
         stroke-width="1.7"
         stroke-linecap="round"
         stroke-linejoin="round">

        <path d="M21 11.5a9 9 0 0 1-9 9
                 9 9 0 0 1-4-.9L3 21
                 l1.4-5A9 9 0 1 1 21 11.5Z"/>

        <path d="M8 11h8M8 15h5"/>

    </svg>
    """,

    "progress": """
    <svg width="26" height="26"
         viewBox="0 0 24 24"
         fill="none"
         stroke="currentColor"
         stroke-width="1.7"
         stroke-linecap="round"
         stroke-linejoin="round">

        <path d="M3 3v18h18"/>
        <path d="m6 15 5-5 4 4 6-8"/>
        <path d="M16 6h5v5"/>

    </svg>
    """
}


# ==========================================
# NAVIGATION CARDS
# ==========================================

st.subheader(T[4])

cards = [

    (
        "01",
        "exam",
        T[5],
        T[6],
        "pages/exam.py"
    ),

    (
        "02",
        "diagnostic",
        T[7],
        T[8],
        "pages/diagnostic.py"
    ),

    (
        "03",
        "practice",
        T[9],
        T[10],
        "pages/practice.py"
    ),

    (
        "04",
        "progress",
        T[11],
        T[12],
        "pages/progress.py"
    )

]


def render_card(card):

    number, icon, title, description, page = card

    with st.container(border=True):

        st.html(f"""
        <div class="home-card" dir="{direction}">

            <div class="home-card-top">

                <div class="home-card-icon">
                    {ICONS[icon]}
                </div>

                <div class="home-card-number">
                    {number}
                </div>

            </div>

            <div class="home-card-title">
                {escape(title)}
            </div>

            <div class="home-card-description">
                {escape(description)}
            </div>

        </div>
        """)

        if st.button(
            T[13] + " ↗",
            key=f"home_card_{number}",
            width="stretch"
        ):
            st.switch_page(page)


col1, col2 = st.columns(2)

with col1:
    render_card(cards[0])
    render_card(cards[2])

with col2:
    render_card(cards[1])
    render_card(cards[3])


# ==========================================
# FEYNMAN PHOTO
# ==========================================

photo_path = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "feynman.jpg"
)

photo_html = ""

if photo_path.is_file():

    photo_base64 = base64.b64encode(
        photo_path.read_bytes()
    ).decode("utf-8")

    photo_html = f"""
    <div class="quote-photo">

        <img
            src="data:image/jpeg;base64,{photo_base64}"
            alt="Richard P. Feynman"
        >

        <div class="quote-credit">

            Photo: Caltech, circa 1960.

            <a href="https://commons.wikimedia.org/wiki/File:Richard_Feynman_circa_1960.jpg"
               target="_blank"
               rel="noopener noreferrer"
               style="color: #C6F432;">

                Source

            </a>

        </div>

    </div>
    """


# ==========================================
# QUOTE TRANSLATION
# ==========================================

translation_html = ""

if T[15]:

    translation_html = f"""
    <div class="quote-translation"
         dir="{direction}">

        {escape(T[15])}

    </div>
    """


# ==========================================
# SCIENTIFIC QUOTE BANNER
# ==========================================

st.html(f"""
<div class="quote-banner">

    <div class="home-eyebrow"
         style="color: #C6F432;"
         dir="{direction}">

        {escape(T[14])}

    </div>

    <div class="quote-layout">

        <div class="quote-content">

            <div class="quote-symbol">
                “
            </div>

            <div class="quote-text">

                What I cannot create,<br>
                I do not understand.

            </div>

            {translation_html}

            <div style="
                width: 45px;
                height: 3px;
                background: #C6F432;
                margin: 25px 0 20px;
            "></div>

            <div class="quote-author">
                Richard P. Feynman
            </div>

            <div class="quote-bio">

                Theoretical physicist · 1918–1988
                <br>
                Nobel Prize in Physics, 1965

            </div>

            <div style="
                color: #A8B0A3;
                font-size: 11px;
                margin-top: 16px;
            ">

                Source: Feynman's blackboard, 1988.

            </div>

        </div>

        {photo_html}

    </div>


    <!-- WAVE GRAPHIC -->

    <svg width="100%"
         height="90"
         viewBox="0 0 600 100"
         preserveAspectRatio="none"
         style="margin-top: 35px;">

        <defs>

            <pattern id="home-quote-grid"
                     width="25"
                     height="25"
                     patternUnits="userSpaceOnUse">

                <path d="M 25 0 L 0 0 0 25"
                      fill="none"
                      stroke="#FFFFFF"
                      stroke-opacity="0.09"/>

            </pattern>

        </defs>

        <rect width="600"
              height="100"
              fill="url(#home-quote-grid)"/>

        <path d="
            M 0 50
            Q 37.5 -20 75 50
            T 150 50
            T 225 50
            T 300 50
            T 375 50
            T 450 50
            T 525 50
            T 600 50
        "
        fill="none"
        stroke="#C6F432"
        stroke-width="2"/>

        <path d="
            M 0 20
            Q 75 110 150 20
            T 300 20
            T 450 20
            T 600 20
        "
        fill="none"
        stroke="#FFFFFF"
        stroke-opacity="0.25"
        stroke-width="1.5"/>

    </svg>

</div>
""")


# ==========================================
# FOOTER
# ==========================================

st.write("")

st.caption(
    "ScienceHub · IB Physics AI Tutor"
)
