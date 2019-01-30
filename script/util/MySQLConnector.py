import pymysql
import re


class MySQLConnector:

    def __init__(self):
        # self.con = pymysql.Connect(host='localhost', port=3306,
        #                                user='root', passwd='0316',
        #                                db="refined_operation", charset='utf8')
        # print('-'*20+"已建立本地MySQL数据库连接"+'-'*20)
        self.con = pymysql.Connect(host='117.187.193.36', port=33060,
                                       user='wangbo', passwd='lc2018',
                                       db="new_ro", charset='utf8')
        print("已建立线上MySQL数据库连接")
        self.cur = self.con.cursor()

    def execute(self,query,args=None):
        self.cur.execute(query,args)
        pass

    def executemany(self,query,args=None):
        self.cur.executemany(query,args)
        print(query,"已完成多次执行操作！")
        pass

    def commit(self):
        self.con.commit()
        pass

    def fetall(self):
        return self.cur.fetchall()

    def close(self):
        self.con.close()
        print('-'*20+"数据库连接已关闭！"+'-'*20)
        pass

    def upload_dir(self,tbl_name,list):
        tupp = []
        for i in list:
            keys = i.keys()

            sql = "insert into "+tbl_name+" ("
            for k in keys:
                sql += "`"+k+ "`,"
            sql = sql[:-1]+") values ("
            for k in keys:
                sql += "%s,"
            sql = sql[:-1] + ")"
            tup = []
            for k in keys:
                if type(i[k]) != str:
                    tup.append(str(i[k]))
                else:
                    tup.append(i[k])
            tupp.append(tuple(tup))
        self.executemany(sql,tupp)
        self.commit()
        print("已将字典列表插入到", tbl_name, "数据表中！")
        pass

    def upload_obj(self,tbl_name,list):
        obj = list[0]
        keys = obj.__dict__.keys()
        sql = "insert into " + tbl_name + " ("
        for k in keys:
            sql += "`" + k + "`,"
        sql = sql[:-1] + ") values ("
        for k in keys:
            sql += "%s,"
        sql = sql[:-1] + ")"
        tupList = []
        for l in list:
            di = l.__dict__
            tup = []
            for k in keys:
                tup.append(di[k])
            tupp = tuple(tup)
            tupList.append(tupp)
        self.executemany(sql, tupList)
        self.commit()
        print("已将对象列表插入到",tbl_name,"数据表中！")
        pass

    def trunc_table(self,tbl_name):
        self.execute("TRUNCATE TABLE "+tbl_name)
        self.commit()
        print("已完成数据表",tbl_name,"的清空操作")
        pass

    def query_dir(self,sql):
        col_names = re.findall(r'SELECT (.*) FROM',sql)[0]
        col_list = col_names.split(",")
        self.execute(sql)
        result = self.fetall()
        dircList = []
        for r in result:
            dirc = {}
            for i in range(0,len(r)):
                dirc[col_list[i].replace("`","")] = r[i]
            dircList.append(dirc)
        return dircList
