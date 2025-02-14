from jinja2 import Environment, FileSystemLoader
import time
import requests
from tool import gen_sign
from urllib.parse import unquote

pageNum = 1
pageSize = 10
currentPage = 1
posCount = 0
location = '成都'
company = []
major = '物流管理'
# 是否搜索不限专业岗位
switchBtnVal = 'true'
# education=%E4%B8%8D%E9%99%90 不限学历
education = '%E4%B8%8D%E9%99%90'
Authorization = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3N1ZXIiLCJzdWIiOiJzdWJqZWN0IiwiYXVkIjoiYXVkaWVuY2UiLCJpYXQiOjE3Mzk1Mzc5NTcsIm5iZiI6MTczOTUzNzk1NywiZXhwIjoxNzcxMDczOTU3LCJkYXRhIjpbeyJ1c2VyX2lkIjoiMTg1NDciLCJ1c2VybmFtZSI6IjE3ODIzMjYzMzA2IiwibW9iaWxlIjoiMTc4MjMyNjMzMDYiLCJjcmVhdGVfdGltZSI6IjIwMjUtMDItMTQgMjA6NTk6MTcifV19.X9Z2HSEBgtD8tbEm1512ypH50j-Y3AMXD6QWGuf5Y0c'


p_n = 0
while True:
    url = f'https://qzb.cntjhr.com/newapi/api/news/position/list?pageNum={pageNum}&pageSize={pageSize}&currentPage={currentPage}&posCount={posCount}&major={major}&education={education}&switchBtnVal={switchBtnVal}&time_box=%E8%BF%9B%E8%A1%8C%E4%B8%AD&location={location}&nw=&gc=&xxlx=&position=&name=&ischeckLogin=1'
    timestamp = int(time.time())
    headers = {
        'Host': 'qzb.cntjhr.com',
        'Connection': 'keep-alive',
        'timestamp': str(timestamp),
        'xweb_xhr': '1',
        'Authorization': Authorization,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275',
        'sign':  gen_sign(unquote(url) ,timestamp),
        'appkey': 'ZBE36LCpWHtL',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx8df0c890844bdc43/18/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    time.sleep(1)
    res = requests.get(url, headers=headers, verify=False)
    print(res.text)
    data = res.json()['data']
    print(data)
    if data['list'] == []:
        break
    for e in data['list']:
        p_n += len(e['arr'])
    company += data['list']
    posCount = int(data['posCount'])
    pageNum += 1
print(company)
data = {
    'title': location,
    'companys': enumerate(company),
    'c_n': len(company),
    'p_n': p_n
}
# 设置模板文件夹路径
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
if switchBtnVal == 'true':
    name = 'main_' + location + '-' + major +  '_' + '包括不限专业' + '.html'
else:
    name = 'main_' + location + '-' + major + '.html'
# 加载模板
template = env.get_template('template.html')

# 渲染模板
html_output = template.render(data)

# 或者保存到文件
with open('docs' + '/' + name, 'w', encoding='utf8') as f:
    f.write(html_output)