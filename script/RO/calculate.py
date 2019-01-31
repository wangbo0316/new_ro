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
    M = MySQLConnector.MySQLConnector()
    sql = 'SELECT `集团编号`,`计费号码`,`产品实例`,`区县-按集团归属`,`区县-按客户经理`,`集团归属地市`,`集团名称`,`集团等级`,`专线类型`,`集团专线收入` FROM  ro_list WHERE `数据日期` = '
    try:
        this_month_data = M.query_dir(sql+'"'+this_month+'"')
        last_year_data = M.query_dir(sql+'"'+last_year+'"')
        last_quarter_data = M.query_dir(sql+'"'+last_quarter+'"')
        last_month_data = M.query_dir(sql+'"'+last_month+'"')
        capital_data = [i['产品实例'] for i in M.query_dir('SELECT `产品实例`,`日期` FROM capital WHERE `日期` = "'+this_month+'"')]
        marketing_data = {}
        for i in M.query_dir('SELECT `计费号码`,`活动标签` FROM marketing'):
            marketing_data[i["计费号码"]] = i['活动标签']
        industry_data = {}
        M.execute('SELECT DISTINCT `行业名称` FROM industry')
        industry_all = [i[0] for i in M.fetall()]
        for i in industry_all:
            M.execute('SELECT `关键字` FROM industry WHERE `行业名称`="'+i+'"')
            industry_data[i] = [i[0] for i in M.fetall()]
        M.execute('''
                SELECT
                    `集团编号`,
                    `数据日期`,
                    COUNT(DISTINCT `产品实例`)
                FROM
                    ro_list
                GROUP BY
                    `集团编号`,
                    `数据日期`
                HAVING
                    COUNT(`产品实例`) >= 10
                AND `数据日期` = %s
                ''', this_month)
        big_pro_ids = [l[0] for l in M.fetall()]
        c.p('数据拉取成功，正在执行计算，消耗时间较长请勿关闭程序...')
    except:
        c.p('数据拉取失败，请检查网络连接或联系管理员',2)
        return
    # 生成产品实例编码列表

    this_ids = [i['产品实例'] for i in this_month_data]
    year_ids = [i['产品实例'] for i in last_year_data]
    quarter_ids = [i['产品实例'] for i in last_quarter_data]
    month_ids = [i['产品实例'] for i in last_month_data]

    results = []
    # 开始遍历本月清单
    for i in this_month_data:
        vo_year = {**i}
        vo_year['状态口径'] = "年度"
        vo_year['数据日期'] = this_month
        vo_month = {**i}
        vo_month['状态口径'] = "月度"
        vo_month['数据日期'] = this_month
        vo_quarter = {**i}
        vo_quarter['状态口径'] = "季度"
        vo_quarter['数据日期'] = this_month
        if i['产品实例'] in year_ids:
            vo_year['状态'] = "保有"
        else:
            vo_year['状态'] = "新增"

        if i['产品实例'] in month_ids:
            vo_month['状态'] = "保有"
        else:
            vo_month['状态'] = "新增"

        if i['产品实例'] in quarter_ids:
            vo_quarter['状态'] = "保有"
        else:
            vo_quarter['状态'] = "新增"
        results.append(vo_month)
        results.append(vo_year)
        results.append(vo_quarter)
    # 开始遍历上月清单
    for i in last_month_data:
        vo = {**i}
        vo['状态口径'] = "月度"
        vo['数据日期'] = this_month
        if i['产品实例'] not in this_ids:
            vo['状态'] = "离网"
            results.append(vo)
    # 开始遍历上季度清单
    for i in last_quarter_data:
        vo = {**i}
        vo['状态口径'] = "季度"
        vo['数据日期'] = this_month
        if i['产品实例'] not in this_ids:
            vo['状态'] = "离网"
            results.append(vo)
    # 开始遍历上年清单
    for i in last_year_data:
        vo = {**i}
        vo['状态口径'] = "年度"
        vo['数据日期'] = this_month
        if i['产品实例'] not in this_ids:
            vo['状态'] = "离网"
            results.append(vo)

    # 遍历结果数组
    for i in results:
        # 数据一致
        if i['状态'] != "离网":
            if i['产品实例'] in capital_data:
                i['数据一致'] = '已匹配'
            else:
                i['数据一致'] = '未匹配'
        else:
            i['数据一致'] = '-'
        # 营销活动
        if i['计费号码'] in marketing_data.keys():
            i["营销活动"] = marketing_data[i["计费号码"]]
        else:
            i['营销活动'] = "无营销活动记录"
        # 行业
        i["行业"] = "其他"
        for j in industry_data:
            for k in industry_data[j]:
                if k in i["集团名称"]:
                    i["行业"] = j
        # 大项目

        if i['产品实例'] in big_pro_ids:
            i["是否大项目"] = '是'
        else:
            i['是否大项目'] = '否'



    c.p('计算完成，正在将计算结果保存至数据库...')
    try:
        M.execute('DELETE FROM ro_results WHERE `数据日期`=%s',this_month)
        M.commit()
        M.upload_dir('ro_results',results)
        c.p('结果数据保存成功！',3)
    except:
        c.p('结果数据保存失败，请联系管理员！', 2)
        return

def Calcullate_RO_t(dateMonth):
    try:
        this_month = datetime.strptime(dateMonth + "-1","%Y-%m-%d").strftime("%Y-%m-%d")
        last_month = getLastMonth(this_month)
        last_quarter = getLastQuarter(this_month)
        last_year = getLastYear(this_month)
        print(last_month,last_quarter,last_year)
    except:
        return
    M = MySQLConnector.MySQLConnector()
    sql = 'SELECT `集团编号`,`计费号码`,`产品实例`,`区县-按集团归属`,`区县-按客户经理`,`集团归属地市`,`集团名称`,`集团等级`,`专线类型`,`集团专线收入` FROM  ro_list WHERE `数据日期` = '
    try:
        this_month_data = M.query_dir(sql+'"'+this_month+'"')
        last_year_data = M.query_dir(sql+'"'+last_year+'"')
        last_quarter_data = M.query_dir(sql+'"'+last_quarter+'"')
        last_month_data = M.query_dir(sql+'"'+last_month+'"')
        capital_data = [i['产品实例'] for i in M.query_dir('SELECT `产品实例`,`日期` FROM capital WHERE `日期` = "'+this_month+'"')]
        marketing_data = {}
        for i in M.query_dir('SELECT `计费号码`,`活动标签` FROM marketing'):
            marketing_data[i["计费号码"]] = i['活动标签']
        industry_data = {}
        M.execute('SELECT DISTINCT `行业名称` FROM industry')
        industry_all = [i[0] for i in M.fetall()]
        for i in industry_all:
            M.execute('SELECT `关键字` FROM industry WHERE `行业名称`="'+i+'"')
            industry_data[i] = [i[0] for i in M.fetall()]
        M.execute('''
                SELECT
                    `集团编号`,
                    `数据日期`,
                    COUNT(DISTINCT `产品实例`)
                FROM
                    ro_list
                GROUP BY
                    `集团编号`,
                    `数据日期`
                HAVING
                    COUNT(`产品实例`) >= 10
                AND `数据日期` = %s
                ''', this_month)
        big_pro_ids = [l[0] for l in M.fetall()]
    except:
        return
    # 生成产品实例编码列表

    this_ids = [i['产品实例'] for i in this_month_data]
    year_ids = [i['产品实例'] for i in last_year_data]
    quarter_ids = [i['产品实例'] for i in last_quarter_data]
    month_ids = [i['产品实例'] for i in last_month_data]

    results = []
    # 开始遍历本月清单
    for i in this_month_data:
        vo_year = {**i}
        vo_year['状态口径'] = "年度"
        vo_year['数据日期'] = this_month
        vo_month = {**i}
        vo_month['状态口径'] = "月度"
        vo_month['数据日期'] = this_month
        vo_quarter = {**i}
        vo_quarter['状态口径'] = "季度"
        vo_quarter['数据日期'] = this_month
        if i['产品实例'] in year_ids:
            vo_year['状态'] = "保有"
        else:
            vo_year['状态'] = "新增"

        if i['产品实例'] in month_ids:
            vo_month['状态'] = "保有"
        else:
            vo_month['状态'] = "新增"

        if i['产品实例'] in quarter_ids:
            vo_quarter['状态'] = "保有"
        else:
            vo_quarter['状态'] = "新增"
        results.append(vo_month)
        results.append(vo_year)
        results.append(vo_quarter)
    # 开始遍历上月清单
    for i in last_month_data:
        vo = {**i}
        vo['状态口径'] = "月度"
        vo['数据日期'] = this_month
        if i['产品实例'] not in this_ids:
            vo['状态'] = "离网"
            results.append(vo)
    # 开始遍历上季度清单
    for i in last_quarter_data:
        vo = {**i}
        vo['状态口径'] = "季度"
        vo['数据日期'] = this_month
        if i['产品实例'] not in this_ids:
            vo['状态'] = "离网"
            results.append(vo)
    # 开始遍历上年清单
    for i in last_year_data:
        vo = {**i}
        vo['状态口径'] = "年度"
        vo['数据日期'] = this_month
        if i['产品实例'] not in this_ids:
            vo['状态'] = "离网"
            results.append(vo)

    # 遍历结果数组
    for i in results:
        # 数据一致
        if i['状态'] != "离网":
            if i['产品实例'] in capital_data:
                i['数据一致'] = '已匹配'
            else:
                i['数据一致'] = '未匹配'
        else:
            i['数据一致'] = '-'
        # 营销活动
        if i['计费号码'] in marketing_data.keys():
            i["营销活动"] = marketing_data[i["计费号码"]]
        else:
            i['营销活动'] = "无营销活动记录"
        # 行业
        i['行业'] = "其他"
        for j in industry_data:
            for k in industry_data[j]:
                if k in i["集团名称"]:
                    i["行业"] = j
        # 大项目
        if i['产品实例'] in big_pro_ids:
            i["是否大项目"] = '是'
        else:
            i['是否大项目'] = '否'

    M.execute('DELETE FROM ro_results WHERE `数据日期`=%s',this_month)
    M.commit()
    M.upload_dir('ro_results',results)
