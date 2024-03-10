# Use the official Python image as the base image
FROM python:3.9

# Setting the arguments that need to be passed onto the Dockerfile
ARG WEATHER_API_URL
ARG TEMPERATURE_PARAMS
ARG RAIN_PARAMS

# Set environment variables (replace with your actual values)
ENV WEATHER_API_URL $WEATHER_API_URL
ENV TEMPERATURE_PARAMS $TEMPERATURE_PARAMS
ENV RAIN_PARAMS $RAIN_PARAMS

# Set working directory inside the container
WORKDIR /app

# Copy your Python code into the container
COPY . /app

# Install dependencies
RUN pip install --requirement requirements.txt
COPY . /tmp/

# Expose the port your FastAPI app will run on
EXPOSE 8000

# Command to run your FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
