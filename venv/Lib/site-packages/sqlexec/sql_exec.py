# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from . import exec
from .loader import Loader
from .page_exec import PageExec


class SqlPageExec:

    def __init__(self, sql: str, page_exec: PageExec):
        self.sql = sql
        self.page_exec = page_exec

    def query(self, *args, **kwargs):
        """
        Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.page_exec.query(self.sql, *args, **kwargs)

    def select(self, *args, **kwargs):
        """
        Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.page_exec.select(self.sql, *args, **kwargs)

    def do_query(self, *args):
        """
        Execute select SQL and return list results(dict).
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.page_exec.do_query(self.sql, *args)

    def do_select(self, *args):
        """
        Execute select SQL and return list results(dict).
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.page_exec.do_select(self.sql, *args)


class ParamPageExec:

    def __init__(self, sql_page_exec: SqlPageExec, *args, **kwargs):
        self.sql_page_exec = sql_page_exec
        self.args = args
        self.kwargs = kwargs

    def query(self):
        return self.sql_page_exec.query(*self.args, **self.kwargs)

    def select(self):
        return self.sql_page_exec.select(*self.args, **self.kwargs)


class Param:

    def __init__(self, sql_exec, *args, **kwargs):
        self.sql_exec = sql_exec
        self.args = args
        self.kwargs = kwargs

    def execute(self) -> int:
        """
        sqlexec.sql('INSERT INTO person(name, age) VALUES(?, ?)').param('张三', 18).execute()
        """
        return self.sql_exec.execute(*self.args, **self.kwargs)

    def save(self):
        """
        sqlexec.sql('INSERT INTO person(name, age) VALUES(?, ?)').param('张三', 18).save('SELECT LAST_INSERT_ID()')
        """
        return self.sql_exec.save(*self.args, **self.kwargs)

    def save_select_key(self, select_key: str):
        """
        sqlexec.sql('INSERT INTO person(name, age) VALUES(?, ?)').param('张三', 18).save('SELECT LAST_INSERT_ID()')
        """
        return self.sql_exec.save_select_key(select_key, *self.args, **self.kwargs)

    def get(self):
        """
        sqlexec.sql('SELECT count(1) FROM person WHERE name=? and age=? limit 1').param('张三', 18).get()
        """
        return self.sql_exec.get(*self.args, **self.kwargs)

    def select(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).select()
        """
        return self.sql_exec.select(*self.args, **self.kwargs)

    def select_one(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=? limit 1').param('张三', 18).select_one()
        """
        return self.sql_exec.select_one(*self.args, **self.kwargs)

    def query(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).query()
        """
        return self.sql_exec.query(*self.args, **self.kwargs)

    def query_one(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=? limit 1').param('张三', 18).query_one()
        """
        return self.sql_exec.query_one(*self.args, **self.kwargs)

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).to_csv('test.csv')
        """
        self.sql_exec.load(*self.args, **self.kwargs).to_csv(file_name, delimiter, header, encoding)

    def to_df(self):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).to_df()
        """
        return self.sql_exec.load(*self.args, **self.kwargs).to_df()

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        sqlexec.sql('SELECT * FROM person WHERE name=? and age=?').param('张三', 18).to_json('test.json')
        """
        self.sql_exec.load(*self.args, **self.kwargs).to_json(file_name, encoding)

    def page(self, page_num=1, page_size=10) -> ParamPageExec:
        return ParamPageExec(self.sql_exec.page(page_num, page_size), *self.args, **self.kwargs)


class SqlExec:

    def __init__(self, _exec, sql: str):
        self.exec = _exec
        self.sql = sql

    def execute(self, *args, **kwargs) -> int:
        """
        Execute sql return effect rowcount

        sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
             INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.execute(self.sql, *args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.exec.save_sql(self.sql, *args, **kwargs)

    def save_select_key(self, select_key: str, *args, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.exec.save_sql_select_key(select_key, self.sql, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
             SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.get(self.sql, *args, **kwargs)

    def select(self, *args, **kwargs):
        """
        execute select SQL and return unique result or list results(tuple).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.select(self.sql, *args, **kwargs)

    def select_one(self, *args, **kwargs):
        """
        Execute select SQL and return unique result(tuple), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.select_one(self.sql, *args, **kwargs)

    def query(self, *args, **kwargs):
        """
        Execute select SQL and return list results(dict).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.query(self.sql, *args, **kwargs)

    def query_one(self, *args, **kwargs):
        """
        execute select SQL and return unique result(dict), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.query_one(self.sql, *args, **kwargs)

    def do_execute(self, *args):
        """
        Execute sql return effect rowcount

        sql: insert into person(name, age) values(?, ?)  -->  args: ('张三', 20)
        """
        return self.exec.do_execute(None, self.sql, *args)

    def do_save_sql(self, select_key: str, *args):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.exec.do_save_sql(select_key, self.sql, *args)

    def do_get(self, *args):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.exec.do_get(self.sql, *args)

    def do_select(self, *args):
        """
        execute select SQL and return unique result or list results(tuple).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.exec.do_select(self.sql, *args)

    def do_select_one(self, *args):
        """
        Execute select SQL and return unique result(tuple), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.exec.do_select_one(self.sql, *args)

    def do_query(self, *args):
        """
        Execute select SQL and return list results(dict).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.exec.do_query(self.sql, *args)

    def do_query_one(self, *args):
        """
        execute select SQL and return unique result(dict), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.exec.do_query_one(self.sql, *args)

    def batch_execute(self, *args):
        """
        Batch execute sql return effect rowcount

        sql: insert into person(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]

        :param args: All number must have same size.
        :return: Effect rowcount
        """
        return self.exec.batch_execute(self.sql, *args)

    def load(self, *args, **kwargs) -> Loader:
        """
        sqlexec.sql('select id, name, age from person WHERE name = :name').load(name='张三')
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name = :name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.load(self.sql, *args, **kwargs)

    def do_load(self, *args) -> Loader:
        """
        sqlexec.sql('select id, name, age from person WHERE name = ?').do_load('张三')
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.exec.do_load(self.sql, *args)

    def param(self, *args, **kwargs) -> Param:
        """
        sqlexec.sql('select id, name, age from person WHERE name = :name').param(name='张三')
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name = :name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return Param(self, *args, **kwargs)

    def page(self, page_num=1, page_size=10) -> SqlPageExec:
        return SqlPageExec(self.sql, PageExec(self.exec, page_num=page_num, page_size=page_size))


def sql(sql_text: str) -> SqlExec:
    sql_text = sql_text.strip()
    assert sql_text, "Parameter 'sql' must not be none"
    return SqlExec(exec, sql_text)
