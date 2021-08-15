import os
import pathlib

from dotenv import load_dotenv
from omegaconf import OmegaConf, dictconfig


def create_item_choice():
    def load_config() -> dictconfig.DictConfig:
        load_dotenv()
        config_path = os.getenv(
            "CONFIG_PATH", pathlib.Path(__file__).parent.parent / "config.yaml"
        )
        config = OmegaConf.load(config_path)
        return config

    config = load_config()
    choice = tuple([tuple(item) for item in config.item])
    return choice


if __name__ == "__main__":
    choice = create_item_choice()
    print(choice)
