"""
whois 模块
"""
import asyncio
import whois
from typing import Dict
from datetime import datetime

async def whois_query(domain: str) -> Dict:
    """
    异步 whois
    """
    try:
        loop = asyncio.get_event_loop()
        w = await loop.run_in_executor(None, whois.whois, domain)

        # 日期格式化
        def format_date(date_obj):
            if date_obj is None:
                return None
            if isinstance(date_obj, list):
                date_obj = date_obj[0] if date_obj else None
            if isinstance(date_obj, datetime):
                return date_obj.strftime('%Y-%m-%d %H:%M:%S')
            return str(date_obj)
        
        # 列表格式化
        def format_list(data):
            if data is None:
                return []
            if isinstance(data, list):
                return data
            return [data]
        
        # 解析数据
        parsed_data = {
            "registrar": w.registrar if isinstance(w.registrar, str) else (w.registrar[0] if w.registrar else None),
            "creation_date": format_date(w.creation_date),
            "expiration_date": format_date(w.expiration_date),
            "updated_date": format_date(w.updated_date),
            "name_servers": format_list(w.name_servers),
            "status": format_list(w.status)
        }

        return {
            "domain": domain,
            "success": True,
            "parsed_data": parsed_data,
            "raw_data": w.text if hasattr(w, 'text') else str(w)
        }
    
    # 异常处理
    except Exception as e:
        return {
            "domain": domain,
            "success": False,
            "error": str(e)
        }