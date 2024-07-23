# common.py

# Importing from the telegram package
from telegram import Update
from telegram.ext import ContextTypes

# Import datetime if you're using it across multiple modules
from datetime import datetime

# Importing logging and configuring it here if used globally
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import database utilities if they're centralized
from .database import get_collection_for_chat

# Import global variables or utilities
# from .globals import awaiting_responses  # Example for global variables

# Re-export
__all__ = [
    "Update",
    "ContextTypes",
    "datetime",
    "logger",
    "get_collection_for_chat",
    # "awaiting_responses",  # Uncomment if using global variables
]