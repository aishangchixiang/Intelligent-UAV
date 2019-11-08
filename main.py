from algo3 import pointPolygonTest
from algo2 import get_linePoint
from facepp_lisense import get_Carcard

import time


def one_picture(address):
    # 得到停车线的坐标
    con = get_linePoint(address)

    # 得到汽牌的坐标
    list_car = get_Carcard(address)

    # 这是疑似违章的存储
    bad_car = []

    # 进行检测是否停车标准
    if len(list_car) != 0:
        for i in list_car:
            if pointPolygonTest(con, [i[1], i[2]]) == False:
                bad_car.append(i)
    return bad_car

def two_picture(address1:str,address2:str):
    bad_car1 = one_picture(address1)
    bad_car2 = one_picture(address2)
    last_car = []
    for i in bad_car2:
        for j in bad_car1:
            if i[0] == j[0] :
                juli = ((i[1]-j[1]) ** 2 + (i[2]-j[2]) ** 2) ** 0.5
                if juli < 30 :
                    last_car.append([address2,i[0],True])
                break
    return  last_car
def two_picture_plus(address1,address2):
    last_car = two_picture(address1,address2)
    if len(last_car) == 0:
        last_car = two_picture(address1, address2)
    car_list1 = get_Carcard(address2)
    if len(car_list1) == 0:
        car_list1 = get_Carcard(address2)
    car_list = []

    if len(car_list1) == 0:
        return []
    for i in car_list1:
        car_list.append([address2,i[0],False])
    for i in car_list:
        for j in last_car:
            if i[1] == j[1]:
                i[2] = True
                break
    return car_list
if __name__ == "__main__":
    t1 = time.time()
    address1 = "pic0.jpg"
    address2 = "pic2.jpg"
    print(two_picture_plus(address1,address2))
    t2 = time.time()
    print(t2 - t1)

