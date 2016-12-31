import os,re
path = "/Volumes/100G(HDD)/zhihu_res2"
dir_list = os.listdir(path)
##过滤非法文件
def rm_other_files(dirlist):
    ##传入dir_list引用
    for i in range(0,len(dirlist)-1):
        if not re.match("\d+-\d+.jpg",dirlist[i]):
            del dirlist[i]
def getindex(filename):
    offset = int(filename[:filename.index('-')])
    name_index = int(filename[(filename.index('-')+1):filename.index(".")])
    ##消除offset受到name_index的影响
    return offset*400+name_index
rm_other_files(dir_list)
#print(getindex("450-1.jpg"))
dir_list.sort(key = lambda dir: getindex(dir))
print(dir_list)
