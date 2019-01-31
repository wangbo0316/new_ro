from util import MySQLConnector,ExcelLoader


def UploadINDUSTRY(path,c):
    c.p('正在启动校验程序...')
    c.sleep(1)
    E = ExcelLoader.ExcelLoader(path,0)
    first_row = E.row_values(0)
    industry_index = {}
    for i in ["行业名称","关键字"]:
        if i not in first_row:
            c.p('校验失败，'+i+'字段不存在！',2)
            return
        else:
            industry_index[i] = first_row.index(i)
    c.p('校验通过，正在启动解析程序...')
    results = []
    for i in range(1,E.row_size):
        row = E.row_values(i)
        vo = {"行业名称":row[industry_index['行业名称']],"关键字":row[industry_index['关键字']]}
        results.append(vo)
    c.p('解析成功，正在启动上传程序...')
    try:
        M = MySQLConnector.MySQLConnector()
        M.execute('TRUNCATE TABLE industry')
        M.commit()
        M.upload_dir('industry',results)
        c.p('数据上传成功',3)
    except:
        c.p('数据上传失败，请检查网络连接或联系管理员!',2)

def UploadINDUSTRY_t(path):
    E = ExcelLoader.ExcelLoader(path,0)
    first_row = E.row_values(0)
    industry_index = {}
    for i in ["行业名称","关键字"]:
        if i not in first_row:
            return
        else:
            industry_index[i] = first_row.index(i)
    results = []
    for i in range(1,E.row_size):
        row = E.row_values(i)
        vo = {"行业名称":row[industry_index['行业名称']],"关键字":row[industry_index['关键字']]}
        results.append(vo)
    try:
        M = MySQLConnector.MySQLConnector()
        M.execute('TRUNCATE TABLE industry')
        M.commit()
        M.upload_dir('industry',results)
    except:
        return
