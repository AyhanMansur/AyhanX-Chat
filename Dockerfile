# استفاده از پایتون نسخه سبک
FROM python:3.10-alpine

# تنظیم ورک‌دایرکتوری
WORKDIR /app

# کپی فایل‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# تعیین پورت (Railway به صورت خودکار پورت را ست می‌کند)
ENV PORT=8080
EXPOSE 8080

# دستور اجرای برنامه
CMD ["python", "app.py"]
