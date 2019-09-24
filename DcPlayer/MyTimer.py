import time 

class MyTimer():
    
    def __init__(self):
        self.isActive = False

    def start(self,waitTime):
        self.isActive = True
        self.startTime = time.time()
        self.waitTime = waitTime/1000.0

    def isTimeOut(self):
        self.nowTime = time.time()
        if self.nowTime - self.startTime >= self.waitTime:
            return True
        else :
            return False
    
    def waitTimeOut(self):
        while self.isTimeOut() == False & self.isActive == True:
            time.sleep(0.01)
    
    def end(self):
        self.isActive = False

    def resetWaitTime(self,waitTime):
        self.waitTime = waitTime/1000.0
    
    
