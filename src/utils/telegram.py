import os
import time
from typing import Optional
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

BASE_URL = "https://api.telegram.org/bot"


def send_and_wait(
    bot_token: str | None = None,
    chat_id: str | int | None = None,
    message: str = "",
    timeout: float = 60.0
) -> Optional[str]:
    """
    Send a message to a Telegram chat and wait for a reply.
    
    Args:
        bot_token: Telegram bot token (defaults to TELEGRAM_BOT_TOKEN from .env)
        chat_id: Chat ID (numeric) or username (with or without @) to send message to
        message: Message text to send
        timeout: Maximum time to wait for reply in seconds (default: 60)
    
    Returns:
        Reply message text, or None if timeout
    """
    if bot_token is None:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if bot_token is None:
            raise ValueError("bot_token must be provided or TELEGRAM_BOT_TOKEN must be set in .env")
    
    if chat_id is None:
        raise ValueError("chat_id must be provided")
    
    # Normalize chat_id: remove @ if present
    if isinstance(chat_id, str):
        chat_id_normalized = chat_id.lstrip('@')
    else:
        chat_id_normalized = str(chat_id)
    
    # Send the message
    url = f"{BASE_URL}{bot_token}/sendMessage"
    response = requests.post(url, json={
        "chat_id": chat_id_normalized,
        "text": message
    })
    
    sent_data = response.json()
    if not sent_data.get("ok"):
        error_desc = sent_data.get('description', 'Unknown error')
        raise ValueError(f"Failed to send message: {error_desc}")
    
    # Get the actual chat ID from the sent message
    actual_chat_id = sent_data["result"]["chat"]["id"]
    sent_timestamp = sent_data["result"]["date"]
    sent_message_id = sent_data["result"]["message_id"]
    
    # Poll for replies
    start_time = time.time()
    last_update_id = 0
    
    while time.time() - start_time < timeout:
        url = f"{BASE_URL}{bot_token}/getUpdates"
        params = {"offset": last_update_id + 1, "timeout": 10}
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        updates_data = response.json()
        if not updates_data.get("ok"):
            break
        
        for update in updates_data.get("result", []):
            last_update_id = max(last_update_id, update.get("update_id", 0))
            
            if "message" in update:
                msg = update["message"]
                msg_chat_id = msg.get("chat", {}).get("id")
                msg_timestamp = msg.get("date", 0)
                msg_id = msg.get("message_id")
                msg_text = msg.get("text")
                
                # Check if this is a reply from the same chat, after our message
                if (msg_chat_id == actual_chat_id and
                    msg_timestamp > sent_timestamp and
                    msg_id != sent_message_id and
                    msg_text):
                    return msg_text
        
        # Small delay to avoid hammering the API
        time.sleep(0.5)
    
    return None


# Alias for backward compatibility
send_and_wait_sync = send_and_wait


def get_recent_chats(bot_token: str | None = None) -> list[dict]:
    """
    Get recent chats that have sent messages to the bot.
    Useful for finding chat IDs.
    
    Args:
        bot_token: Telegram bot token (defaults to TELEGRAM_BOT_TOKEN from .env)
    
    Returns:
        List of dicts with 'chat_id' and 'username' (if available)
    """
    if bot_token is None:
        bot_token = get_bot_token()
    
    url = f"{BASE_URL}{bot_token}/getUpdates"
    response = requests.get(url)
    response.raise_for_status()
    
    updates_data = response.json()
    if not updates_data.get("ok"):
        return []
    
    chats = {}
    for update in updates_data.get("result", []):
        if "message" in update:
            chat = update["message"].get("chat", {})
            chat_id = chat.get("id")
            if chat_id and chat_id not in chats:
                chats[chat_id] = {
                    'chat_id': chat_id,
                    'username': chat.get("username"),
                    'first_name': chat.get("first_name"),
                    'type': chat.get("type")
                }
    
    return list(chats.values())


def get_bot_token() -> str:
    """
    Get the bot token from environment variable.
    
    Returns:
        Bot token from TELEGRAM_BOT_TOKEN env var
    
    Raises:
        ValueError: If TELEGRAM_BOT_TOKEN is not set
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token is None:
        raise ValueError("TELEGRAM_BOT_TOKEN must be set in .env file")
    return token
