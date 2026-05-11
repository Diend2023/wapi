"""
HXWZ 口令服务端
管理口令存储、生成、验证。
"""
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# 加密密钥（与客户端共用，通过环境变量配置）
SECRET_KEY = os.environ.get("HXWZ_SECRET_KEY", "sda-getter-hxwz-auth-2026")

# 口令存储文件
_TOKEN_FILE = Path(__file__).resolve().parent / "token.json"


def _xor_encrypt(plaintext: str) -> str:
    """简单的 XOR 加密（对称）"""
    key_bytes = SECRET_KEY.encode()
    pt_bytes = plaintext.encode()
    encrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(pt_bytes))
    return encrypted.hex()


def _xor_decrypt(hex_str: str) -> str:
    """XOR 解密"""
    key_bytes = SECRET_KEY.encode()
    encrypted = bytes.fromhex(hex_str)
    decrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(encrypted))
    return decrypted.decode()


def _load_token_data() -> Optional[dict]:
    """从文件加载口令数据"""
    if not _TOKEN_FILE.exists():
        return None
    try:
        with open(_TOKEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 兼容旧格式 {"token": "xxx"} -> {"plaintext": "xxx"}
        if "token" in data and "plaintext" not in data:
            data["plaintext"] = data["token"]
        if "encrypted" not in data and "plaintext" in data:
            data["encrypted"] = _xor_encrypt(data["plaintext"])
        if "updated_at" not in data:
            data["updated_at"] = ""
        return data
    except (json.JSONDecodeError, IOError):
        return None


def _save_token_data(plaintext: str) -> None:
    """保存口令到文件"""
    _TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "plaintext": plaintext,
        "encrypted": _xor_encrypt(plaintext),
        "updated_at": datetime.now().isoformat(),
    }
    with open(_TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_token_info() -> Optional[dict]:
    """获取当前口令信息"""
    data = _load_token_data()
    if data is None:
        return None
    return {
        "encrypted": data["encrypted"],
        "updated_at": data.get("updated_at", ""),
    }


def verify_token(user_input: str) -> dict:
    """
    验证用户输入的口令。
    返回 {"success": bool, "plaintext": str, "encrypted": str}
    """
    data = _load_token_data()
    if data is None:
        return {"success": False, "error": "服务端未配置口令"}

    plaintext = data["plaintext"]
    encrypted = data["encrypted"]

    if user_input == plaintext:
        return {
            "success": True,
            "plaintext": plaintext,
            "encrypted": encrypted,
        }
    else:
        return {"success": False, "error": "口令错误"}


def set_token(plaintext: str) -> dict:
    """设置/更新口令"""
    _save_token_data(plaintext)
    return {"success": True, "message": "口令已更新"}


def decrypt_token(encrypted: str) -> str:
    """解密口令"""
    return _xor_decrypt(encrypted)


def has_token() -> bool:
    """检查是否已配置口令"""
    return _load_token_data() is not None


# ---- 接口别名（供 endpoint 调用） ----

def get_current_token() -> Optional[str]:
    """获取当前明文口令"""
    data = _load_token_data()
    if data is None:
        return None
    return data.get("plaintext")


def encrypt_token(plaintext: str) -> str:
    """加密明文口令"""
    return _xor_encrypt(plaintext)
