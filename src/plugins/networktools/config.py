from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    DATA_PATH: str = "data/networktools"