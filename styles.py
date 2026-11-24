
import streamlit as st


def apply_styles():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Noto+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* =========================================
       DESIGN SYSTEM — LIME & GRAPHITE
       ========================================= */

    :root {
        --graphite: #202420;
        --lime: #C6F432;
        --lime-hover: #B4DF25;
        --soft-lime: #E9F3D5;
        --background: #F6F7F2;
        --white: #FFFFFF;
        --border: #DCE1D5;
        --muted: #687064;
    }

    /* =========================================
       GLOBAL LAYOUT
       ========================================= */

    .stApp {
        background-color: var(--background);
    }

    .block-container {
        max-width: 1250px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    /* =========================================
       TYPOGRAPHY — DM SANS
       ========================================= */

    html, body, .stApp,
    .stApp p,
    .stApp label,
    .stApp button,
    .stApp input,
    .stApp textarea,
    [data-testid="stMarkdownContainer"],
    [data-testid="stSidebarNavLink"],
    [data-baseweb="select"] {
        font-family: 'DM Sans', 'Noto Sans',
                     sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'DM Sans', 'Noto Sans',
                     sans-serif !important;
    }

    h1 {
        font-size: 2.7rem !important;
        font-weight: 700 !important;
        letter-spacing: -1.8px;
    }

    h2 {
        font-weight: 600 !important;
        letter-spacing: -0.8px;
    }

    h3 {
        font-weight: 600 !important;
        letter-spacing: -0.4px;
    }

    .stApp p {
        line-height: 1.65;
    }

    code, pre {
        font-family: 'JetBrains Mono',
                     monospace !important;
    }

    /* =========================================
       SIDEBAR
       ========================================= */

    [data-testid="stSidebar"] {
        background-color: #202420;
    }

    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }

    [data-testid="stSidebarNavLink"] {
        border-radius: 10px;
        margin-bottom: 5px;
        font-weight: 500;
        transition: background-color 0.2s ease;
    }

    [data-testid="stSidebarNavLink"]:hover {
        background-color: #353B32;
    }

    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background-color: #C6F432 !important;
        color: #202420 !important;
    }

    [data-testid="stSidebarNavLink"][aria-current="page"] * {
        color: #202420 !important;
    }

    /* =========================================
       BUTTONS
       ========================================= */

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 44px;
        transition: all 0.2s ease;
    }

    button[kind="primary"],
    button[kind="primaryFormSubmit"] {
        background-color: #C6F432 !important;
        color: #202420 !important;
        border: 1px solid #C6F432 !important;
    }

    button[kind="primary"]:hover,
    button[kind="primaryFormSubmit"]:hover {
        background-color: #B4DF25 !important;
        color: #202420 !important;
    }

    button[kind="primary"] p,
    button[kind="primaryFormSubmit"] p {
        color: #202420 !important;
    }

    .stButton > button:hover {
        border-color: #8EAD27;
    }

    /* =========================================
       INPUT FIELDS
       ========================================= */

    [data-baseweb="input"],
    [data-baseweb="textarea"],
    [data-baseweb="select"] > div {
        border-radius: 10px;
    }

    /* =========================================
       CARDS
       ========================================= */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #DCE1D5;
        border-radius: 16px;
        padding: 20px;
    }

    [data-testid="stMetricValue"] {
        font-weight: 700;
        letter-spacing: -1px;
    }

    .science-card {
        background-color: #FFFFFF;
        border: 1px solid #DCE1D5;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .science-card h3 {
        margin-top: 0;
        color: #202420;
    }

    /* =========================================
       HERO BANNER
       ========================================= */

    .science-hero {
        background-color: #C6F432;
        color: #202420;
        border-radius: 22px;
        padding: 40px;
        margin-bottom: 28px;
    }

    .science-hero h1 {
        color: #202420;
        font-size: 3rem !important;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .science-hero p {
        color: #202420;
        font-size: 1.05rem;
    }

    .science-eyebrow {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* =========================================
       AI CHAT
       ========================================= */

    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #DCE1D5;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) {
        background-color: #E9F3D5;
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #202420;
        color: #C6F432;
    }

    [data-testid="stChatMessageAvatarUser"] {
        background-color: #C6F432;
        color: #202420;
    }

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }

    /* =========================================
       EXPANDERS
       ========================================= */

    [data-testid="stExpander"] {
        border-radius: 12px;
    }

    [data-testid="stMain"] [data-testid="stExpander"] {
        background-color: #FFFFFF;
    }

    /* =========================================
       TABLES
       ========================================= */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stMain"] table {
        background-color: #FFFFFF;
        border-collapse: collapse;
        width: 100%;
    }

    [data-testid="stMain"] th {
        background-color: #E9F3D5;
        color: #202420;
        font-weight: 600;
    }

    [data-testid="stMain"] td,
    [data-testid="stMain"] th {
        padding: 12px;
        border: 1px solid #DCE1D5;
    }

    /* =========================================
       FILE UPLOADER
       ========================================= */

    [data-testid="stFileUploaderDropzone"] {
        border-radius: 14px;
    }

    /* =========================================
       PROGRESS
       ========================================= */

    [data-testid="stProgress"] [role="progressbar"] > div {
        background-color: #C6F432;
    }

    /* =========================================
       DIVIDERS
       ========================================= */

    hr {
        border-color: #DCE1D5;
    }

    /* =========================================
       MOBILE RESPONSIVE DESIGN
       ========================================= */

    @media (max-width: 768px) {

        .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 2rem !important;
            letter-spacing: -1px;
        }

        .science-hero {
            padding: 24px;
            border-radius: 16px;
        }

        .science-hero h1 {
            font-size: 2rem !important;
        }

        .science-card {
            padding: 16px;
        }

        [data-testid="stChatMessage"] {
            padding: 12px;
        }
    }

    </style>
    """, unsafe_allow_html=True)
