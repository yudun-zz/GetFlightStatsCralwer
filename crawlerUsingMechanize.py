import myParser
import mechanize 
import cookielib
from bs4 import BeautifulSoup, NavigableString
import datetime

target=('http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airport=%28EZE%29+Ministro+'
'Pistarini+Airport&airportQueryDate=2011-05-04&airportQueryTime=12&airlineToFilter=&airportQu'
'eryType=0&x=10&y=7')
username='myyudun'
password='0'
base_url = 'https://www.flightstats.com'
login_action = '/go/Login/login.do'
login_url=base_url+login_action

cookie_file = 'login.cookies'
# set up a cookie jar to store cookies
cj = cookielib.MozillaCookieJar(cookie_file)

br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(True)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 
    ('Mozilla/5.0 (Windows NT 6.1; WOW64)'
     'AppleWebKit/537.36 (KHTML, like Gecko)'
     'Chrome/33.0.1750.154 Safari/537.36'))
]##模拟浏览器头

###################################  准备工作结束  #######################
br.open(login_url)
cj.save()
br.select_form(nr=0)##选择表单1，
br.form.set_all_readonly(False) # allow changing the .value of all controls
br.form['username'] = username
br.form['arbitraryName'] = password
br.form['originalUserNameTextBox'] = username
br.form['password'] = 'hzSGBxCxIh4OKcSkJj+T/A=='
br.form['__checkbox_remember'] = '__checkbox_true'
br.submit()##提交表单
print "-------------------第一次尝试登录--------------------"
br.open(target)
cj.save()
br.select_form(nr=0)##选择表单1，
br.form.set_all_readonly(False) # allow changing the .value of all controls
br.form['username'] = username
br.form['arbitraryName'] = password
br.form['originalUserNameTextBox'] = username
br.form['password'] = 'hzSGBxCxIh4OKcSkJj+T/A=='
br.form['__checkbox_remember'] = '__checkbox_true'
br.submit()##提交表单
print "------------------第二次尝试登录-------------------"

response = br.open(base_url)
cj.save()
soup = BeautifulSoup(response.read())
mainPageAfterLogin = soup.select("#headerLogin")

s = ""
for tag in mainPageAfterLogin:
        s+=tag.text.strip()
if("myyudun" in s):
    print "成功登陆！！！！！"
    print s
else:
    sys.exit(1)

###################################  登陆过程结束  #######################
###################################  开始爬数据！！#######################
t0=datetime.time(0, 0, 0)
t1=datetime.time(6, 0, 0)
t2=datetime.time(9, 0, 0)
t3=datetime.time(12, 0, 0)
t4=datetime.time(15, 0, 0)
t5=datetime.time(18, 0, 0)
t6=datetime.time(21, 0, 0)
t7=datetime.time(23, 59, 59)
##timeValueL=["0","6","9","12","15","18","21"]
timeValueL=["0","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

##根据所要获得的数据创建需要GET的URL
def gnerateUrl(departure, date, time):
    return ('http://www.flightstats.com/go/FlightStatus/flightStatusByAirport.do?airport=%28'+departure+'%29M'
    '&airportQueryDate='+date+'&airportQueryTime='+str(time)+'&airlineToFilter='
    '&airportQueryType=0&x=10&y=7')

def noDifference(l1,l2):
    len1=len(l1)
    len2=len(l2)
    if len1!=len2:
##        print "len1=",len1,"len2=",len2
        return False
    for i in range(0,len1):
        if l1[i]!=l2[i]:
##            print "Ddddddddddd!!!!!!!!!!!!!!!==",l1[i],l2[i]
            return False
    return True

##选取机场名称来源
if len(timeValueL)==19:
    with open("E:\Academic\courses\work at VIDI\crawler\IATAdirectory-19.dat") as f:
        IATAlist = [x.split(",")[0] for x in f.readlines()]
else:
    with open("E:\Academic\courses\work at VIDI\crawler\IATAdirectory-7.dat") as f:
        IATAlist = [x.split(",")[0] for x in f.readlines()]

oneDay = datetime.timedelta(1)
process = 0
badprocess = 0

##第一次初始化时间
startDate = datetime.datetime.strptime("2011-05-20", "%Y-%m-%d")
endDate = datetime.datetime.strptime("2011-09-17", "%Y-%m-%d")
date = startDate
ferrout=open('E:\Academic\courses\work at VIDI\data\\errorlog.dat','a')
for airport in IATAlist:
##    ################# TEST ######################
##    airport="BSB"
##    ################# TEST END ######################    ##数据初始化
    airportQueryDate=date.strftime("%Y-%m-%d")
    airportQueryTime="0"
    ##爬取机场 airport 的数据
    fout=open('E:\Academic\courses\work at VIDI\data\\'+airport+'-airport.dat','a')
    while(date<=endDate):
        x=0
        lastFirst=[]
        thisFirst=[]
        lastnum = 0
        ###开始遍历当天内的时间段
        countPeriod = 0 
        while x < len(timeValueL):
            ##爬取本页面航班数据所在的table
            airportQueryTime=timeValueL[x]
            nexturl = gnerateUrl(airport,airportQueryDate,airportQueryTime)
            response = br.open(nexturl)
            html = response.read()
            soup = BeautifulSoup(html)
            table = soup.select(".tableListingTable > tbody > tr")
            if(table==[]): table =  soup.select(".tableListingTable > tr")

            ##本页没有合法的表格
            if len(table)<2:
                ##若本页不含 next 按钮（当天没有划分时间段），则不需要继续遍历时间段
                if "Btn_en_next" not in html:
                    break
                else:
                    x+=1
                    continue            

            ##解析本页的航班数据
            strlist=myParser.parse(table)

            ##若本页不含 next 按钮（当天没有划分时间段），则不需要继续遍历时间段
            if "Btn_en_next" not in html:
                for s in strlist:
                    fout.write(airport+","+airportQueryDate+","+",".join(s).replace("\n", " ")+"\n")

                if len(strlist) != 0:
                    print "Record Num = ",len(table)-2," | ", \
                            airport," ",airportQueryDate," timeperiod=Whole Day",\
                                        "(", process,"/",  len(IATAlist) ,") done"
                break
            
            ##获取本页第一条记录以及本页记录总数
            if len(strlist)==0:
                thisFirst=[]
            else:
                thisFirst=strlist[0]
            thisnum = len(strlist)
            ##若本页第一条和上一页第一条一样并且两页record数量相同，则不dump该记录
            if  thisnum == lastnum and noDifference(thisFirst,lastFirst):
                x+=1
                continue
            else:
                lastFirst=thisFirst
                lastnum=thisnum
            
            for s in strlist:
                fout.write(airport+","+airportQueryDate+","+",".join(s).replace("\n", " ")+"\n")

            if len(strlist) != 0:
                countPeriod += 1
                print "Record Num = ",len(table)-2," | ", \
                        airport," ",airportQueryDate," timeperiod=",airportQueryTime,\
                                    "(", process,"/",  len(IATAlist) ,") done"

            ##若提示没有下一页了，则不再爬下个时间段
            if "Btn_en_next_disabled" in html:
                break
            x+=1
        ##记录有可能遗漏Period的数据
        if countPeriod not in [0, 1, 2, 4]:
            ferrout.write(airport+","+str(countPeriod)+","+airportQueryDate+"\n")
        print airport," in ",airportQueryDate," data finished!!! \n"
        date+=oneDay
        airportQueryDate=date.strftime("%Y-%m-%d")
        airportQueryTime="0"
    process+=1
    print "data of", airport, "done!", process*100.0/len(IATAlist), "% (", process,"/",  len(IATAlist) ,") done" 
    print "----------------------------------------------------------- \n"
    ##该机场数据爬取完毕，重新初始化日期
    
    startDate = datetime.datetime.strptime("2011-05-20", "%Y-%m-%d")
    endDate = datetime.datetime.strptime("2011-09-17", "%Y-%m-%d")
    date = startDate
    fout.close()
ferrout.close()
