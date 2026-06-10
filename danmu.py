import json
import time
from datetime import datetime


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


class DanmuClient:
    """B站弹幕客户端"""

    def __init__(self, room_id, cookie):
        self.room_id = room_id
        self.cookie = cookie
        self.uid = 0

    def send_danmu(self, text):
        """发送弹幕"""
        import requests

        # 从cookie中提取csrf token
        csrf = ''
        for item in self.cookie.split(';'):
            if 'bili_jct' in item:
                csrf = item.split('=')[1].strip()
                break

        url = 'https://api.live.bilibili.com/msg/send'
        data = {
            'color': '16777215',
            'fontsize': '25',
            'mode': '1',
            'msg': text,
            'rnd': str(int(time.time())),
            'roomid': self.room_id,
            'bubble': '0',
            'csrf_token': csrf,
            'csrf': csrf,
        }
        headers = {
            'cookie': self.cookie,
            'origin': 'https://live.bilibili.com',
            'referer': f'https://live.bilibili.com/{self.room_id}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        }

        try:
            resp = requests.post(url, data=data, headers=headers, timeout=10)
            result = resp.json()
            if result.get("code") == 0:
                log(f"发送弹幕: {text}")
                return True
            else:
                log(f"发送弹幕失败: {result.get('message')}")
                return False
        except Exception as e:
            log(f"发送弹幕异常: {e}")
            return False

    def close(self):
        """关闭连接（无需操作）"""
        pass


def check_room_status(room_id):
    """检查直播间状态"""
    import requests
    headers = {
        'Referer': 'https://live.bilibili.com/',
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        resp = requests.get(
            f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}",
            headers=headers,
            timeout=10
        )
        data = resp.json()
        if data.get("code") == 0:
            return data["data"].get("live_status") == 1
        return False
    except:
        return False