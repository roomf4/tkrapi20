--
-- cr_tkrapi.sql
--

-- This script should create role tkrapi and create database tkrapi.
-- Demo:
-- sudo su - postgres
-- psql -f cr_tkrapi.sql

create database tkrapi;
create role tkrapi with login superuser password 'tkrapi';
