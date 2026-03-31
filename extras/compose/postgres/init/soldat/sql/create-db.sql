CREATE USER soldat PASSWORD 'p';

CREATE DATABASE soldat;

GRANT ALL ON DATABASE soldat TO soldat;

CREATE TABLESPACE soldatspace OWNER soldat LOCATION '/tablespace/soldat';
