# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from .log_support import logger
from functools import lru_cache
from typing import Sequence, Collection
from executor.sql_support import require_limit
from executor import get, query, select, DBError, Engine
from .constant import CACHE_SIZE, LIMIT_1, DEFAULT_KEY_FIELD, MYSQL_COLUMN_SQL, MYSQL_SELECT_KEY, POSTGRES_COLUMN_SQL,\
    SQLITE_SELECT_KEY


def get_page_start(page_num: int, page_size: int):
    assert page_num >= 1 and page_size >= 1, "'page_name' and 'page_size' should be higher or equal to 1"
    return (page_num - 1) * page_size


class BaseDialect:

    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def create_insert_sql(table: str, cols: Collection[str]):
        columns, placeholders = zip(*[('{}'.format(col), '?') for col in cols])
        return 'INSERT INTO {}({}) VALUES({})'.format(table, ', '.join(columns), ','.join(placeholders))

    @staticmethod
    def before_execute(sql: str):
        if '%' in sql and 'like' in sql.lower():
            sql = sql.replace('%', '%%').replace('%%%%', '%%')
        return sql.replace('?', '%s')

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        start = get_page_start(page_num, page_size)
        if require_limit(sql):
            sql = '{} LIMIT ? OFFSET ?'.format(sql)
        args = [*args, page_size, start]
        return sql, args

    @staticmethod
    def get_table_columns(table_name: str):
        return '*'

    @staticmethod
    def get_truncate_sql(table_name: str):
        return 'TRUNCATE TABLE %s' % table_name

    @staticmethod
    def get_select_key(*args, **kwargs):
        raise NotImplementedError("Not implement method 'get_select_key', you can use orm snowflake for primary key.")


class MySQLDialect(BaseDialect):

    @staticmethod
    def create_insert_sql(table: str, cols: Sequence[str]):
        columns, placeholders = zip(*[('`{}`'.format(col), '?') for col in cols])
        return 'INSERT INTO `{}`({}) VALUES({})'.format(table, ','.join(columns), ','.join(placeholders))

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        start = get_page_start(page_num, page_size)
        if require_limit(sql):
            sql = '{} LIMIT ?, ?'.format(sql)
        args = [*args, start, page_size]
        return sql, args

    @staticmethod
    def get_table_columns(table_name: str):
        sql = MySQLDialect.before_execute(MYSQL_COLUMN_SQL)
        return get(sql, table_name, LIMIT_1)

    @staticmethod
    def get_select_key(*args, **kwargs):
        return MYSQL_SELECT_KEY

    @staticmethod
    def get_truncate_sql(table_name: str):
        return 'TRUNCATE TABLE `%s`' % table_name


class PostgresDialect(BaseDialect):

    @staticmethod
    def get_table_columns(table_name: str):
        sql = MySQLDialect.before_execute(POSTGRES_COLUMN_SQL)
        return get(sql, table_name, LIMIT_1)

    @staticmethod
    def get_select_key(key_seq: str = None, table_name: str = None, key: str =None, sql: str = None):
        if not key_seq:
            if table_name:
                key_seq = PostgresDialect.build_key_seq(table_name, key)
            else:
                if sql:
                    key_seq = PostgresDialect._get_key_seq_from_sql(sql)
                else:
                    raise DBError("Get PostgreSQL select key fail, all of 'key_seq', 'table', 'sql' are None")
        return f"SELECT currval('{key_seq}')"

    @staticmethod
    def build_key_seq(table_name: str, key: str = None):
        if not key:
            key = DEFAULT_KEY_FIELD
        return f'{table_name}_{key}_seq'

    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE)
    def _get_key_seq_from_sql(sql: str):
        table_name = re.search('(?<=into )\w+', sql, re.I)
        key_seq = PostgresDialect.build_key_seq(table_name.group())
        logger.warning("'key_seq' is None, will use default '{}' from sql.".format(key_seq))
        return key_seq


class OracleDialect(BaseDialect):

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        start = get_page_start(page_num, page_size)
        end = start + page_size
        sql = 'SELECT * FROM (SELECT tmp.*, rownum row_num FROM ({}) tmp WHERE rownum <= >) WHERE row_num > :startRow '.format(sql)
        args = [*args, end, start]
        return sql, args

    @staticmethod
    def get_table_columns(table_name: str):
        sql = Dialect.before_execute('SELECT column_name FROM user_tab_columns WHERE table_name = ?')
        results = select(sql, table_name)
        return ','.join([result[0] for result in results])


class SQLiteDialect(BaseDialect):

    @staticmethod
    def get_table_columns(table_name: str):
        results = query(f'PRAGMA table_info({table_name})')
        return ','.join([result['name'] for result in results])

    @staticmethod
    def get_select_key(*args, **kwargs):
        return SQLITE_SELECT_KEY

    @staticmethod
    def before_execute(sql: str):
        if '%' in sql and 'like' in sql.lower():
            sql = sql.replace('%', '%%').replace('%%%%', '%%')
        return sql

    @staticmethod
    def get_truncate_sql(table_name: str):
        return 'DELETE FROM `%s`' % table_name
    

_DIALECT = None


class Dialect:

    @classmethod
    def init(cls, engine: Engine):
        global _DIALECT
        if _DIALECT is None:
            if Engine.MYSQL == engine:
                _DIALECT = MySQLDialect(engine)
            elif Engine.POSTGRESQL == engine:
                _DIALECT = PostgresDialect(engine)
            elif Engine.ORACLE == engine:
                _DIALECT = OracleDialect(engine)
            elif Engine.SQLITE == engine:
                _DIALECT = SQLiteDialect(engine)
            else:
                _DIALECT = BaseDialect(engine)

    @staticmethod
    def create_insert_sql(table: str, cols: Collection[str]):
        global _DIALECT
        return _DIALECT.create_insert_sql(table, cols)

    @staticmethod
    def before_execute(sql: str):
        global _DIALECT
        return _DIALECT.before_execute(sql)

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        global _DIALECT
        return _DIALECT.get_page_sql_args(sql, page_num, page_size, *args)

    @staticmethod
    def get_table_columns(table_name: str):
        global _DIALECT
        return _DIALECT.get_table_columns(table_name)

    @staticmethod
    def get_truncate_sql(table_name: str):
        global _DIALECT
        return _DIALECT.get_truncate_sql(table_name)

    @staticmethod
    def get_select_key(*args, **kwargs):
        global _DIALECT
        return _DIALECT.get_select_key(*args, **kwargs)

    @staticmethod
    def curr_engine():
        global _DIALECT
        return _DIALECT.engine
