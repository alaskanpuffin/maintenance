# Django Maintenance/Inventory Software

Required environment variables:

`DJANGO_ENVIRONMENT` can either be set to "production" or "development". It is recommended to be set to "production".
`SECRET_KEY` can be anything, used by Django to verify sessions.
`DB_ENGINE` either "sqlite" or "mssql" (Microsoft SQL Server).

If `DB_ENGINE` is "mssql", the following environment variables are required.
`DB_NAME` the name of the database.
`DB_USERNAME` username of a database user with read/write permissions.
`DB_PASSWORD` password for the above user.
`DB_HOST` IP of the MSSQL server.

Can also be run using Docker, build an image with the included Dockerfile.
