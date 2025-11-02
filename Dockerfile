# Use a more specific Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements first (better for caching)
COPY requirements.txt .

# Install PyArrow with binary wheels first, then the rest
RUN pip install --no-cache-dir --only-binary=pyarrow pyarrow
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install in editable mode
RUN pip install --no-cache-dir -e .


# Expose the port that Flask will run on
EXPOSE 8080

# Command to run the app
CMD ["python", "application.py"]