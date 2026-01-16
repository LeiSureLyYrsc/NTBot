"""
nslookup 指令处理
"""
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Option
from arclet.alconna import Arparma
from nonebot.exception import FinishedException

from ..func.nslookup import nslookup, SUPPORTED_RECORD_TYPES
from ..func.text_format import format_nslookup_result

nslookup_cmd = Alconna(
    "nslookup",  # 主命令
    Args["domain?", str],  # 域名
    Args["server?", str],  # 记录类型,默认为 A
    Option("-t|--type", Args["type", str]),  # 选项：记录类型
)

nslookup_cmd_matcher = on_alconna(nslookup_cmd, use_cmd_start=True, aliases=["dnslookup", "dns"])

@nslookup_cmd_matcher.handle()
async def handle_nslookup_cmd(result: Arparma):
    try:
        # 获取域名参数
        domain = result.main_args.get("domain")
        if not domain:
            msg = "--- nslookup ---"
            msg += "\n"
            msg += "用法: nslookup 域名 类型(默认为 A)"
            msg += "\n"
            msg += "支持的类型: A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, SRV"
            await nslookup_cmd_matcher.finish(msg)
            return
    
        # 获取记录类型
        record_type_pos = result.main_args.get("server")
        record_type_opt = result.query[str]("type.type")
        record_type = (record_type_opt or record_type_pos or "A").upper()

        # 验证记录是否为支持类型
        if record_type not in SUPPORTED_RECORD_TYPES:
            msg = "--- nslookup ---"
            msg += "\n"
            msg += f"不支持的记录类型: {record_type}"
            await nslookup_cmd_matcher.finish(msg)
            return
        
        # 执行前发送文本
        msg = "--- nslookup ---"
        msg += "\n"
        msg += f"域名: {domain} ({record_type})"
        await nslookup_cmd_matcher.send(msg)

        # 执行 nslookup
        nslookup_result = await nslookup(domain, record_type)

        # 格式化文本
        msg = format_nslookup_result(nslookup_result)
        await nslookup_cmd_matcher.finish(msg)

    # 错误处理
    except FinishedException:
        raise
    except Exception as e:
        msg = f"nslookup 发生错误: {str(e)}"
        await nslookup_cmd_matcher.finish(msg)