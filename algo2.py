import cv2
import numpy as np
import matplotlib.image as mplimg
import matplotlib.pyplot as plt

def get_linePoint(img_address :str):
    img = mplimg.imread(img_address)  # 读入原图
    hei = len(img)
    wit = len(img[0])
    # 装换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 高斯平滑
    blur_ksize = 9
    blur_gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0, 0)
    # Canny边缘检测
    edges = cv2.Canny(blur_gray, 70, 140)

    # 定义一个眼膜作为兴趣区域
    mask = np.zeros_like(edges)
    ignore_mask_color = 255

    # This time we are defining a four sided polygon to mask
    imshape = img.shape
    vertices = np.array([[(0.3 * wit, hei), (0.3 * wit,0.15 * hei),(0.5 * wit, 0.15 * hei), (wit - 10, 0.5 * hei), (wit - 10, hei)]],
                        dtype=np.int32)
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_edges = cv2.bitwise_and(edges, mask)

    # Hough检测
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 20, minLineLength=10, maxLineGap=10)
    # print(lines)

    # 利用斜率分类

    heng_lines = []  # 横线集
    xie_lines = []  # 斜线集

    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if x1 - x2 == 0:
            xie_lines.append(line)
            continue
        k = (y1 - y2) / (x1 - x2)
        if abs(k) < 0.2:
            heng_lines.append(line)
        elif k > 1:
            xie_lines.append(line)

    # 筛选出最低的横线
    heng_max_lines = []
    max_y = 0
    for line in heng_lines:
        for x1, y1, x2, y2 in line:
            if y1 > max_y:
                max_y = y1
            elif y2 > max_y:
                max_y = y2
    for line in heng_lines:
        for x1, y1, x2, y2 in line:
            if (y1 <= max_y and y1 >= max_y - 15) and (y2 <= max_y and y2 >= max_y - 15):
                heng_max_lines.append(line)
    if len(heng_max_lines) < 2 :
        return []
    # 求出最大横线长度
    heng_left = [10000, 10000]
    heng_right = [0, 0]
    for line in heng_max_lines:
        for x1, y1, x2, y2 in line:
            if x1 < heng_left[0]:
                heng_left[0] = x1
                heng_left[1] = y1
            if x1 > heng_right[0]:
                heng_right[0] = x1
                heng_right[1] = y1
            if x2 < heng_left[0]:
                heng_left[0] = x2
                heng_left[1] = y2
            if x2 > heng_right[0]:
                heng_right[0] = x2
                heng_right[1] = y2

    LBPoint = heng_left
    RBPoint = heng_right

    # 筛选出Y最小的斜线点
    min_y = [10000, 10000]
    for line in xie_lines:
        for x1, y1, x2, y2 in line:
            if y1 < min_y[1]:
                min_y[0] = x1
                min_y[1] = y1
            if y2 < min_y[1]:
                min_y[0] = x2
                min_y[1] = y2
    LTPoint = min_y
    RTPoint = [min_y[0] + (RBPoint[0] - LBPoint[0]), min_y[1] + (RBPoint[1] - LBPoint[1])]
    con = [LTPoint, LBPoint, RTPoint, RBPoint]
    return con

if __name__ == "__main__":
    add = "try4.jpg"
    print(get_linePoint(add))

