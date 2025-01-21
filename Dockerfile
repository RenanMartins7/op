#Python imagem from docker hub
FROM python:3.9-slim

#Set the working directory inside the container
WORKDIR /app

#Copy the needed files to the container
COPY . .

#Installing the iperf server dependencies
RUN apt-get update && apt-get install -y \
    iperf3 \
    && apt-get clean

#instaling the requiriments to the applications
RUN pip install -r requirements.txt


#Expose the port that runs the app
EXPOSE 8000

#Runing the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]