from mcstatus import JavaServer, BedrockServer


def minecraft_server(domain: str):
    if ':' in domain:
        host, port_str = domain.split(':')
        port = int(port_str)
        java_status, = status_java_server(host, port)
        bedrock_status = status_bedrock_server(host, port)
    else:
        host = domain
        java_status = status_java_server(host)
        bedrock_status = status_bedrock_server(host)

    return {
        "java_status": java_status,
        "bedrock_status": bedrock_status
    }

def status_java_server(host: str, port: int = 25565):
    try:
        server = JavaServer(host, port, timeout=2)
        status = server.status()
        status.raw["latency"] = str(int(status.latency)) + " ms"
        status.raw["online"] = True
        return status.raw
    except Exception as e:
        return {"online": False, "error": str(e)}

def status_bedrock_server(host: str, port: int = 19132):
    try:
        server = BedrockServer(host, port, timeout=2)
        status = server.status()
        status.raw["latency"] = str(int(status.latency)) + " ms"
        status.raw["online"] = True
        return status.raw
    except Exception as e:
        return {"online": False, "error": str(e)}