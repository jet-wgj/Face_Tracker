class PWM_Motor(object):

    def __init__(self, pin,pi= pigpio.pi(), freq = 50, min_width = 1000, max_width=2000):
        self.SPin = pin
        self.Speed= 1500
        self.positionSet = self.Position
        self.Min = min_width
        self.Max = max_width
        self.SpeedChanged = False
        pi.set_PWM_frequency(self.SPin,freq)
        t = threading.Thread(target=motor.updateSpeed, args=(self,))
        t.setDaemon(True)
        t.start()            


    def setSpeed(self, speed):
        if pos < self.Min or pos > self.Max:
            print(pos)
            return
        self.Speed = speed
        self.speedChanged = True
        
 
    def getSpeed(self):
        return self.Speed

    def updateSpeed(self):
        while True:
            if self.SpeedChanged is True:
                self.SpeedChanged = False
                self.pi.set_servo_pulsewidth(self.SPin, int(self.Speed ))
            
