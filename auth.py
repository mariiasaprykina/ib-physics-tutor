
import streamlit as st
from supabase import create_client


def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


def show_login():
    st.title("⚛️ IB Physics AI Tutor")
    st.write("Welcome! Sign in to start learning physics.")

    login_tab, signup_tab = st.tabs(
        ["Log in", "Create account"]
    )

    # -------------------------
    # LOG IN
    # -------------------------

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input(
                "Password",
                type="password"
            )
            login = st.form_submit_button("Log in")

        if login:
            if not email.strip() or not password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    client = get_supabase()

                    result = client.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password,
                    })

                    if result.session and result.user:
                        st.session_state.auth_session = result.session
                        st.session_state.user_id = result.user.id

                        if "physics_level" not in st.session_state:
                            st.session_state.physics_level = "SL"

                        st.rerun()
                    else:
                        st.error("Unable to sign in.")

                except Exception as e:
                    st.error(f"Login failed: {type(e).__name__}")
                    print(
                        f"SUPABASE LOGIN ERROR: {type(e).__name__}: {e}",
                        flush=True
                    )
    # -------------------------
    # CREATE ACCOUNT
    # -------------------------

    with signup_tab:
        with st.form("signup_form"):
            email = st.text_input("Email address")
            password = st.text_input(
                "Create password",
                type="password"
            )
            level = st.selectbox(
                "Physics level",
                ["SL", "HL"]
            )

            signup = st.form_submit_button(
                "Create account"
            )

        if signup:
            if not email.strip():
                st.warning("Please enter your email address.")

            elif len(password) < 8:
                st.error(
                    "Password must contain at least 8 characters."
                )

            else:
                try:
                    client = get_supabase()

                    result = client.auth.sign_up({
                        "email": email.strip(),
                        "password": password,
                    })

                    if result.session and result.user:
                        st.session_state.auth_session = result.session
                        st.session_state.user_id = result.user.id
                        st.session_state.physics_level = level

                        st.rerun()

                    else:
                        st.success(
                            "If email confirmation is required, "
                            "check your inbox and confirm your account. "
                            "Then return and log in."
                        )

                except Exception as e:
                    print(
                        f"Supabase signup error: "
                        f"{type(e).__name__}"
                    )
                    st.error(
                        "Registration failed. Please try again later."
                    )


# -------------------------
# AUTHENTICATED CLIENT
# -------------------------

def get_authenticated_client():
    session = st.session_state.get("auth_session")

    if session is None:
        return None

    try:
        client = get_supabase()

        result = client.auth.set_session(
            session.access_token,
            session.refresh_token,
        )

        if not result.session or not result.user:
            st.session_state.pop("auth_session", None)
            st.session_state.pop("user_id", None)
            return None

        st.session_state.auth_session = result.session
        st.session_state.user_id = result.user.id

        if "physics_level" not in st.session_state:
            st.session_state.physics_level = "SL"

        return client

    except Exception as e:
        print(
            f"Supabase session error: "
            f"{type(e).__name__}"
        )

        st.session_state.pop("auth_session", None)
        st.session_state.pop("user_id", None)

        return None


# -------------------------
# LOG OUT
# -------------------------

def logout():
    client = get_authenticated_client()

    if client:
        try:
            client.auth.sign_out()
        except Exception:
            pass

    st.session_state.clear()
    st.rerun()
