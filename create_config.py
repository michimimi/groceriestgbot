import yaml
import time

def main():
    # Introduce a 3-second delay before starting the prompts
    print("Preparing to create the configuration file...")
    time.sleep(3)
    
    # Collect user input for the configuration
    config = {}

    config['telegram_bot_token'] = input("Enter your Telegram bot token: ")
    config['mongodb_uri'] = input("Enter your MongoDB URI: ")
    config['database_name'] = input("Enter your database name: ")

    # Write the configuration to a YAML file
    with open("config.yaml", 'w') as file:
        yaml.dump(config, file)

    print("config.yaml has been created successfully.")

if __name__ == "__main__":
    main()