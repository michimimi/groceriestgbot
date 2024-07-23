from utils.common import Update, ContextTypes, datetime, logger, get_collection_for_chat
from globals import current_categories

async def clear_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    user = update.effective_user
    identifier = str(chat_id) if chat_type in ['group', 'supergroup'] else user.username if user.username else str(user.id)

    current_category = current_categories.get(chat_id, "groceries")
    collection = get_collection_for_chat(chat_id, current_category)
        
    # Find items that are not already archived (i.e., do not have an 'archived_at' field or it's empty)
    items_to_archive = collection.find({"$or": [{"archived_at": {"$exists": False}}, {"archived_at": []}]})
    items_list = list(items_to_archive)

    if items_list:
        result = collection.update_many(
            {"$or": [{"archived_at": {"$exists": False}}, {"archived_at": []}]},
        {
            "$set": {"archived": True},  # Set the item as archived
            "$push": {"archived_at": datetime.now()}  # Push current timestamp to 'archived_at' array
        }
    )

    if result.modified_count > 0:
        await update.message.reply_text(f"All items have now been archived.")
    else:
        await update.message.reply_text("There was a problem archiving the items. Please try again.")

    try:
        # Attempt to delete the command message itself, to keep the chat clean
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    except Exception as e:
        logger.error(f"Error deleting user's command message: {e}")
