docker run -d -p 27017:27017 --name jhmongo \
        -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
        -e MONGO_INITDB_ROOT_PASSWORD=m0nG0Adm1n \
        mongo
