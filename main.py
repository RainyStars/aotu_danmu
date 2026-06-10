import json
import time
import random
from danmu import log, DanmuClient, check_room_status


def load_config():
    """加载配置"""
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    config = load_config()
    room_id = config["room_id"]
    cookie = config["cookie"]
    danmaku_list = config["danmaku"]

    log(f"监控房间: {room_id}")
    log(f"弹幕列表: {danmaku_list}")

    client = DanmuClient(room_id, cookie)

    while True:
        if check_room_status(room_id):
            log("直播间: 在线")

            danmu = random.choice(danmaku_list)
            client.send_danmu(danmu)
        else:
            log("直播间: 离线")

        interval = random.randint(10, 180)
        log(f"等待 {interval} 秒")
        time.sleep(interval)


if __name__ == "__main__":
    main()