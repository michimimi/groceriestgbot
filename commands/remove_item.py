from utils.database import get_collection_for_chat
from utils.common import Update, ContextTypes, datetime, logger, get_collection_for_chat
from globals import last_message_ids, current_categories
from commands.list_items import list_items

async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    user = update.effective_user
    identifier = str(chat_id) if chat_type in ['group', 'supergroup'] else user.username if user.username else str(user.id)

    current_category = current_categories.get(chat_id, "groceries")
    collection = get_collection_for_chat(chat_id, current_category)
    
    if context.args:
        args = context.args
        deletion_indices = []
        for arg in args:
            if arg.isdigit():
                deletion_index = int(arg) - 1
                deletion_indices.append(deletion_index)
            else:
                await update.message.reply_text("All arguments must be numbers. Please try again.")
                return

        user_items = collection.find({"archived": {"$ne": True}})
        sorted_items_list = sorted(list(user_items), key=lambda x: x['name'].lower())
        deletion_indices = sorted(set(deletion_indices), reverse=True)  # Remove duplicates and sort in descending order

        for index_to_delete in deletion_indices:
            if 0 <= index_to_delete < len(sorted_items_list):
                item_to_delete = sorted_items_list[index_to_delete]
                result = collection.delete_one({"_id": item_to_delete['_id']})
                if result.deleted_count == 0:
                    await update.message.reply_text(f"There was an error deleting '{item_to_delete['name']}'. Please try again.")
            else:
                await update.message.reply_text("One or more selections were invalid. Not all items have been deleted.")
                break  # Break out of the loop if an invalid index is encountered

        # Send a confirmation message if at least one item was deleted
        if deletion_indices:
            await update.message.reply_text("Requested items have been deleted.")
    else:
        await update.message.reply_text("Please provide item numbers to delete. Usage: /remove <number> [<number> ...]")

    await list_items(update, context)
    await try_delete_message(context, chat_id, update.message.message_id)
    
async def try_delete_message(context, chat_id, message_id):
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logger.error(f"Could not delete message {message_id} in chat {chat_id}: {e}")