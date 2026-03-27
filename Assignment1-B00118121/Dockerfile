# Use the official Python 3.11 slim image as the base
# slim means it is a smaller, lighter version of Python with only the essentials
# this keeps the container size down compared to the full Python image
FROM python:3.11-slim

# Set the working directory inside the container to /app
# all commands after this will run from this folder
WORKDIR /app

# Copy only the requirements.txt file first before copying the rest of the code
# this is done first so Docker can cache this layer
# if requirements.txt hasn't changed, Docker skips re-installing packages on the next build
COPY requirements.txt .

# Install all the Python libraries listed in requirements.txt
# --no-cache-dir prevents pip from saving downloaded packages locally
# which keeps the container image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining project files from the local machine into the /app folder in the container
# this includes main.py, models.py, database.py and any other project files
COPY . .

# Tell Docker that the container will listen on port 8000
# this does not actually open the port, it is just documentation
# the port is opened when you run the container with -p 8000:8000
EXPOSE 8000

# The command that runs when the container starts
# this starts the FastAPI application using uvicorn as the web server
# --host 0.0.0.0 makes the server accessible from outside the container
# --port 8000 tells uvicorn to listen on port 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]