import pymysql


class StringHandler:

    def __init__(self):
        self.data = []
        self.dictionary = {}

    def get_input_name(self):
        input_string_00 = input("Please choose to organize files or add new vid_num into DB (ADD/ORG):")
        if input_string_00.upper() == "ADD":
            input_string = input("Please enter the VidHead, and separate w/ comma (ABP, IPX, GVG): ")
            if input_string is None:
                print("Invalid input, Exit!")
                exit(1)
            string_list = input_string.split(",")
            for string in string_list:
                string.strip()
                if len(string) > 0:
                    self.data.append(string.upper())
            self.check_db()
        elif input_string_00.upper() == "ORG":
            self.enumerate_db()
        else:
            print("Illegal input, please choose ADD or ORG")
            exit(1)

    def check_db(self):
        db = pymysql.connect("localhost", "haolun", "sis001", "PornDB", charset='utf8')
        cursor = db.cursor()
        for vid_head in self.data:
            sql_select = "select * from videonumber where VidHead = '" + vid_head + "'"
            cursor.execute(sql_select)
            row = cursor.fetchone()
            if row is not None:
                row_list = list(row)
                print(row_list)
                self.dictionary.update({row_list[0].upper(): row_list[1].upper()})
            else:
                input_string = input("Cannot find related VidHead: " + vid_head +
                                     " in DB, please input 'VidHead,CompanyName': ")
                if input_string is None:
                    print("Failed to get VidHead info from user, VidHead is " + vid_head)
                    exit(1)
                string_list = input_string.split(",")
                if len(string_list) != 2:
                    print("Illegal input, you have to input 'VidHead,CompanyName'")
                    exit(1)
                sql_update = "insert into videonumber values ('" + string_list[0].upper() + "', '" + \
                             string_list[1].upper() + "')"
                cursor.execute(sql_update)
                db.commit()
                self.dictionary.update({string_list[0].upper(): string_list[1].upper()})
        cursor.close()

    def enumerate_db(self):
        db = pymysql.connect("localhost", "haolun", "sis001", "PornDB", charset='utf8')
        cursor = db.cursor()
        sql_select = "select * from videonumber"
        cursor.execute(sql_select)
        rows = cursor.fetchall()
        for row in rows:
            self.dictionary.update({row[0].upper(): row[1].upper()})
        cursor.close()
