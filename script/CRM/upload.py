from util import MySQLConnector,ExcelLoader


def UploadCRM(path,c):
    c.p('CRM路径读取成功...')
    c.sleep(1)
    c.p('当前路径为：' + path)