import random
import json


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.nNeighbors = []
        self.sNeighbors = []
        self.eNeighbors = []
        self.wNeighbors = []


class BigMap:
    def __init__(self, W, H, minSize, maxSize, minRooms):
        self.W = W
        self.H = H
        self.minSize = minSize
        self.maxSize = maxSize
        self.RoomList = [Rectangle(0, 0, self.W, self.H)]
        self.minRooms = minRooms
        self.worldArray = [[' ' for i in range(self.W)] for j in range(self.H)]

    def buildWorld(self):
        for index, rect in enumerate(self.RoomList):
            shouldSplit = bool(random.getrandbits(1))
            if rect.w <= 2*self.minSize or rect.h <= 2*self.minSize:
                continue
            if rect.w >= self.maxSize and rect.h >= self.maxSize or shouldSplit == 1:
                # split the rect into four rects
                # determine the split locations vertically and horizontally
                hSplit = self.minSize + \
                    random.randrange(0, rect.h - (2*self.minSize))
                wSplit = self.minSize + \
                    random.randrange(0, rect.w - (2*self.minSize))
                # add the rects to the end of the list
                rect1 = Rectangle(rect.x, rect.y, wSplit, hSplit)
                self.RoomList.append(rect1)
                rect2 = Rectangle(rect.x + wSplit, rect.y,
                                rect.w - wSplit, hSplit)
                self.RoomList.append(rect2)

                rect3 = Rectangle(rect.x, rect.y + hSplit,
                                wSplit, rect.h-hSplit)
                self.RoomList.append(rect3)
                rect4 = Rectangle(rect.x + wSplit, rect.y + hSplit,
                                rect.w - wSplit, rect.h-hSplit)
                self.RoomList.append(rect4)
                # update neighbors
                rect1.eNeighbors.append(rect2)
                rect1.sNeighbors.append(rect3)
                rect2.wNeighbors.append(rect1)
                rect2.sNeighbors.append(rect4)
                rect3.nNeighbors.append(rect1)
                rect3.eNeighbors.append(rect4)
                rect4.wNeighbors.append(rect3)
                rect4.nNeighbors.append(rect2)
                # remove original rect from the list
                del self.RoomList[index]
        if len(self.RoomList) < self.minRooms:
            self.buildWorld()

        for room in self.RoomList:
            for i in range(room.x, room.x + room.w):
                self.worldArray[i][room.y] = '#'
                self.worldArray[i][room.y+room.h - 1] = "#"
            for j in range(room.y, room.y + room.h):
                self.worldArray[room.x][j] = "#"
                self.worldArray[room.x + room.w - 1][j] = "#"

        return self.RoomList
