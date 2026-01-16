"""
TCPing 模块
"""
import asyncio
import time
from typing import Dict, Optional, Callable

def parse_host_port(host_str: str, port_arg: int = None) -> tuple:
    """
    解析主机和端口
    支持 host:port 格式
    """
    if ':' in host_str:
        parts = host_str.rsplit(':', 1)
        try:
            return parts[0], int(parts[1])
        except (ValueError, IndexError):
            return host_str, port_arg
    return host_str, port_arg

async def tcp_ping(
    host: str,  # 地址
    port: int,  # 端口
    count: int = 4,  # 次数
    timeout: float = 3.0,  # 超时时间(秒)
    callback: Optional[Callable] = None  # 进度回调函数
) -> Dict:
    """
    异步 TCPing
    """

    # 结果初始化
    results = {
        "host": host,
        "port": port,
        "count": count,
        "success_count": 0,
        "failed_count": 0,
        "times": [],
        "avg_time": 0,
        "min_time": float('inf'),
        "max_time": 0,
        "loss_rate": 0
    }
    
    async def single_ping(index: int) -> tuple:
        """单次 TCPing"""
        start_time = time.perf_counter()

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout
            )
            writer.close()
            await writer.wait_closed()

            elapsed = (time.perf_counter() - start_time) * 1000  # 转为毫秒
            return (index, elapsed)
        
        except (asyncio.TimeoutError, Exception):
            return (index, None)
        
    # asyncio.gather 并发,间隔 0.2s
    tasks = []
    for i in range(count):
        tasks.append(single_ping(i))
        await asyncio.sleep(0.2)  # 短暂间隔，避免过载

    # 等待任务完成
    ping_results = await asyncio.gather(*tasks)

    # 按顺序处理结果
    for index, elapsed in sorted(ping_results, key=lambda x: x[0]):
        results["times"].append(elapsed)

        if elapsed is not None:
            results["success_count"] += 1
            results["avg_time"] += elapsed
            results["min_time"] = min(results["min_time"], elapsed)
            results["max_time"] = max(results["max_time"], elapsed)

            # 回调进度
            if callback:
                await callback(index + 1, elapsed)
        else:
            results["failed_count"] += 1

            # 回调进度
            if callback:
                await callback(index + 1, None)
    
    # 计算其他数据
    valid_times = [t for t in results["times"] if t is not None]
    if valid_times:
        results["avg_time"] = sum(valid_times) / len(valid_times)
    else:
        results["min_time"] = 0

    results["loss_rate"] = (results["failed_count"] / count) * 100

    return results