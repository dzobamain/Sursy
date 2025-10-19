# test/save_settings.py

from data.json_io import save_to_json, load_from_json
from data.settings import Settings
from config import Config

def start_test():
    settings = Settings()
    settings.by_default()
    
    save_to_json(settings, Config.SETTINGS_PATH)
    load_from_json(settings, Config.SETTINGS_PATH)
    
    print(settings.__dict__)

if __name__ == "__main__":
    start_test()