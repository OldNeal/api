# ============================================
# Dockerfile для FastAPI сервера
# ============================================
FROM python:3.13-slim AS api_builder

# Настройки окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Создаём non-root пользователя
RUN useradd --create-home --shell /bin/bash apiuser && \
    chown -R apiuser:apiuser /app
USER apiuser

# Запуск API с авто-перезагрузкой (для разработки)
CMD ["uvicorn", "main:run", "--host", "0.0.0.0", "--port", "8000", "--reload"]