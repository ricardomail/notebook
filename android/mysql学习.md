**mysql创建数据库**

CREATE DATABASE 数据库名;

**使用mysqladmin**

mysqladmin -u root -p create 数据库名

**删除数据库**

drop database <数据库名>

mysqladmin -u root -p drop <数据库名>

**链接数据库**

use <数据库名>

**数据类型**

http://www.runoob.com/mysql/mysql-data-types.html

**创建数据库**

CREATE TABLE IF NOT EXISTS pro_order ( 
order_id INT UNSIGNED AUTO_INCREMENT, 
order_name VARCHAR(100) NOT NULL, 
order_time DATE, 
PRIMARY KEY(order_id) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

可以不用每个字端写`号，不要写'号，如果不想为null就写not null, auto_increment定义为自增属性，一般用于主键，数字会自动加1.

PRIMARY KEY关键字用于定义列为主键，可以使用多列来定义主键，列间以逗号分隔。

ENGINE 设置存储引擎，CHARSET设置编码。

**删除数据库**

drop table <表名>

**插入数据**

INSERT INTO TABLE_NAME (field1, field2,…….)

​					VALUES

​						(value1, value2,......)

插入字符串要用双引号包裹“”

**数据库查询**

SELECT COLUMN_NAME FROM TABLE_NAME 

[WHERE CLAUSE]

[LIMIT N]

[OFFSET M]

- 查询语句中你可以使用一个或者多个表，表之间使用逗号(,)分割，并使用WHERE语句来设定查询条件。
- SELECT 命令可以读取一条或者多条记录。
- 你可以使用星号（*）来代替其他字段，SELECT语句会返回表的所有字段数据
- 你可以使用 WHERE 语句来包含任何条件。
- 你可以使用 LIMIT 属性来设定返回的记录数。
- 你可以通过OFFSET指定SELECT语句开始查询的数据偏移量。默认情况下偏移量为0。

**WHERE 子句**

```
SELECT field1, field2,...fieldN FROM table_name1, table_name2...
[WHERE condition1 [AND [OR]] condition2.....
```

- 查询语句中你可以使用一个或者多个表，表之间使用逗号, 分割，并使用WHERE语句来设定查询条件。
- 你可以在 WHERE 子句中指定任何条件。
- 你可以使用 AND 或者 OR 指定一个或多个条件。
- WHERE 子句也可以运用于 SQL 的 DELETE 或者 UPDATE 命令。
- WHERE 子句类似于程序语言中的 if 条件，根据 MySQL 表中的字段值来读取指定的数据。

**BINARY关键字**

MySQL 的 WHERE 子句的字符串比较是不区分大小写的。 你可以使用 BINARY 关键字来设定 WHERE 子句的字符串比较是区分大小写的。

