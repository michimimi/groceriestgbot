import yaml
from pymongo import MongoClient

def load_config(config_file="config.yaml"):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# MongoDB Setup
client = MongoClient(config['mongodb_uri'])
db = client[config['database_name']]
orders_collection = db.orders  # A separate collection for orders

def get_collection_for_chat(chat_id, category="groceries"):
    normalized_chat_id = str(chat_id).replace("-", "neg")
    collection_name = f"{category}_{normalized_chat_id}_items"
    return db[collection_name]