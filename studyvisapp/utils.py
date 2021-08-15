import os
import pathlib

from dotenv import load_dotenv
from omegaconf import OmegaConf, dictconfig


def load_config() -> dictconfig.DictConfig:
    load_dotenv()
    config_path = os.getenv(
        "CONFIG_PATH", pathlib.Path(__file__).parent.parent / "config.yaml"
    )
    config = OmegaConf.load(config_path)
    return config


def create_item_choice():
    config = load_config()
    dict = config.item
    choice = tuple([tuple([item, item]) for item in dict.keys()])
    return choice


if __name__ == "__main__":
    choice = create_item_choice()
    print(choice)
