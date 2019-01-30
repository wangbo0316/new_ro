from util import MySQLConnector,ExcelLoader
from xlrd.xldate import xldate_as_datetime

def UploadRo(path,c):
    c.p('正在启动校验程序...')
    c.sleep(1)
    E = ExcelLoader.ExcelLoader(path,0)
    validata = {
        '数据日期':-1,
        '集团编号':-1,
        '计费号码':-1,
        '产品实例':-1,
        '区县-按集团归属':-1,
        '区县-按客户经理':-1,
        '集团归属地市':-1,
        '地市编号':-1,
        '集团名称':-1,
        '集团等级':-1,
        '专线类型':-1,
        '专线办理时间':-1,
        '专线归档时间':-1,
        '带宽':-1,
        '当月出账':-1,
        '集团专线收入':-1
    }
    first_row = E.row_values(0)
    for i in validata:
        for j,k in enumerate(first_row):
            if i in k :
                validata[i] = j
    for i in validata:
        if validata[i] == -1:
            c.p('校验未通过，"'+i+'"字段不存在或书写错误！',2)
            return

    c.sleep(1)
    c.p('校验通过，正在启动解析程序...')
    results = []
    for row_index in range(1,E.row_size):
        row = E.row_values(row_index)
        vo = {}
        for i in validata:
            if i in ["数据日期","专线办理时间","专线归档时间"]:
                try:
                    vo[i] = xldate_as_datetime(row[validata[i]],0).strftime("%Y-%m-%d")
                except:
                    vo[i] = "1900-1-1"
            else:
                if i in ['当月出账','集团专线收入']:
                    try:
                        vo[i] = float(row[validata[i]])
                    except:
                        vo[i] = 0
                else:
                    vo[i] = row[validata[i]]
        results.append(vo)
    print(results)
    c.p('数据解析成功，正在连接数据库...')
    try:
        M = MySQLConnector.MySQLConnector()
        c.p('连接成功正在上传数据...')
    except:
        c.p('连接失败，请检查网络连接或联系管理员！',2)
        return
    try:
        M.execute("DELETE FROM ro_list WHERE `数据日期` = %s",results[0]['数据日期'])
        M.commit()
        M.upload_dir('ro_list',results)
        M.close()
        c.p('数据上传成功！',3)
    except:
        c.p('数据上传失败，程序异常退出请联系管理员...',2)
        return


