
from datetime import datetime, timezone

import streamlit as st

from auth import get_authenticated_client


def get_client():
    client = get_authenticated_client()

    if client is None:
        raise RuntimeError("Please log in again.")

    session = st.session_state.get("auth_session")

    if session is None or not session.access_token:
        raise RuntimeError("No Supabase access token.")

    result = client.auth.get_user(session.access_token)

    if not result.user:
        raise RuntimeError("Supabase user verification failed.")

    st.session_state.user_id = result.user.id

    return client


def create_conversation(title="New conversation"):
    client = get_client()
    user_id = st.session_state["user_id"]

    result = (
        client.table("tutor_conversations")
        .insert({
            "user_id": user_id,
            "title": title[:100]
        })
        .execute()
    )

    if not result.data:
        raise RuntimeError("Could not create conversation.")

    return result.data[0]["id"]


def get_conversations():
    client = get_client()

    result = (
        client.table("tutor_conversations")
        .select("id, title, created_at, updated_at")
        .order("updated_at", desc=True)
        .execute()
    )

    return result.data or []


def get_messages(conversation_id):
    client = get_client()

    result = (
        client.table("tutor_messages")
        .select("role, content")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )

    return [
        {
            "role": row["role"],
            "content": row["content"]
        }
        for row in (result.data or [])
    ]


def save_message(conversation_id, role, content):
    client = get_client()
    user_id = st.session_state["user_id"]

    client.table("tutor_messages").insert({
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": role,
        "content": content
    }).execute()

    client.table("tutor_conversations").update({
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", conversation_id).execute()


def rename_conversation(conversation_id, title):
    client = get_client()

    client.table("tutor_conversations").update({
        "title": title[:100]
    }).eq("id", conversation_id).execute()


def delete_conversation(conversation_id):
    client = get_client()

    client.table("tutor_conversations").delete().eq(
        "id", conversation_id
    ).execute()
