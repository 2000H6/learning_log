# 使用官方 Python 3.12 轻量级镜像
FROM python:3.12-slim

# 设置环境变量，确保 Python 输出直接打印到终端，不缓冲
ENV PYTHONUNBUFFERED=1

# 设置容器内的工作目录
WORKDIR /app

# 安装系统级依赖：gcc 用于编译，libpq-dev 是 psycopg2 必需的
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖清单并安装，利用 Docker 的缓存机制
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制项目代码
COPY . .

# 收集静态文件（Bootstrap 的 CSS/JS 样式就靠它了）
RUN python manage.py collectstatic --noinput

# 暴露 8000 端口
EXPOSE 8000

# 启动 Gunicorn 服务器
CMD ["sh", "-c", "python manage.py migrate && gunicorn learning_log.wsgi:application --bind 0.0.0.0:8000"]