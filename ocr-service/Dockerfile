FROM python:3.11-bookworm

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies required by PaddleOCR/OpenCV/PDF support
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgomp1 \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]