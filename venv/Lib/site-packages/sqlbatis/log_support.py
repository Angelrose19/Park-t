from sqlexec.log_support import logger


def save_log(table, **kwargs):
    logger.debug("Exec func 'pgsqlx.db.save' \n\t Table: '%s', kwargs: %s" % (table, kwargs))


def do_page_log(function: str, sql: str, page_num, page_size, *args):
    logger.debug(
        "Exec func 'sqlbatis.db.%s', page_num: %d, page_size: %d \n\t sql: %s \n\t args: %s" % (function, page_num, page_size, sql.strip(), args))


def page_log(function: str, sql: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'sqlbatis.db.%s', page_num: %d, page_size: %d \n\tsql: %s \n\targs: %s \n\tkwargs: %s" % (
                 function, page_num, page_size, sql.strip(), args, kwargs))


def page_sql_id_log(function: str, sql_id: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'sqlbatis.dbx.%s', page_num: %d, page_size: %d, sql_id: %s, args: %s, kwargs: %s" % (function, page_num, page_size, sql_id, args, kwargs))


def sql_id_log(function: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func '%s', sql_id: %s, args: %s, kwargs: %s" % (function, sql_id.strip(), args, kwargs))


def sql_id_select_key_log(function: str, select_key: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func 'sqlbatis.dbx.%s', select_key: %s, sql_id: %s, args: %s, kwargs: %s" % (function, select_key, sql_id.strip(), args, kwargs))


def orm_insert_log(function, class_name, **kwargs):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))


def orm_delete_by_id_log(function, class_name, _id, update_by):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', id: %d, update_by: %s" % (function, class_name, _id, update_by))


def orm_by_log(function, class_name, where, *args, **kwargs):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', where: %s, args: %s, kwargs: %s" % (function, class_name, where, args, kwargs))


def orm_inst_log(function, class_name):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s', Class: '%s'" % (function, class_name))


def orm_logical_delete_by_ids_log(function, class_name, ids, update_by, batch_size):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', ids: %s, update_by: %s, batch_size: %s" % (
        function, class_name, ids, update_by, batch_size))


def orm_count_log(function, class_name, **kwargs):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))


def orm_find_log(function, class_name, *fields, **kwargs):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', fields: %s, kwargs: %s" % (function, class_name, fields, kwargs))


def orm_find_by_id_log(function, class_name, _id, *fields):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', id: %d, fields: %s" % (function, class_name, _id, fields))


def orm_find_by_ids_log(function, class_name, ids, *fields):
    logger.debug("Exec func 'sqlbatis.orm.Model.%s' \n\t Class: '%s', ids: %s, fields: %s" % (function, class_name, ids, fields))


def orm_page_log(function, page_num, page_size, class_name, *fields, **kwargs):
    logger.debug("Exec func 'pgsqlx.orm.Model.%s', page_num: %d, page_size: %d \n\t Class: '%s', fields: %s, kwargs: %s" % (
        function, page_num, page_size, class_name, fields, kwargs))


def orm_by_page_log(function, page_num, page_size, class_name, where, *args, **kwargs):
    logger.debug("Exec func 'sqlx-batis.orm.Model.%s', page_num: %d, page_size: %d \n\t Class: '%s', where: %s, args: %s, kwargs: %s" % (
        function, page_num, page_size, class_name, where, args, kwargs))
