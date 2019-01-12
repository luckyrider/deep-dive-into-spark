# SQL Support

## Overview


## Design and Implementation

### CTE (Common Table Expression)
```
WITH person2 AS (SELECT * FROM person WHERE id < 2)
SELECT p.id, p.name, gp.school FROM person2 p JOIN graduate_program gp ON p.graduate_program = gp.id;
```
