from telegram.ext import ContextTypes
from utils.database import get_collection_for_chat
from globals import current_categories
from datetime import datetime
from commands.list_items import list_items

async def add_item(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    current_category = current_categories.get(chat_id, "groceries")
    collection = get_collection_for_chat(chat_id, current_category)
    
    item_name = " ".join(context.args).strip()
    if not item_name:
        await update.message.reply_text("Please provide an item name to add. Usage: /add <item name>")
        return

    normalized_item_name = item_name.lower()
    
    # First, check if the item exists and is archived
    archived_item = collection.find_one({"name_normalized": normalized_item_name, "archived": True})
    if archived_item:
        # If the item exists and is archived, unarchive it
        collection.update_one(
            {"_id": archived_item["_id"]},
            {"$set": {"archived": False, "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}
        )
        await update.message.reply_text(f"Added '{item_name}' to your list!")
    else:
        # Check if the item exists and is not archived
        existing_item = collection.find_one({"name_normalized": normalized_item_name, "archived": False})
        if existing_item:
            await update.message.reply_text(f"'{item_name}' is already in your list.")
            return

        # If the item does not exist, insert it as a new item
        collection.insert_one({
            "name": item_name,
            "name_normalized": normalized_item_name,
            "added_by": update.effective_user.username or update.effective_user.id,
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "archived": False
        })

        await update.message.reply_text(f"Added '{item_name}' to your list!")

    # Optionally, you can call list_items to show the updated list
    await list_items(update, context)
