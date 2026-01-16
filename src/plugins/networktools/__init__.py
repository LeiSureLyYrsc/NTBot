from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

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

