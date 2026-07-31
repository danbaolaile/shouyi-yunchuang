FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

# 初始化数据库
RUN python database/init_db.py

EXPOSE 5000

CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:5000", "-w", "2"]
