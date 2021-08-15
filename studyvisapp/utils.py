import os
import pathlib

from dotenv import load_dotenv
from omegaconf import OmegaConf, dictconfig
from django.core.management.utils import get_random_secret_key


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


def create_key():
    secret_key = get_random_secret_key()
    secret_key = "SECRET_KEY = '{0}'".format(secret_key)
    print(secret_key)
    return secret_key


if __name__ == "__main__":
    create_key()
