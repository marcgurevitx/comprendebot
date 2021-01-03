FROM postgres

COPY extlibs/depesz-Versioning/install.versioning.sql /docker-entrypoint-initdb.d

