"""
nslookup 模块
"""

from typing import Dict
import dns.resolver
import dns.asyncresolver

# 支持的 DNS 记录类型
SUPPORTED_RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA", "PTR", "SRV"]

async def nslookup(domain: str, record_type: str = "A") -> Dict:
    """
    异步 nslookup
    """
    nxdomain = "记录不存在"
    no_answer = "没有找到对应的记录"
    timeout = "查询超时"

    try:
        resolver = dns.asyncresolver.Resolver()
        resolver.timeout = 5  # 解析超时时间
        resolver.lifetime = 5  # 总超时时间

        answers = await resolver.resolve(domain, record_type)

        # 结果初始化
        results = {
            "domain": domain,
            "type": record_type,
            "success": True,
            "records": []
        }

        # 针对不同记录类型处理结果
        for rdata in answers:
            if record_type == "MX":
                results["records"].append({
                    "preference": rdata.preference,
                    "exchange": str(rdata.exchange)
                })
            elif record_type == "SOA":
                results["records"].append({
                    "mname": str(rdata.mname),
                    "rname": str(rdata.rname),
                    "serial": rdata.serial
                })
            elif record_type == "SRV":
                results["records"].append({
                    "priority": rdata.priority,
                    "weight": rdata.weight,
                    "port": rdata.port,
                    "target": str(rdata.target)
                })
            else:
                results["records"].append(str(rdata))

    # 错误处理
    except dns.resolver.NXDOMAIN:  # 域名不存在
        results = {
            "domain": domain,
            "type": record_type,
            "success": False,
            "error": nxdomain
        }
    except dns.resolver.NoAnswer:  # 无对应记录
        results = {
            "domain": domain,
            "type": record_type,
            "success": False,
            "error": no_answer
        }
    except dns.resolver.Timeout:  # 查询超时
        results = {
            "domain": domain,
            "type": record_type,
            "success": False,
            "error": timeout
        }
    # 其他错误
    except Exception as e:
        results = {
            "domain": domain,
            "type": record_type,
            "success": False,
            "error": str(e)
        }

    return results