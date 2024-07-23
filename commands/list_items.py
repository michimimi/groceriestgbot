from utils.database import get_collection_for_chat
from utils.common import Update, ContextTypes, datetime, logger
from globals import last_message_ids, current_categories

async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Determine chat_id based on update source
    chat_id = None
    if update.message:
        chat_id = update.message.chat_id
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id
        # Acknowledge callback query if not already done
        await update.callback_query.answer()
    else:
        logger.error("list_items was called without a valid update.message or update.callback_query")
        return  # Exit the function if chat_id could not be determined

    current_category = current_categories.get(chat_id, "groceries")
    collection = get_collection_for_chat(chat_id, current_category)

    # Delete the previous list message if it exists
    if chat_id in last_message_ids:
        try:
            await context.bot.delete_message(chat_id, last_message_ids[chat_id])
        except Exception as e:
            logger.error(f"Error deleting previous list message: {e}")

    user_items = collection.find({"archived": {"$ne": True}})
    items_list = list(user_items)  # Convert cursor to list directly without 'await'
    
    # Sort the items alphabetically by name
    sorted_items_list = sorted(items_list, key=lambda x: x['name'].lower())

    # Dynamically include the category in the message
    category_display = current_category.replace('_', ' ').capitalize()
    message = f"Your {category_display} list is empty."
    if sorted_items_list:
        # Enumerate the sorted list to add numbering and construct the message
        message_lines = [f"{idx + 1}. {item['name']}" for idx, item in enumerate(sorted_items_list)]
        message = f"Your {category_display} list:\n" + "\n".join(message_lines)
    
    # Send the list message
    if chat_id:
        sent_message = await context.bot.send_message(chat_id, message)
        # Store the new message's ID
        last_message_ids[chat_id] = sent_message.message_id

    # Attempt to delete the user's command message, applicable only for message updates
    if update.message:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        except Exception as e:
            logger.error(f"Error deleting user's command message: {e}")