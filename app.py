
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


st.set_page_config(
    page_title="IB Physics AI Tutor",
    page_icon="⚛️",
    layout="wide"
)


# Initialize language settings
init_languages()


# Default physics level
if "physics_level" not in st.session_state:
    st.session_state.physics_level = "SL"


# Require authentication
if "auth_session" not in st.session_state:
    show_login()
    st.stop()


supabase = get_authenticated_client()

if supabase is None:
    show_login()
    st.stop()


# Student profile
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


# Save physics level
def save_physics_level():
    supabase.table("profiles").update({
        "physics_level": st.session_state.physics_level
    }).eq("id", user_id).execute()


# Sidebar
with st.sidebar:

    st.title("⚛️ IB Physics Tutor")

    st.caption("Student account")

    st.radio(
        "IB Physics level",
        ["SL", "HL"],
        key="physics_level",
        horizontal=True,
        on_change=save_physics_level,
    )

    st.divider()


# Language settings
show_language_settings()


# Logout
with st.sidebar:

    st.divider()

    if st.button(
        t("logout"),
        key="logout_button",
        width="stretch",
    ):
        logout()


# Application pages
pages = [

    st.Page(
        "pages/exam.py",
        title=t("exam"),
        icon="📘",
        default=True,
    ),

    st.Page(
        "pages/diagnostic.py",
        title=t("diagnostic"),
        icon="📝",
    ),

    st.Page(
        "pages/practice.py",
        title=t("practice"),
        icon="💬",
    ),

    st.Page(
        "pages/progress.py",
        title=t("progress"),
        icon="📈",
    ),
]


# Run navigation
st.navigation(pages).run()
