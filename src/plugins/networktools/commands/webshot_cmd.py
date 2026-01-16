"""
网页截图 指令处理
"""
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Image
from arclet.alconna import Arparma
from nonebot.exception import FinishedException

from ..func.webshot import web_screenshot
from ..func.text_format import format_webshot_result

webshot_cmd = Alconna(
    "webshot",  # 主命令
    Args["url?", str],  # URL
    Args["width?", int],  # 宽度
    Args["height?", int],  # 高度
)

webshot_cmd_matcher = on_alconna(webshot_cmd, use_cmd_start=True, aliases=["screenshot", "网页截图"])

@webshot_cmd_matcher.handle()
async def handle_webshot(result: Arparma):
    try:
        # 获取 URL 参数
        url = result.main_args.get("url")
        if not url:
            msg = "--- 网页截图 ---"
            msg += "\n"
            msg = "用法: webshot URL"
            await webshot_cmd_matcher.finish(msg)
            return
        
        # 如果没有 http 头,则帮助添加
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # 获取宽度和高度参数
        width = result.main_args.get("width") or 1920
        height = result.main_args.get("height") or 1080

        # 执行前发送文本
        msg = "--- 网页截图 ---"
        msg += "\n"
        msg += f"URL: {url}, 宽: {width}, 高: {height}"
        await webshot_cmd_matcher.send(msg)

        # 执行网页截图
        webshot_result = await web_screenshot(url, width, height)

        # 检查结果
        if not webshot_result["success"]:
            output = format_webshot_result(webshot_result, width, height)
            await webshot_cmd_matcher.finish(output)
            return
        
        # 格式化文本结果
        text_output = format_webshot_result(webshot_result, width, height)

        # 发送截图
        if webshot_result.get("screenshot_bytes"):
            msg = text_output + "\n"
            msg += Image(raw=webshot_result["screenshot_bytes"])
            await webshot_cmd_matcher.finish(msg)
        else:
            await webshot_cmd_matcher.finish(text_output)

    # 错误处理
    except FinishedException:
        raise
    except Exception as e:
        msg = f"网页截图 出现问题: {str(e)}"
        await webshot_cmd_matcher.finish(msg)