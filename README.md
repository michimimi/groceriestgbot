# Groceries Bot

This is a Telegram bot for managing grocery lists. It allows users to add, remove, list, and clear items from their grocery lists. The bot also supports changing categories and listing archived orders.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Creating a Bot on Telegram](#creating-a-bot-on-telegram)
- [Commands](#commands)
- [Project Structure](#project-structure)

## Features

- Add items to grocery lists
- Remove items from grocery lists
- List all items in the current grocery list
- Clear the current grocery list
- Change the category of items
- List the last archived orders

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/michimimi/groceriesbot.git
    cd groceries
    ```

2. **Run the setup task:**
    This will install the dependencies and prompt you to create the configuration file.
    ```bash
    task setup
    ```

## Creating a Bot on Telegram

1. Open Telegram and search for the BotFather.
2. Start a chat with the BotFather and use the `/newbot` command to create a new bot.
3. Follow the instructions to choose a name and username for your bot.
4. Once the bot is created, you will receive a token. Save this token as it will be needed for the setup.

## Commands

- `/list` - Lists all items in the current grocery list.
- `/clear` - Clears all items in the current grocery list.
- `/add <item>` - Adds an item to the grocery list.
- `/remove <item>` - Removes an item from the grocery list.
- `/category` - Changes the category of items.
- `/lastorder` - Lists the last archived orders.
