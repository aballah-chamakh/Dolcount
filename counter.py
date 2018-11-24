import numpy as np
import cv2
import Object
import time
import requests

cnt_up   = 0
cnt_down = 0
count_down = 0
obj_id = 1 
cap = cv2.VideoCapture(0)
w = cap.get(3)
h = cap.get(4)

line_up = int(3*(h/5))
line_down   = int(3*(h/5))

up_limit =   int(0.5*(h/5))
down_limit = int(4.5*(h/5))

line_down_color = (255,0,0)
line_up_color = (0,0,255)
pt1 =  [0, line_down];
pt2 =  [w, line_down];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up];
pt4 =  [w, line_up];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit];
pt6 =  [w, up_limit];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit];
pt8 =  [w, down_limit];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

def post_img(image,entered):
    url = 'http://127.0.0.1:8000/api/object/'
    headers = {'Content-Type':'application/json'}
    files = {'img': open(image+'.jpg', 'rb')}

    data = {'name':image,'entered':entered}
    r = requests.post(url,files=files,data=data)



#Background Substractor
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)


kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)


font = cv2.FONT_HERSHEY_SIMPLEX
objects = []


while(cap.isOpened()):


    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
    mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)

    for cnt in contours0:
        rect = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        if area > 5000 and  M['m00'] != 0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,width,heigth = cv2.boundingRect(cnt)

            new = True
            if cy in range(up_limit,down_limit):
                cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
                cv2.rectangle(frame,(x,y),(x+width,y+heigth),(0,255,0),2)
                for obj in objects:
                    if abs(cx-obj.getX()) <= width and abs(cy-obj.getY()) <= heigth :
                        new = False
                        obj.updateCoords(cx,cy)
                        print('updateCoords  x : {x} , y : {y}'.format(x=cx,y=cy))
                        if obj.going_UP(line_down,line_up) == True :
                            cnt_up += 1
                            img = frame   #[y:y+heigth,x:x+width]
                            cv2.imwrite('person_up_'+str(cnt_up)+'.jpg',img)
                            post_img('person_up_'+str(cnt_up),True)
                            print("ID:",obj.getId(),'crossed going up at',time.strftime("%c"))
                        elif obj.going_DOWN(line_down,line_up) == True:
                            cnt_down += 1
                            img = frame  #[y:y+heigth,x:x+width]
                            cv2.imwrite('person_down_'+str(cnt_up)+'.jpg',img)
                            post_img('person_down_'+str(cnt_up),False)
                            print("ID:",obj.getId(),'crossed going down at',time.strftime("%c"))
                        break

                if new == True:
                    new_obj = Object.Object(obj_id,cx,cy)
                    objects.append(new_obj)
                    obj_id += 1
            elif M['m00'] == 0 :
                print('this is equal to 0 ')

    cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
    cv2.putText(frame, str_up ,(10,40),font,1.5,(0,0,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(10,90),font,1.5,(255,0,0),2,cv2.LINE_AA)
    cv2.imshow('Frame',frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
