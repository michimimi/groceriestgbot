
from telegram import Update
from telegram.ext import ContextTypes
from .database import get_collection_for_chat  # Adjust the import path as needed
from globals import awaiting_responses  # Adjust the import path as needed
from commands.list_items import list_items  # Adjust the import path as needed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    message_text = update.message.text.strip()

    collection = get_collection_for_chat(chat_id)

    # Check if we are awaiting a response for deletion
    if chat_id in awaiting_responses and 'action' in awaiting_responses[chat_id] and awaiting_responses[chat_id]['action'] == 'delete':
        try:
            selected_index = int(message_text) - 1  # Convert user input into an index
            if 0 <= selected_index < len(awaiting_responses[chat_id]['items']):
                item_to_delete = awaiting_responses[chat_id]['items'][selected_index]
                # Proceed with item deletion logic
                result = collection.delete_one({"_id": item_to_delete['_id']})
                if result.deleted_count > 0:
                    await update.message.reply_text(f"Deleted '{item_to_delete['name']}' from your list.")
                else:
                    await update.message.reply_text("There was an error deleting the item. Please try again.")
                
                # Clear the awaiting response state
                del awaiting_responses[chat_id]

                # Optionally, refresh the list to the user
                await list_items(update, context)
            else:
                await update.message.reply_text("Invalid selection. Please try again.")
        except ValueError:
            # If it's not a number, do nothing or handle other text as needed
            pass

    # Handle any other non-command text messages here, if needed

    # Attempt to delete the user's command message
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    except Exception as e:
        logger.error(f"Error deleting user's message: {e}")