from util import MySQLConnector
from datetime import datetime


def getLastMonth(this_month):
    '''
    获取上月日期
    :param this_month: 本月日期 (str)
    :return: 上月日期 (str)
    '''
    Y,m,d = this_month.split("-")
    if m == "01":
        last_month = str(int(Y)-1)+"-12-1"
    else:
        last_month = Y+"-"+str(int(m)-1)+"-1"
    return last_month

def getLastQuarter(this_month):
    '''
    获取上季度末月日期
    :param this_month: 本月日期 (str)
    :return:  上季度末月日期 (str)
    '''
    Y, m, d = this_month.split("-")
    if m in ["01","02","03"]:
        last_quarter = str(int(Y)-1)+"-12-1"
    if m in ["04","05","06"]:
        last_quarter = Y+"-3-1"
    if m in ["07", "08", "09"]:
        last_quarter = Y + "-6-1"
    if m in ["10", "11", "12"]:
        last_quarter = Y + "-9-1"
    return last_quarter


def getLastYear(this_month):
    '''
    获取上年末月日期
    :param this_month: 本月日期 (str)
    :return:  上年末月日期 (str)
    '''
    Y, m, d = this_month.split("-")
    last_year = str(int(Y)-1)+"-12-1"
    return last_year

# a = "2019-08-01"
#
# print(getLastMonth(a),getLastQuarter(a),getLastYear(a))



def Calcullate_RO(dateMonth,c):
    c.p('正在检测日期月份是否合规')
    try:
        this_month = datetime.strptime(dateMonth + "-1","%Y-%m-%d").strftime("%Y-%m-%d")
        last_month = getLastMonth(this_month)
        last_quarter = getLastQuarter(this_month)
        last_year = getLastYear(this_month)
        print(last_month,last_quarter,last_year)
        c.p('日期月份格式正确，当前计算的日期月份为：'+dateMonth)
    except:
        c.p('填写的月份格式错误，标准格式为:2018-12',2)
        return
    c.p('正在连接数据库拉取清单数据...')
    try:
        M = MySQLConnector.MySQLConnector()
        this_month_sql = '''
                        SELECT
                            `集团编号`,
                            `计费号码`,
                            `产品实例`,
                            `区县-按集团归属`,
                            `区县-按客户经理`,
                            `集团归属地市`,
                            `集团名称`,
                            `集团等级`,
                            `专线类型`,
                            `集团专线收入`
                        FROM
                            ro_list
                        WHERE
                            `数据日期` = %s'''
        M.execute(this_month_sql,this_month)
        this_month_data = M.fetall()
        M.execute(this_month_sql, last_month)
        last_month_data = M.fetall()
    except:
        pass
