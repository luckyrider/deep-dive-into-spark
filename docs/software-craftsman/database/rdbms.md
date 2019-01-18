# RDBMS

## MS SQL Server
https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-2017

```
docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=YourStrong!Passw0rd' -p 1400:1433 --name sqlserver1 -d microsoft/mssql-server-linux:2017-latest

docker exec -it sqlserver1 "bash"

# /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'YourStrong!Passw0rd'
1> select 1;
2> go
```

## Oracle XE
https://github.com/wnameless/docker-oracle-xe-11g

```
docker run -d -p 49161:1521 --name oraclexe1 wnameless/oracle-xe-11g

docker exec -it oraclexe1 "bash"
# sqlplus
Enter user-name: system
Enter password: oracle
SQL> select 1 from dual;
```
