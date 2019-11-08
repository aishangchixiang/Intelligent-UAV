import requests
from json import JSONDecoder
import matplotlib.image as mplimg

def get_Carcard(addess):
    http_url = "https://api-cn.faceplusplus.com/imagepp/v1/licenseplate"
    # 你要调用API的URL

    key = "sAJP_TJEancnYFWOjOnJp1xbK4TRzsYx"
    secret = "-Z4Nj72UKGEtxhZba6lWfiwCSQusbdWc"
    # face++提供的一对密钥

    filepath1 = addess
    # 图片文件的绝对路径
    tu = mplimg.imread(filepath1)  # 读入原图
    hei = len(tu)

    data = {"api_key": key, "api_secret": secret, "return_attributes": "gender,age,smiling,beauty"}
    # 必需的参数，注意key、secret、"gender,age,smiling,beauty"均为字符串，与官网要求一致

    files = {"image_file": open(filepath1, "rb")}
    '''以二进制读入图像，这个字典中open(filepath1, "rb")返回的是二进制的图像文件，所以"image_file"是二进制文件，符合官网要求'''

    response = requests.post(http_url, data=data, files=files)
    # POTS上传

    req_con = response.content.decode('utf-8')
    # response的内容是JSON格式

    req_dict = JSONDecoder().decode(req_con)
    # 对其解码成字典格式
    try:
        if len(req_dict['results']) == 0:
            return []
        else:
            cards = []
            for i in req_dict['results']:
                if (i['bound']['right_top']['y'] + i['bound']['left_top']['y']) // 2 > 0.15 * hei:
                    cards.append(
                        [i['license_plate_number'], (i['bound']['right_top']['x'] + i['bound']['left_top']['x']) // 2,
                         (i['bound']['right_top']['y'] + i['bound']['left_top']['y']) // 2])
        return cards
    except KeyError:
        return []


if __name__ == "__main__":
    print(get_Carcard("pic6.jpg"))









