FROM python:3.9-slim-buster

RUN apt-get update -y && apt-get install -y wget gnupg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get update -y && apt-get install -y curl unzip google-chrome-stable

RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

RUN unzip /tmp/chromedriver.zip chromedriver -d /

RUN chmod +x /chromedriver

WORKDIR /
COPY main.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV DISPLAY=:99
ENV TERM=xterm

ENTRYPOINT ["python", "main.py"]
