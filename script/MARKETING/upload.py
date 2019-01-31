from util import MySQLConnector,ExcelLoader


def UploadMARKETING(path,c):
    c.p('正在启动校验程序...')
    c.sleep(1)
    E = ExcelLoader.ExcelLoader(path,0)
    first_row = E.row_values(0)
    market_index = {}
    for i in ['手机号码','活动标签']:
        if i not in first_row:
            c.p('校验失败，'+i+'字段不存在！',2)
            return
        else:
            market_index[i] = first_row.index(i)
    c.p('校验成功，正在启动解析程序...')
    results = []
    for i in range(1,E.row_size):
        row = E.row_values(i)
        try:
            a = '%.0f'%int(row[market_index["手机号码"]])
        except:
            a = row[market_index["手机号码"]]
        vo = {
            "计费号码":a,
            "活动标签":row[market_index["活动标签"]]
        }
        results.append(vo)
    c.p('文件解析成功,正在启动上传程序')
    try:
        M = MySQLConnector.MySQLConnector()
        M.upload_dir('marketing',results)
        M.close()
        c.p('数据上传成功!',3)
    except:
        c.p('数据上传失败，请检查网络连接或联系管理员',2)
        return
