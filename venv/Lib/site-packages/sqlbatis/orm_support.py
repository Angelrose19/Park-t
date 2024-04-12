from .constant import NO_LIMIT
from .sql_support import simple_sql, get_table_select_sql
from typing import Sequence, Union, List, Tuple
from sqlexec.table_exec import get_condition_arg, get_where_arg_limit
from . import db
from sqlexec import Dialect


class FieldExec:
    def __init__(self, cls, *fields):
        self.cls = cls
        self.fields = fields

    def where(self, **kwargs):
        return WhereExec(self.cls, *self.fields, **kwargs)

    def page(self, page_num=1, page_size=10):
        return OrmPage(self.where(), page_num, page_size)

    def find(self, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find(name='张三', age=55)
        """
        return self.cls.find(*self.fields, **kwargs)

    def find_one(self, **kwargs):
        """
        Return unique result(object) or None if no result.
        person = Person.fields('id', 'name', 'age').find_one(name='张三', age=55)
        """
        return self.cls.find_one(*self.fields, **kwargs)

    # def find_by(self, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result.
    #     rows = Person.fields('id', 'name', 'age').find_by('where name=?', '李四')
    #     """
    #     return [self.cls.to_obj(**d) for d in self.query_by(where, *args, **kwargs)]

    def find_by_id(self, _id: Union[int, str]):
        """
        Return one class object or None if no result.
        person = Person.fields('id', 'name', 'age').find_by_id(1)
        :param _id: key
        """
        return self.cls.find_by_id(_id, *self.fields)

    def find_by_ids(self, *ids):
        """
        Return list(class object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find_by_ids(1,2)
        :param ids: List of key
        """
        return self.cls.find_by_ids(ids, *self.fields)

    def query(self, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query(name='张三', age=55)
        """
        return self.cls.query(*self.fields, **kwargs)

    def query_one(self, **kwargs):
        """
        Return unique result(dict) or None if no result.
        persons = Person.fields('id', 'name', 'age').query_one(name='张三', age=55)
        """
        return self.cls.query_one(*self.fields, **kwargs)

    # def query_by(self, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result.
    #     rows = Person.fields('id', 'name', 'age').query_by('where name=?', '李四')
    #     """
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_query(sql, *args)

    def query_by_id(self, _id: Union[int, str]):
        """
        Return one row(dict) or None if no result.
        person = Person.fields('id', 'name', 'age').query_by_id(1)
        :param _id: key
        """
        return self.cls.query_by_id(_id, *self.fields)

    def query_by_ids(self, *ids):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query_by_ids(1,2)
        :param ids: List of key
        """
        return self.cls.query_by_ids(ids, *self.fields)

    def select(self, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').select(name='张三', age=55)
        """
        return self.cls.select(*self.fields, **kwargs)

    def select_one(self, **kwargs):
        """
        Return unique result(tuple) or None if no result.
        row = Person.fields('id', 'name', 'age').select_one(name='张三', age=55)
        """
        return self.cls.select_one(*self.fields, **kwargs)

    # def select_by(self, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result.
    #     rows = Person.select_by_where('where name=?', '李四')
    #     """
    #     assert where and where.strip().lower().startswith('where'), "Parameter 'where' must startswith 'WHERE'"
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_select(sql, *args)

    def select_by_id(self, _id: Union[int, str]):
        """
        Return one row(dict) or None if no result.
        row = Person.fields('id', 'name', 'age').select_by_id(1)
        :param _id: key
        """
        return self.cls.select_by_id(_id, *self.fields)

    def select_by_ids(self, *ids):
        """
        Return list(dict) or empty list if no result.
        rows = Person.select_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of key
        :param fields: Default select all fields if not set
        """
        return self.cls.select_by_ids(ids, *self.fields)

    def find_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self.cls.find_page(page_num, page_size, *self.fields, **kwargs)

    # def find_page_by(self, page_num: int, page_size: int, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
    #     rows = Person.find_by_page(1, 10, 'where name=?', '李四')
    #     """
    #     return [self.cls.to_obj(**d) for d in self.query_page_by(page_num, page_size, where, *args, **kwargs)]

    def query_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self.cls.query_page(page_num, page_size, *self.fields, **kwargs)

    # def query_page_by(self, page_num: int, page_size: int, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
    #     rows = Person.fields('id', 'name', 'age').query_by_page(1, 10, 'where name=?', '李四')
    #     """
    #     assert where and where.strip().lower().startswith('where'), "Parameter 'where' must startswith 'WHERE'"
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_query_page(sql, page_num, page_size, *args)

    def select_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').select_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self.cls.select_page(page_num, page_size, *self.fields, **kwargs)

    # def select_page_by(self, page_num: int, page_size: int, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
    #     rows = Person.fields('id', 'name', 'age').select_by_page(1, 10, 'where name=?', '李四')
    #     """
    #     assert where and where.strip().lower().startswith('where'), "Parameter 'where' must startswith 'WHERE'"
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_select_page(sql, page_num, page_size, *args)


class WhereExec:
    def __init__(self, cls, *fields, **kwargs):
        self.cls = cls
        self._fields = fields
        self.kwargs = kwargs

    def fields(self, *fields):
        self._fields = fields
        return self

    def where(self, **kwargs):
        self.kwargs = kwargs
        return self

    def page(self, page_num=1, page_size=10):
        return OrmPage(self, page_num, page_size)

    def delete(self):
        """
        Physical delete
        rowcount = Person.delete_by('where name=? and age=?', '张三', 55)
        return: Effect rowcount
        """
        return self.cls.delete(**self.kwargs)

    def count(self):
        """
        Automatically add 'limit ?' where if not.
        count = Person.count_by('where name=?', '李四')
        """
        return self.cls.count(**self.kwargs)

    def exists(self):
        return self.cls.exists(**self.kwargs)

    def select(self):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').select('李四')
        """
        return self.cls.select(*self._fields, **self.kwargs)

    def query(self):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').query('李四')
        """
        return self.cls.query(*self._fields, **self.kwargs)

    def find(self):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').find('李四')
        """
        return [self.cls.to_obj(**d) for d in self.query(*self._fields, **self.kwargs)]

    def select_page(self, page_num=1, page_size=10):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').select('李四')
        """
        return self.cls.select_page(*self._fields, **self.kwargs)

    def query_page(self, page_num=1, page_size=10):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').query('李四')
        """
        return self.cls.query_page(*self._fields, **self.kwargs)

    def find_page(self, page_num=1, page_size=10):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').find('李四')
        """
        return [self.cls.to_obj(**d) for d in self.query_page(page_num, page_size)]


class OrmPage:
    
    def __init__(self, exec: WhereExec, page_num=1, page_size=10):
        self.exec = exec
        self.page_num = page_num
        self.page_size = page_size

    def query(self, *fields, **kwargs):
        """
        Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.cls.query_page(self.page_num, self.page_size, *fields, **kwargs)

    def select(self, *fields, **kwargs):
        """
        Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.cls.select_page(self.page_num, self.page_size, *fields, **kwargs)

    def where(self, **kwargs):
        self.exec.kwargs = kwargs
        return self

    def fields(self, *fields) -> WhereExec:
        return self.exec.fields(*fields)

    def find(self, *args, **kwargs):
        """
        Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.exec.cls.find_page(self.page_num, self.page_size, *fields, **kwargs)


def split_ids(ids: Sequence[int], batch_size):
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]


def get_table_name(class_name):
    for i in range(1, len(class_name) - 1)[::-1]:
        if class_name[i].isupper():
            class_name = class_name[:i] + '_' + class_name[i:]
    return class_name.lower()
