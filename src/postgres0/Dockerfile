FROM postgres:alpine

RUN apk add -u git && \
        mkdir /code && \
        cd /code && \
        git clone https://github.com/longwuyuan/python-crud-api.git && \
        cp /code/python-crud-api/src/postgres0/conf/* /docker-entrypoint-initdb.d/.
