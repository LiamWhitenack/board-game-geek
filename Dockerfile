# Use the official Postgres image from Docker Hub
FROM postgres:17-alpine

# Set environment variables for the default database and user
ENV POSTGRES_DB=bgg-db
ENV POSTGRES_USER=lwhitenack
ENV POSTGRES_PASSWORD=testpword

# Optionally copy an initialization script (e.g., create tables)
# COPY init.sql /docker-entrypoint-initdb.d/
