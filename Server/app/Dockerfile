FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pip
RUN apt-get update -y && apt-get install -y python3-pip

# Install the required packages
RUN apt-get install libgl1-mesa-glx -y

RUN pip install -r requirements.txt

# Expose port 5001
EXPOSE 5001

# Run the command to start the Flask app
CMD ["python", "app.py"]

