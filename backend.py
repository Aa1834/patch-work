class SmartPlug:
    def __init__(self, consumptionRate, deviceName):
        self.consumptionRate = consumptionRate
        self.switchedOn = False
        self.deviceName = deviceName
    
    def setDeviceName(self, devName): #devName = for setting the device name when using the mutator method so we have something as its parameter in the setDeviceName method when we call it.
        self.deviceName = devName

    def getDeviceName(self):
        return self.deviceName
        
    def toggleSwitch(self):
        self.switchedOn = not(self.switchedOn)
        return self.switchedOn 

    def getSwitchOn(self):
        return self.switchedOn

    def getConsumptionRate(self):
        return self.consumptionRate

    def setConsumptionRate(self, rate):
        self.consumptionRate = rate

    def __str__(self):
        output = f"Consumption rate is: {self.consumptionRate}"
        return output
    

def testSmartPlug():
    #consumptionRate = int(input("Enter a value for consumption rate: "))
    plug = SmartPlug(45,"Plug")

    #print(plug.getSwitchOn())
    plug.toggleSwitch()
    print(plug.getSwitchOn())
    print(plug.getConsumptionRate())
    plug.setConsumptionRate(120)
    print(plug.getConsumptionRate())
    print(plug)




class SmartTV:  #custom device
    def __init__(self,deviceName):
        self.switchedOn = False
        self.option = 1
        self.deviceName = deviceName
        
    def toggleSwitch(self):
        self.switchedOn = not(self.switchedOn) 
        return self.switchedOn
    
    def getSwitchedOn(self):
        return self.switchedOn
    
    def getOptions(self):
        return self.option
    
    def getDeviceName(self):
        return self.deviceName
    
    def setDeviceName(self,devName):
        self.deviceName = devName
    
    def setOptions(self,opt): #if parameter opt is greater than 734 or less than 1 then it will result in the options to have default value of 1. Otherwise, it is whatever the user enters via the setOptions method.
        if opt > 734 or opt < 1:
            self.option = 1
        else:
            self.option = opt   
    
    def __str__(self):
        output = f"Is switch on?: {self.switchedOn}\n Current value of option: {self.option}" #For the switch being on question, True will mean the switch is on and False will mean the switch is off.
        return output

def testSmartTV():
    tv = SmartTV('TV')
    print(tv.getSwitchedOn())
    print(tv.toggleSwitch())
    print(tv.getSwitchedOn())
    print(tv.getOptions())
    tv.setOptions(100)
    print(tv.getOptions())
    print(tv)



class SmartHome():
    
    def __init__(self):
        self.devices = []
        self.switchedOn = False
        
        
    
    def addDevice(self,device):
        if isinstance(device,(SmartPlug,SmartTV)):
            self.devices.append(device)
        else:
            print("Invalid device type. Please add a SmartPlug or SmartTV.")
            
            
    
    def removeDevice(self,deviceNumber):
        #for device in self.devices:
        #   if device == :
        #       self.devices.remove(device)
        #      return
        ##  print("Device not found.")
        try:
            del self.devices[deviceNumber]
        except ValueError:
            print("Array element not found")    
       
            
            
    def getDeviceAt(self,deviceNumber): 
        try:
            return self.devices[deviceNumber]
        
        except ValueError:
            print("Device index is not found in the array")
            return None 
        
        
    def getDevice(self):
        return self.devices
    
    def toggleSwitch(self,devicePosition):
        
       try:
           self.devices[devicePosition].switchedOn = not(self.devices[devicePosition].switchedOn )
       except ValueError:
           print("Value not found")
        
           
    def getToggle(self,devicePosition):
        return self.devices[devicePosition].switchedOn
                      
            
        
    
    def toggleOnAll(self):
        for device in self.devices:         
            device.switchedOn = True
        
    def toggleOffAll(self):
        for device in self.devices:
            device.switchedOn = False
            

    
    def __str__(self):
        output = f"Smart home has following devices:"
        if len(self.devices)>0:
            for device in self.devices:
                output += f"\n- {device.deviceName}"
        else:
            output += f"\n- None"
        return output
            
def testSmartHome():
    home = SmartHome()
    firstPlug = SmartPlug(45,"first plug")
    secondPlug = SmartPlug(45,"second plug")
    tv=SmartTV("Samsung")
    firstPlug.toggleSwitch()
    firstPlug.setConsumptionRate(150)
    secondPlug.setConsumptionRate(25)
    tv.setOptions(39)
    home.addDevice(firstPlug)
    home.addDevice(secondPlug)
    home.addDevice(tv)
    secondPlug.toggleSwitch()
    print(home)
    home.toggleOnAll() #Turns on all devices in smartHome (sets status to True for all devices in smartHome)
    print(home)
    home.removeDevice(0)
    print(home)
        
