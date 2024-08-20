import os
import platform
import random
import requests
from configparser import ConfigParser
import io
import logging

# 自动判断运行环境
IS_GITHUB_ACTIONS = 'GITHUB_ACTIONS' in os.environ
IS_SERVER = platform.system() == "Linux" and not IS_GITHUB_ACTIONS

# 从配置文件或环境变量中读取配置信息
def load_config():
    config = ConfigParser()
    if IS_SERVER:
        config_file = './config.ini'
    elif IS_GITHUB_ACTIONS:
        config_file = None
    else:
        config_file = 'config.ini'
    
    if config_file and os.path.exists(config_file):
        config.read(config_file)
    
    return config

config = load_config()

HITOKOTO_URL = config.get('urls', 'hitokoto_url', fallback="https://v1.hitokoto.cn/")

# 扩充的句型模板
sentence_templates = [
    "{0}，{1}，{2}。",
]

# 扩充的词汇库
words = {
    "subject": [
        "我又来啦", "代码写累了来逛逛", "linux.do", "em....", "又是新的一天",
    ],
    "adjective": [
        "助我升级吧", "哈哈哈哈", "什么时候能升级呢", "你可以不活但是不能没有活", "佬友真是啥活都有",
    ],
    "emotion": [
        "🤩🤩🤩", "😚👏👍", "🙌💐🎆", "🎑🎏👏", "💙💙💙",
    ],
    "result": [
        "佬友啊佬友", "佬友好活跃啊", "你是从事什么行业的呢", "佬友助我升级吧", "佬友是基佬还是大佬",
    ],
}

# 扩充的表情符号
emojis = [
    "😊", "👍", "😍", "💪", "👏", "👌", "🎉", "🔥", "😄", "😃",
    "😁", "😆", "😅", "😂", "🤣", "🙂", "🙃", "😉", "😇", "🥰",
    "😘", "😗", "😙", "😚", "😋", "😜", "😝", "😛", "🤑", "😎",
    "🤩", "🥳", "🤗", "🤠", "😺", "😸", "😻", "😼", "😽", "🙌",
    "👏", "👐", "🤲", "🙏", "💐", "🌸", "🌹", "🌺", "🌻", "🌼",
    "💮", "🎆", "🎇", "✨", "🎈", "🎉", "🎊", "🎂", "🎁", "🎍",
    "🎎", "🎏", "🎐", "🎑", "🎀", "🏆", "🏅", "🥇", "🥈", "🥉",
    "🌟", "💫", "💥", "🎯", "🎖", "🎗", "🎄", "🎃", "🎋", "🎋",
    "🎐", "🎏", "🎎", "🎍", "🎀", "🎁", "💖", "💗", "💓", "💞",
    "💕", "💌", "💘", "💝", "💟", "❣", "💚", "💙", "💜", "🖤",
]

def generate_random_image_url():
    """生成一个包含随机数值的图片URL"""
    img_id = random.randint(1000, 99999)   # 随机生成图片ID
    width = random.randint(1000, 3000)      # 随机生成宽度
    height = random.randint(800, 1000)     # 随机生成高度
    return f"![IMG_{img_id}|{width}x{height}](https://api.szfx.top/acg/upyun)"

def generate_positive_sentence():
    """生成一条随机的正面句子"""
    template = random.choice(sentence_templates)
    subject = random.choice(words["subject"])
    adjective = random.choice(words["adjective"])
    emotion = random.choice(words["emotion"])
    result = random.choice(words["result"])
    sentence = template.format(subject, adjective, emotion, result)
    while len(sentence) < 10:
        sentence += random.choice(words["adjective"])
    for _ in range(random.randint(1, 3)):
        position = random.randint(0, len(sentence))
        sentence = sentence[:position] + random.choice(emojis) + sentence[position:]
    # 添加随机图片链接到句子的下一行
    sentence += "\n" + get_hitokoto()
    sentence += "\n" + generate_random_image_url()
    return sentence

def load_predefined_replies():
    """从 reply.txt 读取预定义回复"""
    try:
        with open('./reply.txt', 'r', encoding='utf-8') as file:
            predefined_replies = [line.strip() for line in file if line.strip()]
        return predefined_replies
    except FileNotFoundError:
        return []

def get_hitokoto() -> str:
    """
    从 API 获取一条一言，并返回格式化的字符串。

    Returns:
        str: 格式化的一言字符串，如 "憧憬，是距离了解最遥远的一种感情。    ----BLEACH"
    """
    try:
        response = requests.get(HITOKOTO_URL)
        response.raise_for_status()  # 如果响应状态不是 200，则抛出 HTTPError 异常
        data = response.json()
        hitokoto = data["hitokoto"]
        from_source = data["from"]
        return f"{hitokoto}    ----{from_source}"
    except requests.RequestException as e:
        logging.error(f"一条一言获取失败: {e}。")
        return ""

def generate_or_load_reply():
    """随机选择生成或读取一条回复"""
    predefined_replies = load_predefined_replies()
    if random.choice([True, False]) and predefined_replies:
        return random.choice(predefined_replies) + "\n" + get_hitokoto() + "\n" + generate_random_image_url()
    else:
        return generate_positive_sentence()

def get_random_reply():
    """外部调用直接获取一条随机生成的回复"""
    return generate_or_load_reply()

# 示例调用
# print(generate_or_load_reply())
