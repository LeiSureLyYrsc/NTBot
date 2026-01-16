from typing import Dict

def format_tcping_result(result: Dict) -> str:
    """
    格式化TCP Ping结果为可读文本
    """
    msg = "--- TCPing ---\n"
    msg += f"目标: {result['host']}:{result['port']}\n"
    
    # 显示每次 ping 的结果
    for i, elapsed in enumerate(result['times'], 1):
        if elapsed is not None:
            msg += f"{i}: 连接成功 - 耗时 {elapsed:.2f}ms\n"
        else:
            msg += f"{i}: 连接失败 - 超时\n"
    
    msg += "\n--- 统计信息 ---\n"
    msg += f"发送: {result['count']} 次 "
    msg += f"成功: {result['success_count']}次 "
    msg += f"失败: {result['failed_count']}次\n"
    msg += f"丢包率: {result['loss_rate']:.1f}%\n"
    
    # 只在有成功的连接时显示延迟统计
    if result['success_count'] > 0:
        msg += f"最小延迟: {result['min_time']:.2f}ms "
        msg += f"最大延迟: {result['max_time']:.2f}ms "
        msg += f"平均延迟: {result['avg_time']:.2f}ms"
    
    return msg

def format_nslookup_result(result: Dict) -> str:
    """
    格式化DNS查询结果为可读文本
    """
    if not result["success"]:
        msg = "--- nslookup ---\n"
        msg += f"域名: {result['domain']}\n"
        msg += f"类型: {result['type']}\n"
        msg += f"错误: {result['error']}"
        return msg
    
    msg = "--- nslookup ---\n"
    msg += f"域名: {result['domain']}\n"
    msg += f"类型: {result['type']}\n"
    msg += "记录:\n"
    
    # 显示查询结果
    for i, record in enumerate(result['records'], 1):
        if isinstance(record, dict):
            # 格式化复杂记录（如MX、SRV）
            record_str = ", ".join([f"{k}: {v}" for k, v in record.items()])
            msg += f"{i}: {record_str}\n"
        else:
            msg += f"{i}: {record}\n"
    
    return msg

def format_whois_result(result: Dict, raw_option: bool = False) -> str:
    """
    格式化WHOIS查询结果为可读文本
    """
    if not result["success"]:
        msg = "--- WHOIS ---\n"
        msg += f"域名: {result['domain']}\n"
        msg += f"错误: {result['error']}"
        return msg
    
    msg = "--- WHOIS ---\n"
    msg += f"域名: {result['domain']}\n\n"

    # 如果有原始数据选项，准备附加文本
    raw_msg = None
    
    parsed = result.get('parsed_data', {})
    
    if parsed.get('registrar'):
        msg += f"注册商: {parsed['registrar']}\n"
    if parsed.get('creation_date'):
        msg += f"创建日期: {parsed['creation_date']}\n"
    if parsed.get('expiration_date'):
        msg += f"过期日期: {parsed['expiration_date']}\n"
    if parsed.get('updated_date'):
        msg += f"更新日期: {parsed['updated_date']}\n"
    
    if parsed.get('name_servers'):
        msg += "\n域名服务器:\n"
        for i, ns in enumerate(parsed['name_servers'], 1):
            msg += f"{i}: {ns}\n"
    
    if parsed.get('status'):
        msg += "\n状态:\n"
        for i, status in enumerate(parsed['status'], 1):
            msg += f"{i}: {status}\n"
    
    if raw_option and result.get('raw_data'):
        raw_msg = "WHOIS 原始数据:\n"
        raw_msg += result['raw_data']
    
    return msg, raw_msg