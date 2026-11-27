
import streamlit as st

from auth import (
    show_login,
    get_authenticated_client,
    logout,
)

from translations import (
    init_languages,
    show_language_settings,
    t,
)

from styles import apply_styles


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="IB Physics AI Tutor",
    page_icon="⚛️",
    layout="wide"
)

apply_styles()


# ==========================================
# LANGUAGE SETTINGS
# ==========================================

init_languages()

HOME_NAMES = {
    "en": "Home",
    "sk": "Domov",
    "uk": "Головна",
    "ru": "Главная",
    "cs": "Domů",
    "de": "Startseite",
    "fr": "Accueil",
    "es": "Inicio",
    "it": "Home",
    "pl": "Strona główna",
    "hu": "Kezdőlap",
    "pt": "Início",
    "zh": "首页",
    "ja": "ホーム",
    "ar": "الرئيسية",
}


# ==========================================
# DEFAULT PHYSICS LEVEL
# ==========================================

if "physics_level" not in st.session_state:
    st.session_state.physics_level = "SL"


# ==========================================
# AUTHENTICATION
# ==========================================

if "auth_session" not in st.session_state:
    show_login()
    st.stop()


supabase = get_authenticated_client()

if supabase is None:
    show_login()
    st.stop()


# ==========================================
# STUDENT PROFILE
# ==========================================

user_id = st.session_state.user_id

try:

    response = (
        supabase.table("profiles")
        .select("physics_level")
        .eq("id", user_id)
        .execute()
    )

    profiles = response.data or []

    if profiles:

        if not st.session_state.get("profile_loaded"):

            st.session_state.physics_level = (
                profiles[0]["physics_level"]
            )

            st.session_state.profile_loaded = True

    else:

        supabase.table("profiles").insert({
            "id": user_id,
            "physics_level": st.session_state.physics_level,
        }).execute()

        st.session_state.profile_loaded = True

except Exception as e:

    st.error("Could not load student profile.")

    print(
        f"PROFILE ERROR: {type(e).__name__}: {e}",
        flush=True
    )

    st.stop()


# ==========================================
# SAVE PHYSICS LEVEL
# ==========================================

def save_physics_level():

    supabase.table("profiles").update({
        "physics_level": st.session_state.physics_level
    }).eq("id", user_id).execute()


# ==========================================
# SIDEBAR BRANDING
# ==========================================

with st.sidebar:

    st.html("""
    <div style="
        padding: 10px 0 20px;
        font-family: 'DM Sans', sans-serif;
    ">

        <div style="
            background: #C6F432;
            color: #202420;
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
        ">

            <svg width="32" height="32"
                 viewBox="0 0 40 40"
                 fill="none"
                 stroke="#202420"
                 stroke-width="1.5">

                <g transform="translate(20 20)">

                    <ellipse rx="17" ry="6"/>

                    <ellipse rx="17" ry="6"
                             transform="rotate(60)"/>

                    <ellipse rx="17" ry="6"
                             transform="rotate(120)"/>

                    <circle r="3" fill="#202420"/>

                </g>

            </svg>

        </div>

        <div style="
            color: #FFFFFF;
            font-size: 25px;
            font-weight: 700;
            letter-spacing: -0.8px;
        ">
            ScienceHub<span style="color:#C6F432;">.</span>
        </div>

        <div style="
            color: #A8B0A3;
            font-size: 11px;
            letter-spacing: 2px;
            font-weight: 500;
            margin-top: 5px;
        ">
            IB PHYSICS AI TUTOR
        </div>

    </div>
    """)

    st.divider()

    st.caption("Student account")

    st.radio(
        "IB Physics level",
        ["SL", "HL"],
        key="physics_level",
        horizontal=True,
        on_change=save_physics_level,
    )

    st.divider()


# ==========================================
# LANGUAGE SETTINGS
# ==========================================

show_language_settings()


# ==========================================
# LOGOUT
# ==========================================

with st.sidebar:

    st.divider()

    if st.button(
        t("logout"),
        key="logout_button",
        width="stretch",
        icon=":material/logout:",
    ):
        logout()
        st.rerun()


# ==========================================
# APPLICATION NAVIGATION
# ==========================================

language = st.session_state.get(
    "ui_language",
    "en"
)

home_title = HOME_NAMES.get(
    language,
    "Home"
)


pages = [

    st.Page(
        "pages/home.py",
        title=home_title,
        icon=":material/home:",
        default=True,
    ),

    st.Page(
        "pages/exam.py",
        title=t("exam"),
        icon=":material/menu_book:",
        url_path="exam",
    ),

    st.Page(
        "pages/diagnostic.py",
        title=t("diagnostic"),
        icon=":material/fact_check:",
        url_path="diagnostic",
    ),

    st.Page(
        "pages/practice.py",
        title=t("practice"),
        icon=":material/chat:",
        url_path="practice",
    ),

    st.Page(
        "pages/progress.py",
        title=t("progress"),
        icon=":material/monitoring:",
        url_path="progress",
    ),
    
st.Page(
    "pages/question_bank.py",
    title="Question Bank",
    icon=":material/quiz:"
),
]


# ==========================================
# RUN APPLICATION
# ==========================================

st.navigation(pages).run()
