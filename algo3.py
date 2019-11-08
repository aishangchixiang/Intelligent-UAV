def quicksort_list(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i[0] <= pivot[0]]
        greater = [i for i in array[1:] if i[0] > pivot[0]]
        return quicksort_list(less) + [pivot] + quicksort_list(greater)
def pointPolygonTest(con,point):
    '''
    进行判断point点是否在某个指定区域内
    :param con: 四个点组成的数组，围成一个平行四边形
    :param point: 测试的坐标点
    :return:True / False
    '''
    if len(con) == 0:
        return False
    con = quicksort_list(con)
    if con[0][1] > con[1][1]:
        LBPoint = [con[0][0],con[0][1]]
        LTPoint = [con[1][0],con[1][1]]
    else:
        LBPoint = [con[1][0], con[1][1]]
        LTPoint = [con[0][0], con[0][1]]
    if con[2][1] > con[3][1]:
        RBPoint = [con[2][0],con[2][1]]
        RTPoint = [con[3][0],con[3][1]]
    else:
        RBPoint = [con[3][0], con[3][1]]
        RTPoint = [con[2][0], con[2][1]]

    if LTPoint[0]-LBPoint[0] == 0:
        if point[0] < LTPoint[0]:
            return False
    else :
        k_l = (LTPoint[1]-LBPoint[1]) / (LTPoint[0]-LBPoint[0])
        b_l = LBPoint[1] - k_l * LBPoint[0]
        if point[1] - k_l * point[0] - b_l > 0 :
            return False
    if RTPoint[0] - RBPoint[0] == 0:
        if point[0] < LTPoint[0]:
            return False
    else :
        k_r = (RTPoint[1]-RBPoint[1]) / (RTPoint[0]-RBPoint[0])
        b_r = RBPoint[1] - k_l * RBPoint[0]
        if point[1] - k_r * point[0] - b_r < 0 :
            return False
    if point[1] < LTPoint[1] or point[1] > LBPoint[1]:
        return False
    return True

if __name__ == "__main__":
    lis = [[303, 84], [347, 325], [643, 90], [687, 331]]
    po = [796,295]
    a = pointPolygonTest(lis,po)
    print(a)
