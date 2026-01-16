from plugins.networktools.func.tcping import tcp_ping
import asyncio

async def main():
    result = await tcp_ping("baidu.com", 80)
    return result

if __name__ == "__main__":
    # 运行测试
    result = asyncio.run(main())
    print(f"TCPing 结果: {result}")