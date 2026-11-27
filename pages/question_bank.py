
import streamlit as st

from question_bank.grading import (
    start_test,
    get_test_question,
    submit_answer
)

LANGUAGES = {
    "English": "en",
    "Slovenčina": "sk",
    "Українська": "uk",
    "Čeština": "cs",
    "Deutsch": "de",
    "Español": "es",
    "Français": "fr",
    "Polski": "pl",
    "Magyar": "hu",
    "Italiano": "it",
    "Русский": "ru",
    "中文": "zh",
    "日本語": "ja",
    "Português": "pt",
    "العربية": "ar"
}

TOPICS = {
    "A.1 Kinematics": "A.1",
    "A.2 Forces and momentum": "A.2",
    "A.3 Work, energy and power": "A.3"
}

st.title("Question Bank")

st.markdown(
    "Practice physics, identify knowledge gaps "
    "and improve your understanding."
)

if "qb_attempt" not in st.session_state:
    st.session_state.qb_attempt = None

if "qb_feedback" not in st.session_state:
    st.session_state.qb_feedback = None

if "qb_question" not in st.session_state:
    st.session_state.qb_question = None


def reset_test():
    st.session_state.qb_attempt = None
    st.session_state.qb_feedback = None
    st.session_state.qb_question = None


attempt = st.session_state.qb_attempt
feedback = st.session_state.qb_feedback

if attempt is None:

    level = st.session_state.get("physics_level", "SL")

    st.caption(f"Physics level: {level}")

    topic = st.selectbox(
        "Select topic",
        list(TOPICS.keys())
    )

    language = st.selectbox(
        "Test language",
        list(LANGUAGES.keys())
    )

    mode = st.radio(
        "Test mode",
        ["Learning mode", "Exam mode"]
    )

    if mode == "Learning mode":
        st.info("Receive feedback after each answer.")
    else:
        st.info("Answers are saved without immediate feedback.")

    count = st.select_slider(
        "Number of questions",
        options=[1, 5, 10, 15, 20],
        value=1
    )

    if st.button(
        "Start test",
        type="primary",
        use_container_width=True
    ):
        try:
            st.session_state.qb_attempt = start_test(
                topic=TOPICS[topic],
                level=level,
                language=LANGUAGES[language],
                mode="learning" if mode == "Learning mode"
                else "exam",
                count=count
            )

            st.rerun()

        except Exception as e:
            st.error(f"Could not start test: {e}")

else:

    total = attempt["question_count"]
    position = attempt["current_position"]

    st.caption(
        f"{attempt['topic']} · "
        f"{attempt['level']} · "
        f"{attempt['language'].upper()}"
    )

    st.progress(min(position / total, 1.0))

    if feedback is not None:

        if attempt["mode"] == "learning":

            if feedback.get("is_correct"):
                st.success("Correct answer!")

            else:
                st.error("Not quite right.")

                st.markdown(
                    "### Learn with AI Tutor"
                )

                st.caption(
                    "Understand the concept "
                    "before trying another question."
                )

                st.button(
                    "Learn with AI Tutor",
                    disabled=True,
                    use_container_width=True
                )

                st.caption(
                    "AI Tutor integration coming next."
                )

        else:
            st.success("Answer saved.")

        if feedback.get("completed"):
            st.success("Test completed!")

            if st.button(
                "Finish test",
                use_container_width=True
            ):
                reset_test()
                st.rerun()

        else:
            if st.button(
                "Next question",
                type="primary",
                use_container_width=True
            ):
                st.session_state.qb_feedback = None
                st.session_state.qb_question = None
                st.rerun()

    elif position >= total:

        st.success("Test completed!")

        if st.button("Start another test"):
            reset_test()
            st.rerun()

    else:

        question_id = attempt["question_ids"][position]

        try:
            question = st.session_state.qb_question

            if (
                question is None
                or question["id"] != question_id
            ):
                question = get_test_question(
                    question_id,
                    attempt["language"]
                )

                st.session_state.qb_question = question

            st.subheader(
                f"Question {position + 1} of {total}"
            )

            st.markdown(question["question_text"])

            options = question["options"]

            option_labels = {
                option["id"]: option["text"]
                for option in options
            }

            selected = st.radio(
                "Select your answer",
                options=list(option_labels.keys()),
                format_func=lambda x: option_labels[x],
                index=None,
                key=f"qb_{attempt['attempt_id']}_{question_id}"
            )

            if st.button(
                "Submit answer",
                type="primary",
                disabled=selected is None,
                use_container_width=True
            ):

                result = submit_answer(
                    attempt_id=attempt["attempt_id"],
                    question_id=question_id,
                    selected_answer=[selected]
                )

                st.session_state.qb_feedback = result

                st.session_state.qb_attempt[
                    "current_position"
                ] = result["current_position"]

                st.rerun()

        except Exception as e:
            st.error(f"Question Bank error: {e}")
