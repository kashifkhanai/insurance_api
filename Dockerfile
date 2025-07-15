# Python 3.13.2 Dockerfile
FROM python:3.13.2

# Set the working directory
WORKDIR /insurance

# Copy the requirements file into the container
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirments.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "insurance:app", "--host", "0.0.0.0", "--port", "8000"]