from sqlexec.constant import LIMIT_1

NO_LIMIT = 0

CACHE_SIZE = 256

MAPPER_PATH = 'mapper_path'

MYSQL_SELECT_KEY = "SELECT LAST_INSERT_ID()"

SQLITE_SELECT_KEY = 'SELECT last_insert_rowid()'

MYSQL_COLUMN_SQL = '''SELECT GROUP_CONCAT(CONCAT("`",column_name,"`") SEPARATOR ",") 
                        FROM information_schema.columns WHERE table_schema = (SELECT DATABASE()) AND table_name = ? LIMIT ?'''

POSTGRES_COLUMN_SQL = '''SELECT array_to_string(array_agg(column_name),',') as column_name FROM information_schema.columns 
                          WHERE table_schema='public' and table_name = ? LIMIT ?'''

DYNAMIC_REGEX = '{%|{{|}}|%}'

DEFAULT_KEY_FIELD = 'id'

KEY, SELECT_KEY, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, KEY_STRATEGY = '__key__', '__select_key__', '__table__', '__update_by__', '__update_time__',\
    '__del_flag__', '__key_strategy__'

