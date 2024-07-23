from utils.common import Update, ContextTypes, get_collection_for_chat
from globals import current_categories

async def list_last_archived(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List the items last archived at the same time."""
    chat_id = update.message.chat_id

    current_category = current_categories.get(chat_id, "groceries")
    collection = get_collection_for_chat(chat_id, current_category)

    # Aggregate to unwind archived_at array, sort by it, and group to find the latest timestamp
    pipeline = [
        {"$match": {"archived": True, "archived_at": {"$ne": []}}},
        {"$unwind": "$archived_at"},
        {"$sort": {"archived_at": -1}},
        {"$group": {
            "_id": "$added_by",
            "latest_archived_at": {"$first": "$archived_at"},
            "items": {"$push": "$name"}
        }},
        {"$limit": 1}
    ]

    result = list(collection.aggregate(pipeline))

    if result:
        latest_archived_at = result[0]["latest_archived_at"]
        items = result[0]["items"]
        message = f"\n".join([f"- {item}" for item in items])
    else:
        message = "No archived items found."
    
    # Reply with the generated message
    await update.message.reply_text(message)
    
    # Attempt to delete the user's message after sending the reply
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    except Exception as e:
        print(f"Error deleting user's message: {e}")  # Handle deletion error if necessary