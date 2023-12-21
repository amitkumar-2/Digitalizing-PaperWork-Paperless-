I am facing the main problem is that first create the database seperatly with #docker compose up -d postgres command and then run the flask-app container with seperate command #docker compose up --build flask-app
Make sure in Dockerfile have same port as docker-compose.yaml file flask-app service and same as the flask-app is runnning on the same port.
Token Problem Solution ==>>  PyJWT and pyjwt is two different library. Use pyjwt which have encode method. At container making time i used pyjwt (not jwt and not PyJWT). pyjwt(PyJWT==2.8.0)
