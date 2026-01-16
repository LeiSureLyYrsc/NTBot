"""
TCPing 指令处理
Alconna 插件并不支持合并发送
TODO:
我可能需要自行处理针对 Onebot-V11 的解析
"""
from arclet.alconna import Arparma
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Option
from nonebot.exception import FinishedException

from ..func.tcping import tcp_ping, parse_host_port
from ..func.text_format import format_tcping_result

tcping_cmd = Alconna(
    "tcping",  # 主命令
    Args["host?", str],  # 地址
    Args["port?", int],  # 端口
    Args["count?", int],  # 次数
    Args["timeout?", float],  # 超时
    Option("-p|--port", Args["port", int]),  # 选项：端口
    Option("-c|--count", Args["count", int]),  # 选项
    Option("-t|--timeout", Args["timeout", float]),  # 选项：超时
)

tcping_cmd_matcher = on_alconna(tcping_cmd)

@tcping_cmd_matcher.handle()
async def handle_tcping_cmd(result: Arparma):
    try:
        host_arg = result.main_args.get("host")
        if not host_arg:
            msg = "请提供主机地址"
            await tcping_cmd_matcher.finish(msg)
            return
        
        # 获取选项参数
        opt_port = result.query[int]("port.port")
        opt_count = result.query[int]("count.count")
        opt_timeout = result.query[float]("timeout.timeout")

        # 获取位置参数
        pos_port = result.main_args.get("port")
        pos_count = result.main_args.get("count")
        pos_timeout = result.main_args.get("timeout")

        # 解析主机和端口
        host, port_from_host = parse_host_port(host_arg)

        # 确定最终参数
        port = None
        count = 4
        timeout = 3.0

        # 基于 -c -p -t 选项的格式
        if opt_port or opt_count or opt_timeout:
            port = opt_port or port_from_host
            count = opt_count or 4
            timeout = opt_timeout or 3.0

        # 若为 地址:端口 格式
        elif ':' in host_arg:
            port = port_from_host
            if pos_count:
                count = pos_count
            if pos_timeout:
                timeout = pos_timeout

        # 若为 host port count timeout 格式
        elif pos_port:
            port = pos_port
            if pos_count:
                count = pos_count
            if pos_timeout:
                timeout = pos_timeout
        else:
            port = port_from_host

        # 检查是否有提供端口号
        if port is None:
            msg = "参数内未提供端口号"
            msg += "\n"
            msg += "用法: tcping 主机:端口 次数 超时时间(秒)"
            await tcping_cmd_matcher.finish(msg)
            return
        
        # 检查端口参数是否合法
        if port <1 or port > 65535:
            msg = "端口号必须在 1 到 65535 之间"
            await tcping_cmd_matcher.finish(msg)
            return
        
        # 检查次数参数是否合法
        if count < 1 or count > 50:
            msg = "次数必须在 1 到 50 之间"
            await tcping_cmd_matcher.finish(msg)
            return
        
        # 检查超时时间参数是否合法
        if timeout < 0.1 or timeout > 20.0:
            msg = "超时时间必须在 0.1 到 20.0 秒之间"
            await tcping_cmd_matcher.finish(msg)
            return
        
        # 发送执行操作前文本
        msg = "--- TCPing ---"
        msg += "\n"
        msg += f"地址: {host}:{port},次数: {count},超时: {timeout} 秒"
        await tcping_cmd_matcher.send(msg)

        # 执行 TCPing
        result = await tcp_ping(host, port, count, timeout)

        # 格式化文本
        msg = format_tcping_result(result)
        await tcping_cmd_matcher.finish(msg)

    # 错误处理
    except FinishedException:
        raise
    except Exception as e:
        msg = f"TCPing 出现问题: {str(e)}"
        await tcping_cmd_matcher.finish(msg)
        return