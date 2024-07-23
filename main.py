from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import logging
import yaml
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from commands.list_items import list_items
from commands.clear_items import clear_items
from commands.add_item import add_item
from commands.remove_item import remove_item
from commands.list_last_archived import list_last_archived
from utils.message_handlers import handle_text
from globals import current_categories

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def load_config(config_file="config.yaml"):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

async def change_category(update, context):
    keyboard = [
        [InlineKeyboardButton("Groceries", callback_data='groceries')],
        [InlineKeyboardButton("Household Supplies", callback_data='household_supplies')],
        [InlineKeyboardButton("Things to Remember", callback_data='things_to_remember')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id 
    
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    except Exception as e:
        pass

    sent_message = await context.bot.send_message(chat_id=chat_id, text='Please select a category:', reply_markup=reply_markup)

    context.user_data['last_category_message_id'] = sent_message.message_id
async def category_callback(update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    current_categories[chat_id] = query.data

    if 'last_category_message_id' in context.user_data:
        await context.bot.delete_message(chat_id=chat_id, message_id=context.user_data['last_category_message_id'])
        del context.user_data['last_category_message_id'] 
    await list_items(update, context)
    
def main() -> None:
    config = load_config()
    token = config['telegram']['token']
    application = Application.builder().token(token).build()

    del_variations = ["delete", "remove", "del"] 
    category_variations = ["category", "c", "change"] 


    # Register command handlers
    application.add_handler(CommandHandler("list", list_items))
    application.add_handler(CommandHandler("clear", clear_items))
    application.add_handler(CommandHandler("add", add_item))
    application.add_handler(CallbackQueryHandler(category_callback))


    for command in category_variations:
        application.add_handler(CommandHandler(command, change_category))
    for command in del_variations:
        application.add_handler(CommandHandler(command, remove_item))

    application.add_handler(CommandHandler("lastorder", list_last_archived))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

if __name__ == "__main__":
    main()
