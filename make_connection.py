from conn_config import BaseConfig
config = BaseConfig()


# create connection to database from config
connection = create_engine(config.GP_CONNECTION_STRING)


def execute_query(sql_query, commit=True, conn_db = connection):
  """
  Execute sql query.
  
  :param sql_query: 
  :param commit: if False - output the result (like `select`), True - execute query (like `insert`, `alter`, `drop`, `create` etc, without output)
  :param conn_db: connection to database
  """
    res = None
    # print(f"SQL\n{sql_query}\n")
    conn = conn_db.raw_connection()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    if commit:
        conn.connection.commit()
    else:
        res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


def execute_procedure(_procedure, proc_args, conn_db=connection):
 """
  Execute sql procedure.
  
  :param _procedure: Procedure name
  :param proc_args: peocedure arguments
  :param conn_db: connection to database
  """
    # print(f"SQL\n{_procedure}\n")
    conn = conn_db.raw_connection()
    cursor = conn.cursor()
    cursor.callproc(_procedure, proc_args)
    conn.connection.commit()
    cursor.close()
    conn.close()
