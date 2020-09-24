FROM ubuntu:latest
RUN mkdir /app
RUN mkdir /app/code
RUN apt-get update -y
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip python3-dev build-essential
COPY app /app/code/
WORKDIR /app
RUN pip3 install -r code/requirements.txt
CMD ["python3.8","code/final.py"]
EXPOSE 8123/tcp