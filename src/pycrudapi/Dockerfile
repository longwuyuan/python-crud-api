FROM nginx:alpine

# Install basic needs for building psycopg2 (and isolate layer for cache)
RUN apk -u --no-cache add gcc musl-dev linux-headers python3-dev postgresql-dev py3-pip supervisor

# Install needed python modules (and isolate layer for cache)
RUN pip3 install flask flask_uuid psycopg2-binary gunicorn 

WORKDIR /code/python-crud-api/src/pycrudapi

# Configure the container
ADD https://github.com/longwuyuan/python-crud-api/tree/master/src/pycrudapi/conf /conf
RUN rm /etc/nginx/conf.d/default.conf && \
    mv /conf/default.conf /etc/nginx/conf.d/default.conf && \
    rm /etc/supervisord.conf && \
    mv /conf/supervisord.conf /etc/supervisord.conf && \
    mkdir /etc/supervisor.d /var/log/supervisord

ADD https://github.com/longwuyuan/python-crud-api/tree/master/src/pycrudapi/app /app
WORKDIR /app

EXPOSE 80

CMD /usr/bin/supervisord
