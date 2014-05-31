from bs4 import BeautifulSoup, NavigableString
import re
import string
def parse(table):
    result=[]
    for i in range(2,len(table)):
        ##每一行记录
        record=filter(lambda a: a != '\n', table[i].contents)
        ##每一行记录处理后的的列表形式
        rlist=[]
        for j in range(0,10):
            td = record[j]
            if j==0:
                s=string.split(td.text,None,1)
                rlist.append(s[0].strip())
                rlist.append(s[1].strip())
##                print s[0].strip()
##                print s[1].strip()
            elif j==2:
                starObj=td.find("a")
                if(starObj is not None):
                    s=td.find("a").find("div")['style']
                    l=map(int, re.findall(r'\d+', s))
                    rlist.append(str(l[1]/100.0))
##                    print str(l[1]/100.0)
                else:
                    rlist.append("")
            elif j==7:
                s=[]
                if("En Route" in td.text):
                    s.append("En Route")
                    s.append(td.text.replace(s[0],"").strip())
                else:
                    s=string.split(td.text,None,1)
                rlist.append(s[0].strip()+";"+(len(s)>1 and s[1].strip() or ""))
##                print s[0].strip()+";"+(len(s)>1 and s[1].strip() or "")
            elif j!=9:
                rlist.append(td.text.strip())
##                print(td.text.strip())
##        print("---------------------------------")
        result.append(rlist)
        
    return result
