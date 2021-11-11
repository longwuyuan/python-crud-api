FROM nginx:alpine

# Install basic needs for building psycopg2 (and isolate layer for cache)
RUN apk -u --no-cache add gcc musl-dev linux-headers python3-dev postgresql-dev py3-pip supervisor

# Install needed python modules (and isolate layer for cache)
RUN pip3 install flask flask_uuid psycopg2-binary gunicorn 

RUN apk add -u git && \
    mkdir /code && \
    cd /code && \
    git clone https://github.com/longwuyuan/python-crud-api.git && \
# Configure the container
    rm /etc/nginx/conf.d/default.conf && \
    cp /code/python-crud-api/src/pycrudapi/conf/default.conf /etc/nginx/conf.d/default.conf && \
    rm /etc/supervisord.conf && \
    cp /code/python-crud-api/src/pycrudapi/conf/supervisord.conf /etc/supervisord.conf && \
    mkdir /etc/supervisor.d /var/log/supervisord && \
    cp -r /code/python-crud-api/src/pycrudapi/app /app

WORKDIR /app

EXPOSE 80

CMD /usr/bin/supervisord
