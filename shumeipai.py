import cv2
from main import two_picture_plus
from intergrate_last import post_info

cap = cv2.VideoCapture("video1.mp4")
cap.set(3,1280)
cap.set(4,720)
num = 0
n =0
while (1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    num = num + 1
    if num % 50 == 0:    #每一帧停留50ms，每50*50ms=2.5s  执行一次接下来的程序
        print('画面第'+str(n+1)+'帧截取成功')
        cv2.imwrite('pic' + str(n) + '.jpg', frame)
        n += 1

    # print('输出成功')
    try:
        cv2.imshow("capture", frame)
    except cv2.error:
        break
    if cv2.waitKey(6) & 0xFF == ord('q'):   #画面等待停留50ms，正常速度
        break
    # 释放摄像头及其他资源
cap.release()
cv2.destroyAllWindows()

list = two_picture_plus("pic0.jpg","pic2.jpg")

post_info(list)
