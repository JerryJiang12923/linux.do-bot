import random

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

def generate_or_load_reply():
    """随机选择生成或读取一条回复"""
    predefined_replies = load_predefined_replies()
    if random.choice([True, False]) and predefined_replies:
        return random.choice(predefined_replies) + "\n" + generate_random_image_url()
    else:
        return generate_positive_sentence()

def get_random_reply():
    """外部调用直接获取一条随机生成的回复"""
    return generate_or_load_reply()