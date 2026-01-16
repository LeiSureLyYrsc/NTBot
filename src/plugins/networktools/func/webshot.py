"""
网页截图 模块
"""

from typing import Dict
from nonebot_plugin_htmlrender import get_new_page

async def web_screenshot(url: str, width: int, height: int) -> Dict:
    """
    异步截取网页截图
    """
    try:
        # 使用 htmlrender 获取页面并截图
        async with get_new_page(viewport={"width": width, "height": height}) as page:
            # 访问 URL，等待网络空闲
            await page.goto(url, wait_until="networkidle")
            
            # 截取整页
            screenshot_bytes = await page.screenshot(full_page=True, type="png")
        
        return {
            "success": True,
            "url": url,
            "screenshot_bytes": screenshot_bytes
        }
            
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e)
        }