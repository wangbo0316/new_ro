from util import MySQLConnector,ExcelLoader
from xlrd.xldate import xldate_as_datetime

def UploadCAPITAL(path,c):
    '''
    上传综资清单
    :param path:
    :param c:
    :return:
    '''
    c.p('正在启动校验程序...')
    c.sleep(1)
    E = ExcelLoader.ExcelLoader(path,0)
    first_row = E.row_values(0)
    capital_index = {}
    for i in ['产品实例','日期']:
        if i not in first_row:
            c.p('校验失败，未包含'+i+'字段',2)
            return
        else:
            capital_index[i] = first_row.index(i)
    c.p('校验成功，正在启动解析程序...')
    results = []
    for i in range(1,E.row_size):
        row = E.row_values(i)
        try:
            a = '%.0f'%int(row[capital_index["产品实例"]])
        except:
            a = row[capital_index["产品实例"]]
        vo = {
            "产品实例":a,
            "日期":xldate_as_datetime(row[capital_index["日期"]],0).strftime("%Y-%m-%d")
        }
        results.append(vo)
    c.p('文件解析成功,正在启动上传程序')
    try:
        M = MySQLConnector.MySQLConnector()
        M.execute("DELETE FROM capital WHERE `日期` = %s",results[0]["日期"])
        M.commit()
        M.upload_dir('capital',results)
        M.close()
        c.p('数据上传成功！',3)
    except:
        c.p('数据上传失败，请检查网络连接或联系管理员！',2)
        return