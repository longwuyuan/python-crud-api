## API(s) Microservice
Python flask powered APIs for create, update, delete (CRUD) operations on a PostgreSQL-D
- Flask provides the "views"/"routes" to make the app be web enabled.
- flask_uuid module  https://github.com/wbolster/flask-uuid  brings a special unique advantage. We get the ability of handling UUID as UUID data-type, at the endpoints.
- Psycopg2 __RealDictCursor__, http://initd.org/psycopg/docs/extras.html, is a feature of the psycopg module, that makes python work with PostgreSQL. There are superior modules for using postgres, like SQLAlchemy. But psycopg2 is order of magnitude simpler, faster and requires much much less code. When compared to really great tools like SQlAlchemy, there was no need for a schema hence, did not use SQLAlchemy.
- Psycopg2 RealDictCursor returns the postgresdb column_names, as a python dictionary, and column_names were created exactly as per key names, in the json response expected. So it saved the work to manually handle a bunch of data.
- Pipenv https://docs.pipenv.org/ proved to be a pain (at the time of writing) with alpine/musl so while pipenv was used in dev environ, the build actually uses "requirements.txt" for ease.
- Supervisord  http://supervisord.org/  is a process-manager, that particularly shines in the use case of docker containers because the default behaviour of docker containers, is to start just one process with the CMD/ENTRYPOINT directive
s. So, supervisord has been used for starting both the WSGI server "gunicorn" https://gunicorn.org/#quickstart  as well as the reverseproxy nginx. This brings the really helpful capability of Using "kubectl logs" for useful logging (HTTP headers in full detail) from nginx, which is not super nice with gunicorn.
