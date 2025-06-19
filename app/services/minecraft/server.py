from mcstatus import JavaServer
from mcstatus import BedrockServer
from tcping import Ping
import re


def minecraft_server(domain: str):
    if ':' in domain:
        host, port_str = domain.split(':')
        port = int(port_str)
        java_ping = ping_java_server(host, port)
        java_status = status_java_server(host, port)
        bedrock_status = status_bedrock_server(host, port)
    else:
        host = domain
        java_ping = ping_java_server(host)
        java_status = status_java_server(host)
        bedrock_status = status_bedrock_server(host)

    return {
        "java_ping": java_ping,
        "java_status": java_status,
        "bedrock_status": bedrock_status
    }

def ping_java_server(host: str, port: int = 25565):
    try:
        ping = Ping(host, port)
        ping.ping(4)
        result = ping.result.raw
        match = re.search(r'average = (\d+\.\d+)ms', result)
        if match:
            if match.group(1) == "0.0":
                return "timeout"
            else:
                return match.group(1)
        return result
    except Exception as e:
        return f"error：{str(e)}"

def status_java_server(host: str, port: int = 25565):
    try:
        server = JavaServer.lookup(host, port)
        status = server.status()
        return status.raw
    except Exception as e:
        return {"online": False, "error": str(e)}

def status_bedrock_server(host: str, port: int = 19132):
    try:
        server = BedrockServer.lookup(host, port)
        status = server.status()
        return status.raw
    except Exception as e:
        return {"online": False, "error": str(e)}