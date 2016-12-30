from bs4 import BeautifulSoup
import json,re,requests
##图片标题下标
temp = 0
##offset值
offset = 0
#图片存放文件夹路径（末尾不带/）
storepath = "/Volumes/100G(HDD)/zhihu_res"
##返回msg的src属性
def getsrc(html):
    srcs = []
    bsObj = BeautifulSoup(html,"lxml")
    #img_tags = bsObj.find_all("img",{"src":re.compile("\.zhimg\.com.*_b")})
    img_tags = bsObj.find_all("img", {"class":"origin_image","src":re.compile("\.zhimg\.com.*_b")})
    for img_tag in img_tags:
        srcs.append(img_tag['src'])
    return srcs
##写文件
def writefile(filename,data):
    file = open(filename,"wb")
    file.write(data)
    file.flush()
    file.close()
def get_imgs(id):
    global offset,temp
    url = "https://www.zhihu.com/question/"+str(id)
    ##ajax提交数据json中的params项
    params = json.dumps({
        'url_token': id,
        'pagesize': 10,
        'offset': offset
    })
    ##ajax提交数据json整合
    data = {
        '_xsrf': '',
        "method":"next",
        "params":params
    }
    headers = { 'Host': "www.zhihu.com",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
                'Content-Length': "93",
                'Referer': url}
    req = requests.post("https://www.zhihu.com/node/QuestionAnswerListV2", data=data, headers=headers)
    ##获取返回值
    msgs = req.json()['msg']
    if msgs == None:
        exit()
    for msg in msgs:
        for src in getsrc(msg):
            data = requests.get(src).content
            filename = storepath +"/" + str(temp) + ".jpg"
            writefile(filename, data)
            temp = temp + 1
            print("==============" + filename + " has been saved=================")
    offset = offset+10
while 1:
    get_imgs(52570020)
