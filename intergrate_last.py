import requests
import urllib.parse, urllib.request, base64
import json
import datetime
#import urllib2



class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

def GetCarLicense(PhotoFileName):
    # 调用百度api的准备信息
    access_token = '24.bcb11f91715df4ebfc71fc467d08d8f2.2592000.1566972029.282335-16902078'
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate?access_token=24.551f518d4d0c87902380bf21c8dc36c1.2592000.1567301527.282335-16937187'

    # 此处留下画面的每一帧

    # 二进制方式打开图文件
    f = open(PhotoFileName, 'rb')  # 本地图片

    # 参数image：图像base64编码
    img = base64.b64encode(f.read())

    # 准备图像参数：params通常作为 get请求当中的属性，data作为post请求中携带的属性

    params = {"image": img,
              "multi_detect": True,
              }
    params = urllib.parse.urlencode(params).encode(encoding='UTF8')

    # 此处，在Request请求当中，url,和params并现，意味着将params作为参数追加在url后面
    request = urllib.request.Request(url, params)
    # 追加头部
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    # 得到返回值
    response = urllib.request.urlopen(request)
    # 以json格式读取
    content = response.read()
    # 装载，将json格式的数据，转换成python对象
    content = json.loads(content)

    # print(content.keys())   #只获取第一层的键名
    # print(content['vehicle_info'])
    license=str(content['words_result'][0]['color'])+":"+str(content['words_result'][0]['number'])
    return license

def getPhotoByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str



def PostTimeAndPhotoAndLicense(PhotoFileName,license,IsIllegal):

    #onenet参数
    APIKEY = 'BCnpK4ZTiXdBiD=fT8N4zgk6m8s='
    DEVICEID='536237138'
    SENSORID = 'time'

    #得到当前时间
    curtime = datetime.datetime.now()
    print(curtime)
    #得到车牌信息
    #license=GetCarLicense(PhotoFileName)
    # print(license)
    #时间上传
    url='http://api.heclouds.com/devices/%s/datapoints'%(DEVICEID)
    dict = {"datastreams":[
                            {"id":"time","datapoints":[{"value":curtime}]},
                            {"id": "license", "datapoints": [{"value": license}]},
                            {"id": "isillegal", "datapoints": [{"value": IsIllegal}]}
            ]}
    s = json.dumps(dict,cls=DateEncoder)
    headers = {
                    "api-key":APIKEY,
                    "Connection":"close"
                }
    requests.post(url,headers=headers,data = s)


    #图片上传
    url = "http://api.heclouds.com/bindata"
    headers = {
                "Content-Type": "image/jpg" ,
                "api-key": APIKEY
                }

    querystring1= {"device_id": DEVICEID ,"datastream_id": "photo"}

    # 流式上传
    with open(PhotoFileName, 'rb') as f:
        requests.post(url, params=querystring1, headers=headers, data=f)
    print('违章信息上传成功！')

    #图片二进制，为了微信get到图片
    img_strs = getPhotoByte(PhotoFileName)

    url = 'http://api.heclouds.com/devices/%s/datapoints'%(DEVICEID)
    print("follow is url")
    print(url)
    dict = {"datastreams": [{"id": "photo", "datapoints": [{"value": img_strs}
                                                           ]}]}
    dict['datastreams'][0]['id'] = 'photobinary'
    dict['datastreams'][0]['datapoints'][0]['value'] = img_strs
    s = json.dumps(dict)
    headers = {
        "api-key": APIKEY,
        "Connection": "close"
    }
    requests.post(url, headers=headers, data=s)


def post_info(list):
     for i in list:
          print("违章图片："+i[0])
          print("违章车牌号："+i[1])
          if i[2] == True:
              print("该车辆违章停车！")
          else:
              print("该车辆未违章停车！")
          print("查处时间为：")
          PostTimeAndPhotoAndLicense(i[0],i[1],i[2])