LIMIT_1 = 1

CACHE_SIZE = 256

SELECT_COUNT = 'count(1)'

NAMED_REGEX = r':[\w|\d]*'

DEFAULT_KEY_FIELD = 'id'

MYSQL_SELECT_KEY = "SELECT LAST_INSERT_ID()"

SQLITE_SELECT_KEY = 'SELECT last_insert_rowid()'

MYSQL_COLUMN_SQL = '''SELECT GROUP_CONCAT(CONCAT("`",column_name,"`") SEPARATOR ",") 
                        FROM `information_schema`.`columns` WHERE `table_schema` = (SELECT DATABASE()) AND `table_name` = ? LIMIT ?'''

POSTGRES_COLUMN_SQL = '''SELECT array_to_string(array_agg(column_name),',') as column_name FROM information_schema.columns 
                          WHERE table_schema='public' and table_name = ? LIMIT ?'''