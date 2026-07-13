FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# اکسپوز کردن پورت 5000
EXPOSE 5000

# اجرای اپلیکیشن
CMD ["python", "app.py"]
