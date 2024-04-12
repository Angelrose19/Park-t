import re
from executor import DBError
from .dialect import Dialect
from functools import lru_cache
from .log_support import sql_log
from executor.sql_support import require_limit
from typing import Collection, Union, List, Tuple
from .constant import CACHE_SIZE, NAMED_REGEX, LIMIT_1


def limit_one_sql_args(sql: str, *args):
    if require_limit(sql):
        return '{} LIMIT ?'.format(sql), [*args, LIMIT_1]
    return sql, args


def insert_sql(table: str, cols: Collection[str]):
    cols = cols if isinstance(cols, tuple) else tuple(cols)
    return Dialect.create_insert_sql(table, cols)


def insert_sql_args(table: str, **kwargs):
    cols, args = zip(*kwargs.items())
    sql = Dialect.create_insert_sql(table, cols)
    return sql, args


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Collection) else args


def batch_insert_sql_args(table: str, *args):
    args = get_batch_args(*args)
    args = [zip(*arg.items()) for arg in args]  # [(cols, args)]
    cols, args = zip(*args)  # (cols), (args)
    sql = Dialect.create_insert_sql(table, cols[0])
    return sql, args


def batch_named_sql_args(sql: str, *args):
    args = get_batch_args(*args)
    args = [get_named_args(sql, **arg) for arg in args]
    sql = get_named_sql(sql)
    return sql, args


@lru_cache(maxsize=CACHE_SIZE)
def get_named_sql(sql: str):
    return re.sub(NAMED_REGEX, '?', sql)


def get_named_args(sql: str, **kwargs):
    return [kwargs[r[1:]] for r in re.findall(NAMED_REGEX, sql)]


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args


def is_mapping(sql: str):
    return ':' in sql


def is_placeholder(sql: str):
    return '?' in sql


def get_mapping_sql_args(sql: str, *args, **kwargs):
    if is_mapping(sql):
        assert kwargs, "Named mapping SQL expect '**kwargs' should not be empty."
        return get_named_sql_args(sql, **kwargs)

    if is_placeholder(sql) and not args:
        raise DBError("Placeholder sql expect '*args' should not be empty.")

    return sql, args


def try_mapping(function, sql, *args, **kwargs):
    sql_log(function, sql, *args, **kwargs)
    return get_mapping_sql_args(sql, *args, **kwargs)


def get_table_select_sql(table_name: str, where: str, limit: Union[int, Tuple[int], List[int]], *columns):
    columns = ','.join([col if '(' in col else '{}'.format(col) for col in columns]) if columns else Dialect.get_table_columns(table_name)

    if limit:
        if isinstance(limit, int):
            return 'SELECT {} FROM {} {} LIMIT ?'.format(columns, table_name, where)
        elif (isinstance(limit, Tuple) or isinstance(limit, List)) and len(limit) == 2:
            return 'SELECT {} FROM {} {} LIMIT ? OFFSET ?'.format(columns, table_name, where)
        else:
            raise ValueError("The type of the parameter 'limit' must be 'int' or tuple, list, and it length is 2.")
    else:
        return 'SELECT {} FROM {} {}'.format(columns, table_name, where)
