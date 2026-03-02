-- initialize postgres cluster role and database for local development
CREATE ROLE app WITH LOGIN CREATEDB PASSWORD 'password';
CREATE DATABASE app OWNER app;
