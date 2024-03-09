import sqlite3
import pandas as pd

db_file = "../db.sqlite3"

questions_file = "../../files/Behavioral Questions - Update.xlsx"

excel_data_sheet_name = ["Top 10 Behavioral Questions", "Communication", "Decision Making", "Teamwork", "Leadership"]
sheet_name_to_db = ['top10', 'communication', 'decision_making', 'teamwork', 'leadership']

conn = sqlite3.connect(db_file)


# show all tables
def show_table():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
    cursor.close()


# show table_info
def show_table_info(table_name):
    cursor = conn.cursor()
    sql_query = "PRAGMA table_info(table_name)"
    # table_name = 'interview_question'
    cursor.execute(sql_query.replace('table_name', table_name))
    index_list = cursor.fetchall()
    print("Indexes for table", table_name)
    for index in index_list:
        print(index)
    cursor.close()


# show table_info
def save_data_to_db(sheet_name: str, sheet_name_db: str, question_id: int = 0):
    excel_data_sheet1 = pd.read_excel(questions_file, sheet_name=sheet_name)

    for index, row in excel_data_sheet1.iterrows():
        # print("Index:", index)
        # print("Row data:")
        # print(row[1])
        cursor = conn.cursor()
        data_entry = (question_id, row[1], 'IC', sheet_name_db)
        # print(data_entry)
        cursor.execute("INSERT INTO interview_question VALUES (?, ?, ?, ?)", data_entry)
        conn.commit()
        cursor.close()
        question_id = question_id + 1
        # print(question_id)

    return question_id


# main
# show_table()
temp_id = 0
for i, j in zip(excel_data_sheet_name, sheet_name_to_db):
    temp_id = save_data_to_db(i, j, temp_id)
