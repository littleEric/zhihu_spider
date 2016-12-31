from bs4 import BeautifulSoup
import json,re,requests,os
##图片标题下标
temp = 0
##offset值
offset = 0
#图片存放文件夹路径（末尾不带/）
storepath = "/Volumes/100G(HDD)/zhihu_res2"
##储存目录中的文件列表
dir_list = os.listdir(storepath)
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
def get_img_data(src):
    try:
        data = requests.get(src).content
    except requests.exceptions.ConnectionError:
        get_img_data(src)
    except requests.exceptions.ChunkedEncodingError:
        get_img_data(src)
    return data
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
            data = get_img_data(src)
            filename = storepath +"/" + str(offset) + "-" + str(temp) + ".jpg"
            writefile(filename, data)
            temp = temp + 1
            print("==============" + filename + " has been saved=================")
    temp = 0
    offset = offset+10
##过滤非法文件
def rm_other_files(dirlist):
    ##传入dir_list引用
    for i in range(0,len(dirlist)-1):
        if not re.match("\d+-\d+.jpg",dirlist[i]):
            del dirlist[i]
##根据文件名计算出index
def getindex(filename):
    offset = int(filename[:filename.index('-')])
    name_index = int(filename[(filename.index('-')+1):filename.index(".")])
    ##消除offset受到name_index的影响
    return offset*400+name_index
def get_last_offset(list):
    last_file_name = list[len(list)-1]
    offset = int(last_file_name[:last_file_name.index("-")])
    return offset
##程序运行入口
def runpro():
    global dir_list,offset
    rm_other_files(dir_list)
    # print(getindex("450-1.jpg"))
    dir_list.sort(key=lambda dir: getindex(dir))
    offset = get_last_offset(dir_list)
    while 1:
        get_imgs(52570020)
runpro()