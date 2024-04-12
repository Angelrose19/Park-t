from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(asctime)s %(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def db_ctx_log(action, connection):
    logger.debug("%s connection <%s>..." % (action, hex(id(connection))))


def do_sql_log(module: str, function: str, sql: str, *args):
    args = args if args else ''
    logger.info("Exec func '%s.%s' \n\t sql: %s \n\t args: %s" % (module, function, sql.strip(), args))


def do_save_log(module: str, function: str, select_key: str, sql: str, *args):
    args = args if args else ''
    logger.info("Exec func '%s.%s', select_key: '%s' \n\t sql: %s \n\t args: %s" % (module, function, select_key, sql.strip(), args))