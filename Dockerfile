# Use Python 3.11 as base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy only requirements first (to cache pip install layer)
COPY requirements.txt .

# Install Python dependencies (cached unless requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your app (won't bust pip cache)
COPY . .

# Run your Telegram bot
CMD ["python3", "telegram_bot.py"]
