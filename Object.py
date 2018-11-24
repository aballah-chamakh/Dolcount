import time
import cv2

class Object:

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.tracks = []
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.id
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, new_x, new_y):
        self.tracks.append([self.x,self.y])
        self.x = new_x
        self.y = new_y
    def going_UP(self,mid_start,mid_end):
        if len(self.tracks) >= 2:

            if self.tracks[-1][1] < mid_end and self.tracks[-2][1] > mid_end  :
                return True
            else:
                return False
        else:
            return False
    def going_DOWN(self,mid_start,mid_end):
        if len(self.tracks) >= 2:
            if self.tracks[-1][1] > mid_start and self.tracks[-2][1] < mid_start :

                return True
            else:
                return False
        else:
            return False
