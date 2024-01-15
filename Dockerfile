FROM python:3.11-slim-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN ln -sf /dev/stdout nickbot.log
COPY . .

CMD [ "python", "./nickbot.py" ]