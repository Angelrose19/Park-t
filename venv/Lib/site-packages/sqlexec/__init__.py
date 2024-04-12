from executor import (
    connection,
    transaction,
    with_connection,
    with_transaction,
    get_connection,
    close,
    Driver,
    Engine,
    init as _init
)
from .exec import (
    execute,
    insert,
    save,
    save_sql,
    save_select_key,
    save_sql_select_key,
    batch_insert,
    batch_execute,
    get,
    select,
    select_one,
    query,
    query_one,
    do_execute,
    do_save_sql,
    do_save_sql_select_key,
    do_get,
    do_select,
    do_select_one,
    do_query,
    do_query_one,
    select_page,
    query_page,
    do_select_page,
    do_query_page,
    load,
    do_load,
    insert_from_csv,
    insert_from_df,
    insert_from_json,
    truncate,
    drop
)

from .sql_exec import sql
from .page_exec import page
from .table_exec import table
from .dialect import Dialect


def init(*args, **kwargs):
    """
    Compliant with the Python DB API 2.0 (PEP-249).

    from sqlexec
    sqlexec.init('test.db', driver='sqlite3', show_sql=True, debug=True)
    or
    sqlexec.init("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5, show_sql=True, debug=True)
    or
    sqlexec.init(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql', pool_size=5, show_sql=True, debug=True)

    Addition parameters:
    :param driver=None: str|Driver, import driver, 'import pymysql'
    :param pool_size=0: int, default 0, size of connection pool
    :param show_sql=False: bool,  if True, print sql
    :param debug=False: bool, if True, print debug context

    Other parameters of connection pool refer to DBUtils: https://webwareforpython.github.io/DBUtils/main.html#pooleddb-pooled-db
    """

    engine = _init(*args, **kwargs)
    Dialect.init(engine)
