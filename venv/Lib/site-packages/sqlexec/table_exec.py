#！/usr/bin/env python3
# -*- coding:utf-8 -*-

from .loader import Loader
from . import exec, sql_support
from .constant import LIMIT_1, SELECT_COUNT
from typing import Sequence, Tuple
from .sql_support import get_table_select_sql


class TablePageExec:

    def __init__(self, table_exec, page_num, page_size):
        self.table_exec = table_exec
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *columns):
        sql = get_table_select_sql(self.table_exec.table, '', 0, *columns)
        return self.table_exec.exec.do_select_page(sql, self.page_num, self.page_size)

    def query(self, *columns):
        sql = get_table_select_sql(self.table_exec.table, '', 0, *columns)
        return self.table_exec.exec.do_query_page(sql, self.page_num, self.page_size)


class ColumnPageExec:

    def __init__(self, table_page_exec: TablePageExec, *columns):
        self.table_page_exec = table_page_exec
        self.columns = columns

    def select(self):
        return self.table_page_exec.select(*self.columns)

    def query(self):
        return self.table_page_exec.query(*self.columns)

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        sqlexec.table('person').columns('name', 'age').where(name__eq='李四').json('test.json')
        """


class WherePageExec:

    def __init__(self, where_exec, page_num, page_size):
        self.where_exec = where_exec
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *columns):
        sql, args = self.where_exec.get_select_sql_args(*columns)
        return self.where_exec.exec.do_select_page(sql, self.page_num, self.page_size, *args)

    def query(self, *columns):
        sql, args = self.where_exec.get_select_sql_args(*columns)
        return self.where_exec.exec.do_query_page(sql, self.page_num, self.page_size, *args)
        self._where_exec.load(*self.columns).to_json(file_name, encoding)


class ColumnWherePageExec:

    def __init__(self, where_page_exec: WherePageExec, *columns):
        self.where_page_exec = where_page_exec
        self.columns = columns

    def select(self):
        return self.where_page_exec.select(*self.columns)

    def query(self):
        return self.where_page_exec.query(*self.columns)


class ColumnWhereExec:

    def __init__(self, where_exec, *columns):
        self._where_exec = where_exec
        self.columns = columns

    def get(self):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sqlexec.table('person').columns('name').where(id=1).get()
        """
        return self._where_exec.get(self.columns[0])

    def select(self):
        """
        sqlexec.table('person').columns('name', 'age').where(name='李四').select()
        """
        return self._where_exec.select(*self.columns)

    def select_one(self):
        """
        sqlexec.table('person').columns('name', 'age').where(name='李四').select_one()
        """
        return self._where_exec.select_one(*self.columns)

    def query(self):
        """
        sqlexec.table('person').columns('name', 'age').where(name='李四').query()
        """
        return self._where_exec.query(*self.columns)

    def query_one(self):
        """
        sqlexec.table('person').columns('name', 'age').where(name__eq='李四').query_one()
        """
        return self._where_exec.query_one(*self.columns)

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        sqlexec.table('person').columns('name', 'age').where(name__eq='李四').csv('test.csv')
        """
        self._where_exec.load(*self.columns).to_csv(file_name, delimiter, header, encoding)

    def to_df(self):
        """
        sqlexec.table('person').columns('name', 'age').where(name__eq='李四').df()
        """
        return self._where_exec.load(*self.columns).to_df()

    def page(self, page_num=1, page_size=10) -> ColumnWherePageExec:
        return ColumnWherePageExec(WherePageExec(self._where_exec, page_num, page_size), *self.columns)


class WhereExec:

    def __init__(self, _exec, table_name, **kwargs):
        self.exec = _exec
        self.table = table_name
        self.where_condition = kwargs

    def get(self, column: str):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sqlexec.table('person').where(name='李四').get('id')
        """
        sql, args = self.get_select_one_sql_args(column)
        return self.exec.do_get(sql, *args, LIMIT_1)

    def count(self):
        """
         sqlexec.table('person').where(name='李四').count()
        """
        return self.get(SELECT_COUNT)

    def exists(self):
        """
         sqlexec.table('person').where(name='李四').exists()
        """
        return self.get('1') == 1

    def select(self, *columns):
        """
        sqlexec.table('person').where(name='李四').select('name', 'age')
        """
        sql, args = self.get_select_sql_args(*columns)
        return self.exec.do_select(sql, *args)

    def select_one(self, *columns):
        """
        sqlexec.table('person').where(name='李四').select_one('name', 'age')
        """
        sql, args = self.get_select_one_sql_args(*columns)
        return self.exec.do_select_one(sql, *args, LIMIT_1)

    def query(self, *columns):
        """
        sqlexec.table('person').where(name='李四').query('name', 'age')
        """
        sql, args = self.get_select_sql_args(*columns)
        return self.exec.do_query(sql, *args)

    def query_one(self, *columns):
        """
        sqlexec.table('person').where(name__eq='李四').query_one('name', 'age')
        """
        sql, args = self.get_select_one_sql_args(*columns)
        return self.exec.do_query_one(sql, *args, LIMIT_1)

    def delete(self):
        """
        sqlexec.table('person').where(name='李四').delete()
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = 'DELETE FROM %s %s' % (self.table, where)
        return self.exec.do_execute(sql, *args)

    def update(self, **kwargs):
        """
        sqlexec.table('person').where(name='张三').update(name='李四', age=45)
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        update_cols, update_args = zip(*kwargs.items())
        args = [*update_args, *args]
        update_cols = ', '.join(['{} = ?'.format(col) for col in update_cols])
        sql = 'UPDATE {} SET {} {}'.format(self.table, update_cols, where)
        return self.exec.do_execute(sql, *args)

    def load(self, *columns) -> Loader:
        """
        sqlexec.table('person').where(name='张三').load('name', 'age')
        """
        sql, args = self.get_select_sql_args(*columns)
        return self.exec.do_load(sql, *args)

    def columns(self, *columns) -> ColumnWhereExec:
        return ColumnWhereExec(self, *columns)

    def page(self, page_num=1, page_size=10) -> WherePageExec:
        return WherePageExec(self, page_num, page_size)

    def get_select_sql_args(self, *columns):
        where, args, limit = get_where_arg_limit(**self.where_condition)
        sql = get_table_select_sql(self.table, where, limit, *columns)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return sql, args

    def get_select_one_sql_args(self, *columns):
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = get_table_select_sql(self.table, where, LIMIT_1, *columns)
        return sql, args

class ColumnExec:

    def __init__(self, table_exec, *columns):
        self.table_exec = table_exec
        self.columns = columns

    def insert(self, *args):
        """
        Execute sql return effect rowcount

        sqlexec.table('person').columns('name', 'age').insert(*args)

        :param args: ('张三', 20)
        """
        sql = sql_support.insert_sql(self.table_exec.table.strip(), self.columns)
        return self.table_exec.exec.execute(sql, *args)

    def batch_insert(self, *args):
        """
        Execute sql return effect rowcount

        sqlexec.table('person').columns('name', 'age').batch_insert(*args)

        :param args: [('张三', 20), ('李四', 28)]
        """
        sql = sql_support.insert_sql(self.table_exec.table.strip(), self.columns)
        return self.table_exec.exec.batch_execute(sql, *args)

    def get(self):
        """
        sqlexec.table('person').columns('count(1)').get()
        """
        return self.table_exec.get(*self.columns)

    def select(self):
        """
        sqlexec.table('person').columns('name', 'age').select()
        """
        return self.table_exec.select(*self.columns)

    def select_one(self):
        """
        sqlexec.table('person').columns('name', 'age').select_one()
        """
        return self.table_exec.select_one(*self.columns)

    def query(self):
        """
        sqlexec.table('person').columns('name', 'age').query()
        """
        return self.table_exec.query(*self.columns)

    def query_one(self):
        """
        sqlexec.table('person').columns('name', 'age').query_one()
        """
        return self.table_exec.query_one(*self.columns)

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        sqlexec.table('person').columns('name', 'age').to_csv('test.csv')
        """
        self.table_exec.load(*self.columns).to_csv(file_name, delimiter, header, encoding)

    def to_df(self):
        """
        sqlexec.table('person').columns('name', 'age').to_df()
        """
        return self.table_exec.load(*self.columns).to_df()

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        sqlexec.table('person').columns('name', 'age').to_json('test.json')
        """
        self.table_exec.load(*self.columns).to_json(file_name, encoding)

    def where(self, **kwargs) -> ColumnWhereExec:
        return ColumnWhereExec(self.table_exec.where(**kwargs), *self.columns)

    def page(self, page_num=1, page_size=10) -> ColumnPageExec:
        return ColumnPageExec(TablePageExec(self.table_exec, page_num, page_size), *self.columns)


class TableExec:

    def __init__(self, _exec, table_name):
        self.exec = _exec
        self.table = table_name

    def insert(self, **kwargs):
        """
        Insert data into table, return effect rowcount.

        :param kwargs: {name='张三', age=20}
        return: Effect rowcount
        """
        return self.exec.insert(self.table, **kwargs)

    def save(self, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param kwargs:
        :return: Primary key
        """
        return self.exec.save(self.table, **kwargs)

    def save_select_key(self, select_key: str, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param kwargs:
        :return: Primary key
        """
        return self.exec.save_select_key(select_key, self.table, **kwargs)

    def batch_insert(self, *args):
        """
        Execute sql return effect rowcount
        :param args: [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
        """
        return self.exec.batch_insert(self.table, *args)

    def get(self, column: str):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sqlexec.table('person').get('count(1)')
        """
        sql = get_table_select_sql(self.table, '', LIMIT_1, column)
        return self.exec.do_get(sql, LIMIT_1)

    def count(self):
        """
        sqlexec.table('person').count()
        """
        return self.get(SELECT_COUNT)

    def select(self, *columns):
        """
        sqlexec.table('person').select('name', 'age')
        """
        sql = get_table_select_sql(self.table, '', 0, *columns)
        return self.exec.do_select(sql)

    def select_one(self, *columns):
        """
        sqlexec.table('person').select_one('name', 'age')
        """
        sql = get_table_select_sql(self.table, '', LIMIT_1, *columns)
        return self.exec.do_select_one(sql, LIMIT_1)

    def query(self, *columns):
        """
        sqlexec.table('person').query('name', 'age')
        """
        sql = get_table_select_sql(self.table, '', 0, *columns)
        return self.exec.do_query(sql)

    def query_one(self, *columns):
        """
        sqlexec.table('person').query_one('name', 'age')
        """
        sql = get_table_select_sql(self.table, '', LIMIT_1, *columns)
        return self.exec.do_query_one(sql, LIMIT_1)

    def load(self, *columns) -> Loader:
        """
        sqlexec.table('person').load('name', 'age')
        """
        sql = get_table_select_sql(self.table, '', 0, *columns)

        return self.exec.do_load(sql)

    def insert_from_csv(self, file_name: str, delimiter=',', header=True, columns: Tuple[str] = None, encoding='utf-8'):
        """
        sqlexec.table('person').insert_from_csv('test.csv')
        """
        return self.exec.insert_from_csv(file_name, self.table, delimiter, header, columns, encoding=encoding)

    def insert_from_df(self, df, columns: Tuple[str] = None):
        """
        sqlexec.table('person').insert_from_df(df)
        """
        return self.exec.insert_from_df(df, self.table, columns)

    def insert_from_json(self, file_name: str, encoding='utf-8'):
        """
        sqlexec.table('person').insert_from_json('test.csv')
        """
        return self.exec.insert_from_json(file_name, self.table, encoding=encoding)

    def truncate(self) -> int:
        """ sqlexec.table('person').truncate() """
        return self.exec.truncate(self.table)

    def drop(self) -> int:
        """ sqlexec.table('person').drop() """
        return self.exec.drop(self.table)

    def where(self, **kwargs) -> WhereExec:
        return WhereExec(self.exec, self.table, **kwargs)

    def columns(self, *columns) -> ColumnExec:
        return ColumnExec(self, *columns)

    def page(self, page_num=1, page_size=10) -> TablePageExec:
        return TablePageExec(self,  page_num, page_size)


def table(table_name: str) -> TableExec:
    table_name = table_name.strip()
    assert table_name, "Parameter 'table' must not be none"
    return TableExec(exec, table_name)


def get_condition_arg(k: str, v: object):
    if k.endswith("__eq"):
        return "{} = ?".format(k[:-4]), v
    if k.endswith("__ne"):
        return "{} != ?".format(k[:-4]), v
    if k.endswith("__gt"):
        return "{} > ?".format(k[:-4]), v
    if k.endswith("__lt"):
        return "{} < ?".format(k[:-4]), v
    if k.endswith("__ge"):
        return "{} >= ?".format(k[:-4]), v
    if k.endswith("__gte"):
        return "{} >= ?".format(k[:-5]), v
    if k.endswith("__le"):
        return "{} <= ?".format(k[:-4]), v
    if k.endswith("__lte"):
        return "{} <= ?".format(k[:-5]), v
    if k.endswith("__isnull"):
        return "{} is {}".format(k[:-8], 'null' if v else 'not null'), None
    if k.endswith("__in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} in({})".format(k[:-4], ','.join(['?' for _ in v])), v
    if k.endswith("__in"):
        return "{} in({})".format(k[:-4], '?'), v
    if k.endswith("__not_in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} not in({})".format(k[:-8], ','.join(['?' for _ in v])), v
    if k.endswith("__not_in"):
        return "{} not in({})".format(k[:-8], '?'), v
    if k.endswith("__like"):
        return "{} like ?".format(k[:-6], '?'), v
    if k.endswith("__startswith"):
        return "{} like ?".format(k[:-12]), '{}%'.format(v)
    if k.endswith("__endswith"):
        return "{} like ?".format(k[:-10]), '%{}'.format(v)
    if k.endswith("__contains"):
        return "{} like ?".format(k[:-10]), '%{}%'.format(v)
    if k.endswith("__range") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        col = k[:-7]
        return "{} >= ? and {} <= ?".format(col, col), v
    if k.endswith("__between") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        return "{} between ? and ?".format(k[:-9]), v
    if k.endswith("__range") or k.endswith("__between"):
        return ValueError("Must is instance of Sequence with length 2 when use range or between statement")

    return "{} = ?".format(k), v


def get_where_arg_limit(**kwargs):
    where, args, limit = '', [], 0
    if 'limit' in kwargs:
        limit = kwargs.pop('limit')

    if kwargs:
        conditions, tmp_args = zip(*[get_condition_arg(k, v) for k, v in kwargs.items()])
        tmp_args = [arg for arg in tmp_args if arg is not None]

        for arg in tmp_args:
            if arg is not None:
                if isinstance(arg, Sequence) and not isinstance(arg, str):
                    args.extend(arg)
                else:
                    args.append(arg)
        where = 'WHERE {}'.format(' and '.join(conditions))

    return where, args, limit
