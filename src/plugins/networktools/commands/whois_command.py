"""
whois 指令处理
"""
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Option
from arclet.alconna import Arparma
from nonebot.exception import FinishedException

from ..func.whois import whois_query
from ..func.text_format import format_whois_result

whois_cmd = Alconna(
    "whois",  # 主命令
    Args["domain?", str],  # 域名
    Option("-r|--raw", help_text="显示原始WHOIS数据"),  # 选项：显示原始数据
)

whois_cmd_matcher = on_alconna(whois_cmd)

@whois_cmd_matcher.handle()
async def handle_whois(result: Arparma):
    try:
        # 获取域名参数
        domain = result.main_args.get("domain")
        if not domain:
            msg = "--- WHOIS ---"
            msg += "\n"
            msg += "用法: whois 域名 -r(可选: 显示原始数据)"
            await whois_cmd_matcher.finish(msg)
            return
        
        # 检查是否显示原始数据
        raw_option = result.find("raw")

        # 执行前发送文本
        msg = "--- WHOIS ---"
        msg += "\n"
        msg += f"域名: {domain}"
        await whois_cmd_matcher.send(msg)

        # 执行 whois 查询
        whois_result = await whois_query(domain)

        # 格式化文本
        msg = format_whois_result(whois_result, raw_option)
        await whois_cmd_matcher.finish(msg)

    # 错误处理
    except FinishedException:
        raise
    except Exception as e:
        msg = f"whois 出现问题: {str(e)}"
        await whois_cmd_matcher.finish(msg)