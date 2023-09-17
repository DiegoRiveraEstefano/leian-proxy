FROM python:3.11-slim-buster

COPY /src /leian_proxy/src
WORKDIR /leian_proxy

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY nginx.conf /etc/nginx
COPY start.sh .

RUN chmod +x ./start.sh
EXPOSE 80
EXPOSE 8000

RUN touch access.log

CMD ["./start.sh"]