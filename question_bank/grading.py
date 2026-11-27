
from auth import get_authenticated_client


def get_client():
    client = get_authenticated_client()

    if client is None:
        raise RuntimeError("Please log in again.")

    return client


def start_test(
    topic,
    level,
    language="en",
    mode="learning",
    count=10
):
    client = get_client()

    result = client.rpc(
        "start_test",
        {
            "p_topic": topic,
            "p_level": level,
            "p_language": language,
            "p_mode": mode,
            "p_count": count
        }
    ).execute()

    return result.data


def get_test_question(question_id, language="en"):
    client = get_client()

    result = client.rpc(
        "get_test_question",
        {
            "p_question_id": str(question_id),
            "p_language": language
        }
    ).execute()

    return result.data


def submit_answer(
    attempt_id,
    question_id,
    selected_answer
):
    client = get_client()

    if isinstance(selected_answer, str):
        selected_answer = [selected_answer]

    if not isinstance(selected_answer, list):
        raise ValueError("Answer must be a list.")

    if not selected_answer:
        raise ValueError("Select an answer.")

    result = client.rpc(
        "submit_answer",
        {
            "p_attempt_id": str(attempt_id),
            "p_question_id": str(question_id),
            "p_selected_answer": selected_answer
        }
    ).execute()

    return result.data
