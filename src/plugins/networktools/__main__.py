from arclet.alconna import Arparma
from nonebot_plugin_alconna import Alconna, Args, Subcommand, on_alconna

networktools = Alconna(
    "networktools", # 主命令
    Subcommand(
        "lang",     # 子命令
        Args["language?", str],  # 添加 ? 可以让参数变为可选项
        help_text="切换语言 / Switch language"  # 指令描述
    ),
)

nt = on_alconna(networktools)

@nt.assign("$main")
# 主命令处理
async def welcome():
    """欢迎信息"""
    msg = "NetworkTools 已加载"
    await nt.finish(msg)

@nt.assign("lang") 
# lang 子命令处理:切换语言
async def switch_language(result: Arparma):
    """切换语言"""
    language = result.query[str]("lang.language")  # 获取参数值
    if language is None:  # 如果没有提供参数 则显示当前使用的语言
        msg = "请提供要切换的语言"
        await nt.finish(msg)
    else:
        msg = f"抓取到文本: {language}"
        await nt.finish(msg)