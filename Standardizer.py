import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',       
    'db': 'warehouse'
}

def create_connection(config):
    return pymysql.connect(**config)

def add_column_if_not_exists(cursor, table, column, column_type):
    cursor.execute(f'''
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_name = '{table}' AND column_name = '{column}';
    ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute(f'''
            ALTER TABLE {table}
            ADD COLUMN {column} {column_type};
        ''')

def standardize_data():
    connection = None  
    try:
        connection = create_connection(db_config)

        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS output_table LIKE input_table;
            ''')
            connection.commit()
            add_column_if_not_exists(cursor, 'output_table', 'standardized_degree', 'VARCHAR(255)')
            add_column_if_not_exists(cursor, 'output_table', 'standardized_field_of_study', 'VARCHAR(255)')
            connection.commit()
            cursor.execute('''
                INSERT INTO output_table (id, degree, field_of_study /*, other original columns*/)
                SELECT id, degree, field_of_study /*, other original columns*/ FROM input_table
                ON DUPLICATE KEY UPDATE
                degree = VALUES(degree), field_of_study = VALUES(field_of_study) /*, other columns*/;
            ''')
            connection.commit()
            cursor.execute('''
                UPDATE output_table ot
                INNER JOIN lookup_table lt ON ot.degree = lt.original_value AND lt.column_name = 'degree'
                SET ot.standardized_degree = lt.standardized_value;
            ''')
            connection.commit()
            cursor.execute('''
                UPDATE output_table ot
                INNER JOIN lookup_table lt ON ot.field_of_study = lt.original_value AND lt.column_name = 'field_of_study'
                SET ot.standardized_field_of_study = lt.standardized_value;
            ''')
            connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()

standardize_data()
