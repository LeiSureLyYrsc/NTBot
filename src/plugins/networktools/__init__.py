from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from pathlib import Path
import json

from .config import Config

# 导入其他模块
from . import __main__ as __main__
from .commands import tcping_cmd as tcping_cmd
from .commands import nslookup_cmd as nslookup_cmd
from .commands import whois_cmd as whois_cmd
from .commands import webshot_cmd as webshot_cmd

__plugin_meta__ = PluginMetadata(
    name="NetworkTools",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 确保数据目录存在
data_path = Path(config.DATA_PATH)
data_path.mkdir(parents=True, exist_ok=True)

# 配置文件存储路径
config_file = data_path / "config.json"

# 默认配置
default_config = {
    "language": "cn"  # 默认语言为简体中文
}

# 初始化配置文件
if not config_file.exists():
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)
