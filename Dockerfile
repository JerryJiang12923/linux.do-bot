# 使用官方的 Python 3.7 镜像作为基础镜像
FROM python:3.7-slim

# 设置工作目录为 /app
WORKDIR /app

# 复制项目文件到容器的 /app 目录
COPY . .

# 更换 pip 镜像源为国内镜像源，并安装 requests、tabulate 和 configparser
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir requests tabulate configparser

# 安装系统库
#RUN apt-get update && apt-get install -y --fix-missing \
#    libgtk-3-0 \
#    libasound2 \
#    libx11-6 \
#    libxcomposite1 \
#    libxdamage1 \
#    libxext6 \
#    libxfixes3 \
#    libxrandr2 \
#    libxrender1 \
#    libxtst6 \
#    libfreetype6 \
#    libfontconfig1 \
#    libpangocairo-1.0-0 \
#    libpango-1.0-0 \
#    libatk1.0-0 \
#    libcairo2 \
#    libgdk-pixbuf2.0-0 \
#    libglib2.0-0 \
#    libdbus-1-3 \
#    libxcb1 \
#    libxi6 && \
#    rm -rf /var/lib/apt/lists/*

# 安装 playwright 并安装浏览器
RUN pip install --no-cache-dir playwright && \
    playwright install

# 设置时区为中国时区
ENV TZ=Asia/Shanghai

# 指定容器启动时执行的命令
CMD ["python", "main.py"]
