# Use an official Python runtime as a parent image
FROM apache/airflow:2.6.3-python3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Update pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -v

# Install Airflow
RUN pip install apache-airflow

# Print Airflow version
RUN airflow version

# Expose port 8080 for the Airflow web server to be accessible
EXPOSE 8080

# Define environment variable
ENV AIRFLOW_HOME /app/airflow

# Initialize Airflow database
RUN airflow db init

# Start the web server, default port is 8080
CMD ["airflow", "webserver", "-p", "8080"]