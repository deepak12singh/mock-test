 
# ──────────────────────────────────────
# 1. Base image
# ──────────────────────────────────────
FROM python:3.11-slim

# ──────────────────────────────────────
# 2. Environment variables
# ──────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ──────────────────────────────────────
# 3. Working directory inside container
# ──────────────────────────────────────
WORKDIR /app

# ──────────────────────────────────────
# 4. Install system dependencies
# ─────────────────────────────────────

RUN apt-get update && apt-get install -y \
    netcat-openbsd gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ──────────────────────────────────────
# 5. Install Python dependencies
# ──────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ──────────────────────────────────────
# 6. Copy project files
# ──────────────────────────────────────
COPY . .

# ──────────────────────────────────────
# 7. Add entrypoint script (for migrations/staticfiles)
# ──────────────────────────────────────
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ──────────────────────────────────────
# 8. Expose the default Django/Gunicorn port
# ──────────────────────────────────────
EXPOSE 8000

# ──────────────────────────────────────
# 9. Start with entrypoint script
# ──────────────────────────────────────
ENTRYPOINT ["/entrypoint.sh"]

# 🟢 Replace `myproject` with your Django project name below
CMD ["gunicorn", "Mock_Test.wsgi:application", "--bind", "0.0.0.0:8000"]
