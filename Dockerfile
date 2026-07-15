FROM python:3.13-slim

# Không tạo file .pyc, in log ra ngay không buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Cài các gói hệ thống cần thiết để build một số thư viện Python (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để tận dụng Docker layer cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

EXPOSE 5000

# Chạy bằng uvicorn (phù hợp cho FastAPI)
# Nếu app của bạn tên file là main.py và biến app là "app" -> main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]