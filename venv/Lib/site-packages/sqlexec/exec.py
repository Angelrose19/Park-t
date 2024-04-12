from .dialect import Dialect
from .loader import Loader
from . import sql_support
from executor import DBError
from typing import Collection, Iterable
from .log_support import logger, insert_log, save_log
from executor import execute as _execute, select as _select, select_one as _select_one, do_select as _do_select,\
    save as _save, batch_execute as _batch_execute, get as _get, query as _query, query_one as _query_one


def execute(sql: str, *args, **kwargs):
    """
    Execute sql return effect rowcount

    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('sqlexec.execute', sql, *args, **kwargs)
    return do_execute(sql, *args)


def insert(table_name: str, **kwargs):
    """
    Insert data into table, return effect rowcount.

    :param table_name: table name
    :param kwargs: {name='张三', age=20}
    return: Effect rowcount
    """
    insert_log('insert', table_name, **kwargs)
    sql, args = sql_support.insert_sql_args(table_name.strip(), **kwargs)
    return do_execute(sql, *args)


def save(table_name: str, **kwargs):
    """
    Insert data into table, return primary key.
    """
    try:
        select_key = Dialect.get_select_key(table_name=table_name)
    except NotImplementedError:
        raise DBError(f"Expect 'select_key' but not. you may should use 'save_select_key' func with 'select_key'.")
    return save_select_key(select_key, table_name, **kwargs)


def save_sql(sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.
    """
    try:
        select_key = Dialect.get_select_key(sql=sql)
    except NotImplementedError:
        raise DBError(f"Expect 'select_key' but not. you may should use 'save_sql_select_key' func with 'select_key'.")
    return save_sql_select_key(select_key, sql, *args, **kwargs)


def save_select_key(select_key: str, table_name: str, **kwargs):
    """
    Insert data into table, return primary key.

    :param select_key: sql for select primary key
    :param table_name: table name
    :param kwargs: {name='张三', age=20}
    :return: Primary key
    """
    save_log('save_select_key', select_key, table_name, **kwargs)
    sql, args = sql_support.insert_sql_args(table_name.strip(), **kwargs)
    return save_sql_select_key(select_key, sql, *args)


def save_sql_select_key(select_key: str, sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.

    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}

    :param select_key: sql for select primary key
    :param sql: SQL
    :return: Primary key
    """
    logger.debug("Exec func 'sqlexec.%s', 'select_key': %s \n\t sql: %s \n\t args: %s \n\t kwargs: %s" % ('save_sql', select_key, sql, args, kwargs))
    sql, args = sql_support.get_mapping_sql_args(sql, *args, **kwargs)
    return do_save_sql_select_key(select_key, sql, *args)


def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result, SQL contain 'limit'.

    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('sqlexec.get', sql, *args, **kwargs)
    return do_get(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    execute select SQL and return unique result or list results(tuple).

    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('sqlexec.select', sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and return unique result(tuple), SQL contain 'limit'.

    sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1 --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('sqlexec.select_one', sql, *args, **kwargs)
    return do_select_one(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('sqlexec.query', sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    execute select SQL and return unique result(dict), SQL contain 'limit'.

    sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1 --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('sqlexec.query_one', sql, *args, **kwargs)
    return do_query_one(sql, *args)


def do_execute(sql: str, *args):
    """
    Execute sql return effect rowcount

    sql: insert into person(name, age) values(?, ?)  -->  args: ('张三', 20)
    """
    sql = Dialect.before_execute(sql)
    return _execute(sql, *args)


def do_save_sql(sql: str, *args):
    """
    Insert data into table, return primary key.

    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    try:
        select_key = Dialect.get_select_key(sql=sql)
    except NotImplementedError:
        raise DBError(f"Expect 'select_key' but not. you may should use 'save_sql_select_key' func with 'select_key'.")
    return do_save_sql_select_key(select_key, sql, *args)


def do_save_sql_select_key(select_key: str, sql: str, *args):
    """
    Insert data into table, return primary key.

    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    sql = Dialect.before_execute(sql)
    return _save(select_key, sql, *args)


def do_get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
    MultiColumnsError: Expect only one column.

    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    sql = Dialect.before_execute(sql)
    return _get(sql, *args)


def do_select(sql: str, *args):
    """
    execute select SQL and return unique result or list results(tuple).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql = Dialect.before_execute(sql)
    return _select(sql, *args)


def do_select_one(sql: str, *args):
    """
    Execute select SQL and return unique result(tuple), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    sql = Dialect.before_execute(sql)
    return _select_one(sql, *args)


def do_query(sql: str, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql = Dialect.before_execute(sql)
    return _query(sql, *args)


def do_query_one(sql: str, *args):
    """
    execute select SQL and return unique result(dict), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    sql, args = sql_support.limit_one_sql_args(sql, *args)
    sql = Dialect.before_execute(sql)
    return _query_one(sql, *args)


def select_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('select_page', sql, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


def query_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_mapping('query_page', sql, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def do_select_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql, args = Dialect.get_page_sql_args(sql, page_num, page_size, *args)
    return do_select(sql, *args)


def do_query_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql, args = Dialect.get_page_sql_args(sql, page_num, page_size, *args)
    return do_query(sql, *args)


def batch_execute(sql: str, *args):
    """
    Batch execute
    :param sql: insert into person(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
    :param args: All number must have same size.
    :return: Effect row count
    """
    assert args, "*args must not be empty."
    if isinstance(args[0], dict):
        sql, args = sql_support.batch_named_sql_args(sql, *args)
    sql = Dialect.before_execute(sql)
    args = sql_support.get_batch_args(*args)
    return _batch_execute(sql, *args)


def batch_insert(table_name: str, *args):
    """
    Batch insert
    :param table_name: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    logger.debug("Exec func 'sqlexec.%s' \n\t Table: '%s', args: %s" % ('batch_insert', table_name, args))
    sql, args = sql_support.batch_insert_sql_args(table_name, *args)
    return batch_execute(sql, *args)


def load(sql: str, *args, **kwargs) -> Loader:
    """
    Execute select SQL and save a csv

    sqlexec.load('select id, name, age from person WHERE name=:name', name='张三')

    :param sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
                SELECT * FROM person WHERE name=:name and age=:age limit 1 --> kwargs: {'name': '张三', 'age': 20}
    :return: Loader
    """
    sql, args = sql_support.try_mapping('sqlexec.csv', sql, *args, **kwargs)
    return do_load(sql, *args)


def do_load(sql: str, *args) -> Loader:
    """
    Execute select SQL and save a csv

    sqlexec.do_load('select id, name, age from person WHERE name = ?', '张三')

    :param sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
    :return: Loader
    """
    sql = Dialect.before_execute(sql)
    return Loader(*_do_select(sql, *args))


def insert_from_csv(file_name: str, table_name: str, delimiter=',', header=True, columns: Collection[str] = None, encoding='utf-8') -> int:
    """
    sqlexec.insert_from_csv('test.csv', 'person')
    """
    import csv
    sql = None
    if columns and len(columns) > 0:
        sql = sql_support.insert_sql(table_name.strip(), columns)
    elif not header:
        raise ValueError("Expected one of 'header' and 'columns'.")

    with open(file_name, newline='', encoding=encoding) as f:
        lines = csv.reader(f, delimiter=delimiter)
        lines = [line for line in lines]

    if len(lines) == 0:
        return 0

    if header:
        if len(lines) == 1:
            return 0

        if sql is None:
            sql = sql_support.insert_sql(table_name.strip(), lines[0])
        lines = lines[1:]

    return batch_execute(sql, lines)


def insert_from_df(df, table_name: str, columns: Collection[str] = None) -> int:
    """
    sqlexec.insert_from_df(df, 'person')
    """
    columns = columns if columns and len(columns) > 0 else df.columns.tolist()
    sql = sql_support.insert_sql(table_name.strip(), columns)
    return batch_execute(sql, df.values.tolist())


def insert_from_json(file_name: str, table_name: str, encoding='utf-8') -> int:
    """
    sqlexec.insert_from_json('test.json', 'person')

    many rows json file example:
    [{"id": 1, "name": "张三", "age": 55}, ...]

    one row json file example:
    {"id": 1, "name": "张三", "age": 55}
    """
    import json

    with open(file_name, encoding=encoding) as f:
        data = json.load(f)

    if isinstance(data, dict):
        return insert(table_name, **data)
    elif isinstance(data, Iterable):
        return batch_insert(table_name, data)
    else:
        logger.info("Exec func 'sqlexec.%s' \n\t Table: '%s' insert 0 rows." % ('insert_from_json', table_name))
        return 0


def truncate(table_name: str) -> int:
    """ sqlexec.truncate('person') """
    return _execute(Dialect.get_truncate_sql(table_name))


def drop(table_name: str) -> int:
    """ sqlexec.drop('person') """
    return _execute('DROP TABLE %s' % table_name)


