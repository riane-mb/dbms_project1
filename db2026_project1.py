import mysql.connector
import os


mysql_connect = None
mvTypeList = list();


def is_int(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False

def is_float(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False

def run_select(select: str) -> str:
    #This function runs the SELECT statement and convert the results to the string

    global mysql_connect
    
    try:
        result_str = ""

        cursor= mysql_connect.cursor()
        cursor.execute(select)
        result_str= convert_result_to_string(cursor)
        return result_str

    except Exception as e:
        print("Error:", e)
        return ""



def convert_result_to_string(cursor):
    #This function converts result of mysql connector in cursor to the string.

    try:
        # Get column metadata
        columns = cursor.description
        column_count = len(columns)

        # Print column headers
        result_str = ""
        for col in columns:
            result_str += col[0] + "\t"
        result_str += "\n"

        # Separator line (similar to "--" * len)
        len_line = len(result_str)
        result_str += "-" * (2 * len_line) + "\n"

        
        for row in cursor.fetchall():
            for i in range(len(row)):
                result_str += str(row[i]) + "\t"
            result_str += "\n"

        result_str += "=" * (2 * len_line) + "\n"


        return result_str

    except Exception as e:
        print("Error:", e)
        return ""




# This function reads the table-like file, converts each line to SQL
# and returns the SQL string which contains a set of SQL statememts.
def convert_csv_to_sqls(file_name: str, table_name: str, create_table_option: int):
    global mvTypeList

    try:
        csv_file = open(file_name, "r", encoding="utf-8")
        header = csv_file.readline().strip()  # read the header
        sql_list = []
        
        tokens = header.split(",")

        if (create_table_option==1):
            create="CREATE TABLE "+ table_name + "("
            for i,token in enumerate(tokens):
                create += token + " varchar(100)"
                if (i!=len(tokens)-1):
                    create+=","
            create+=");"
            sql_list.append(create)
        elif create_table_option==2:
            first_line= csv_file.readline().strip()
            first_values=first_line.split(",")
            create="CREATE TABLE "+ table_name + " ("
            for i,token in enumerate(tokens):
                val=first_values[i].strip()
                if is_int(val):
                    create += token + " int"
                elif is_float(val):
                    create += token + " float"
                else:
                    create += token + " varchar(100)"
                if (i!=len(tokens)-1):
                    create+=","
            create+=");"
            sql_list.append(create)
            sql_list.append(convert_string_to_insert(first_line, table_name))
            


        for line in csv_file:
            sql_list.append(convert_string_to_insert(line.strip(),table_name))
        
        return sql_list

    except Exception as e:
        print("Error in convert_csv_to_sqls():", e)
        return None




def convert_string_to_insert(line: str, table_name: str) -> str:
    
    toks = line.strip().split(",")
    sql = f"INSERT INTO {table_name} VALUES ("

    global mvTypeList

    for i,t in enumerate(toks):
        t=t.strip()
        if (is_int(t) or is_float(t)):
            sql+=str(t)
        elif t=='NULL':
            sql+=str('NULL')
        else:
            sql+= "'"+str(t)+"'"
        if (i!=len(toks)-1):
            sql+=","

    sql+=");"


    return sql







def run_multiple_queries(sql_list):
    global mysql_connect
    
    #This fucntion runs multiple queries."
    try:
        ""
        cursor=mysql_connect.cursor()
        for query in sql_list:
            cursor.execute(query)
        mysql_connect.commit()
     
    except Exception as e:
        # Rollback if any query fails
        print("Error in run_multiple_queries():", e)
        try:
            mysql_connect.rollback()
        except:
            pass







def drop_all(database):
    # This function drop all tables in the current database (this.database).
    global mysql_connect

    try:
        query_list=[]
        cursor=mysql_connect.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='"+database+"';")
        
        for row in cursor.fetchall():
            requete="DROP TABLE "+row[0]+";"
            query_list.append(requete)
        run_multiple_queries(query_list)

        ""
    except Exception as e:
        print("Error in drop_all():", e)
        
        
        

def import_data(csv_file: str, tab_name: str, create_table_option: int):
    # This fucntion imports csvFile to tabName
    #   - createTableOption 0: Do not include the create table statement
    #   - createTableOption 1: Include the create table statement without type guessing
    #   - createTableOption 2: Include the create table statement with type guessing

    insert_list = convert_csv_to_sqls(csv_file, tab_name, create_table_option)

    run_multiple_queries(insert_list)


def cmd_interpret(cmd: str, database) -> str:
    cmd = cmd.lower().strip()
    result_str = ""
	
    # print available commands
    if cmd == "help":
        result_str = (
            "\n#Usage#\n"
            "help : print tool commands\n"
            "pwd: print the current working directory \n"
            "ls [path]: print files in \"path\"\n"
            "exit: exit the tool\n"
            "import FILE_NAME TAB_NAME: import FILE_NAME to TAB_NAME without type guessing\n"
            "timport FILE_NAME TAB_NAME: import FILE_NAME to TAB_NAME with type guessing\n"
            "read TAB_NAME: print all records in TAB_NAME\n"
            "show tables: print all tables in the current database\n"
            "desc TAB_NAME: print column names and types for TAB_NAME in the column order\n"
            "find tables column=COL_NAME: find tables which contain the attribute COL_NAME\n"
            "find tables col_type=COL_TYPE: find tables which contain the attribute type COL_TYPE\n"
            "drop all: drop all tables in the current database\n"
        )
		
    # print current working directory
    elif cmd == "pwd":
        result_str = "\n" + os.getcwd() + "\n"
		
    # show the file list in the current directy (ls) or in the specified directory (ls PATH)
    elif cmd == "ls" or cmd.startswith("ls "):
        specified_path = cmd.replace("ls", "").strip()
        path = specified_path if specified_path else "."
        result_str = "\n"
        for name in os.listdir(path):
            full = os.path.join(path, name)
            if os.path.isdir(full):
                result_str += f"({name})\n"
            else:
                result_str += name + "\n"
                
                
    # import the csv file to the table in DBMS without type guessing
    elif cmd.startswith("import "):
        toks = cmd.split()
        if len(toks) < 3:
            result_str = " #command error"
        else:
            file_path = toks[1]  # csv file path
            tab_name = toks[2]   # table name to be created
            import_data(file_path, tab_name, 1)

    # import the csv file to the table in DBMS with type guessing
    elif cmd.startswith("timport "):
        toks = cmd.split()
        if len(toks) < 3:
            result_str = " #command error"
        else:
            file_path = toks[1]  # csv file path
            tab_name = toks[2]   # table name to be created
            import_data(file_path, tab_name, 2)
           

    # read command
    elif cmd.startswith("read "):
        toks = cmd.split()
        if len(toks) < 2:
            result_str = " #command error"
        else:
            tab_name = toks[1]
            sql = 'SELECT * FROM '+ tab_name+';'
            result_str = run_select(sql)

    # show tables command
    elif cmd == "show tables":
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = '"+database+"';"
        result_str= run_select(sql)
        

    # desc command
    elif cmd.startswith("desc "):
        tname = cmd.replace("desc ", "").strip()
        sql= "SELECT column_name, column_type FROM information_schema.columns WHERE table_name='"+tname+"' and table_schema='"+database+"' order by ORDINAL_POSITION;"
        result_str=run_select(sql)
      


    # find tables column=COL_NAME
    elif cmd.startswith("find tables column="):
        col_name = cmd.replace("find tables column=", "").strip()
        sql = "SELECT DISTINCT C.TABLE_NAME FROM information_schema.COLUMNS C WHERE C.TABLE_SCHEMA='"+database+"' and C.COLUMN_NAME='"+col_name+"';"
        result_str = run_select(sql)
    
    # find tables col_type=COL_NAME
    elif cmd.startswith("find tables col_type="):
        col_type = cmd.replace("find tables col_type=", "").strip()
        if col_type not in {"int", "varchar", "float"}:
            result_str = " #command error: type must be int, varchar, or float"
        else:
            sql = "SELECT DISTINCT C.TABLE_NAME FROM information_schema.COLUMNS C WHERE C.TABLE_SCHEMA='"+database+"' and COLUMN_TYPE LIKE '%"+col_type+"%';"
            result_str = run_select(sql)
        


    # drop all
    elif cmd.startswith("drop all"):
        drop_all(database)


    return result_str




def main():
    host = "localhost"
    port = 3306
    database = "week11"
    user = "root"
    password = "PASSWORD" 

    global mysql_connect
        
    mysql_connect = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


    try:
        while True:
            try:
                cmd = input("Riane MBODJI>") 
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if cmd.strip().lower() == "exit":
                break
                
            out = cmd_interpret(cmd, database)
            if out:
                print(out)
    finally:
        mysql_connect.close()

if __name__ == "__main__":
    main()