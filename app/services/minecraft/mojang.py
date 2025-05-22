import requests
from app.models.minecraft.Player import Player


def get_uuid(name):
    """
    获取玩家的UUID
    :param name: 玩家名称
    :return: UUID
    """
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def get_profile(name):
    """
    获取玩家的皮肤和头像
    :param uuid: 玩家UUID
    :return: 皮肤和头像的URL
    """
    uuid_data = get_uuid(name)
    if uuid_data is None:
        return None
    uuid = uuid_data.get("id")
    if uuid is None:
        return None
    legacy = uuid_data.get("legacy", False)
    demo = uuid_data.get("demo", False)

    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        properties = data.get("properties", [])
        for prop in properties:
            if prop.get("name") == "textures":
                value = prop.get("value")
                return Player(name=name, uuid=uuid, value=value, legacy=legacy, demo=demo)
    return None
