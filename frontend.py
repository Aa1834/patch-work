from tkinter import *
from backend import SmartHome, SmartPlug, SmartTV

#frontend

class smartHomeSystem:
    root = Tk()
    root.geometry('800x500')
    selectValue=StringVar()
    home = SmartHome()
    gridItems=[] #Array of buttons.
    gridLabels=[] #Array of labels.
    
    def __init__(self):
        home = SmartHome()
        self.setUpHome()
        
    def setUpHome(self):
        
        # Creating the buttons: Turn on all, Turn off all and Add Device buttons:
        button1 = Button(self.root, text="Turn on all",command=lambda: self.toggleAllDevices(True))
        button1.grid(row=0,column=1)
        
        button2 = Button(self.root, text="Turn off all" ,command=lambda: self.toggleAllDevices(False))
        button2.grid(row=0,column=2)
        #systems.setUpHome(root)
        buttonAddDev=Button(self.root, text= "Add Device", command=lambda: self.openPopUp(-1))
        buttonAddDev.grid(row=7,column=1)
        self.root.mainloop()
        
    def toggleAllDevices(self, status):
        if status==True:
            self.home.toggleOnAll()
        elif status==False:
            self.home.toggleOffAll()
        
        self.rebuildGrid()
        
            
    def openPopUp(self,deviceNumber):
        deviceName=StringVar()
        deviceOption=IntVar()
        deviceConsumptionRate=IntVar()
        deviceSwitchedOn=BooleanVar()
        
        # edit mode is when deviceNumber=0, however -1 is for insert new device mode (when inserting new device)
        if deviceNumber>-1: 
            device =self.home.devices[deviceNumber]
            deviceName.set(device.deviceName)
            deviceSwitchedOn.set(device.switchedOn)
            if isinstance(device, SmartTV):
                deviceOption.set( device.option)
            elif isinstance(device, SmartPlug):
                deviceConsumptionRate.set(device.consumptionRate)
            
        
        
        top= Toplevel(self.root) #Pop up screen
        top.geometry("350x250")
        top.title("Add Device")
    
    
        self.selectValue.set('Select a device')
        options=['Smart TV', 'Smart Plug']
        #This code below only works when editing device
        if deviceNumber >-1:
            if isinstance(device,SmartTV):
                self.selectValue.set('Smart TV')
            elif isinstance(device, SmartPlug):
                self.selectValue.set('Smart Plug')
        
        optionLabel = Label(top, text="Option:")   
        optionEntry = Entry(top, textvariable=deviceOption)
   
        consLabel = Label(top, text="Consumption Rate:")   
        consEntry = Entry(top, textvariable=deviceConsumptionRate) 
        
        view = OptionMenu(top, self.selectValue, *options,command=lambda x:self.showHideFields(top, optionLabel,optionEntry,consLabel,consEntry))
        view.grid(row=0,column=0, padx=100)
        deviceNameLabel = Label(top, text="Device Name:")
        
        deviceNameLabel = Label(top, text="Device Name:")
        deviceNameLabel.grid(row=1,column=0, padx=100)
        deviceNameEntry = Entry(top, textvariable=deviceName)
        deviceNameEntry.grid(row=2,column=0,padx=100)
        

        saveButton = Button(top, text='Save', command=lambda: self.addADevice(top,deviceNameEntry,consEntry,optionEntry, deviceNumber)) 
        saveButton.grid(row=9,column=0, padx=100)
        
          
    def errorMessage(self, top, message, color):
         resultLabel = Label(top, text=message, foreground=color)
         resultLabel.grid(row=10,column=0, padx=100)
         
    def showHideFields(self,top, optionLabel,optionEntry,consLabel,consEntry):
       
        if self.selectValue.get()=='Smart TV': #Originally the code was making option and consumption rate entry boxes when view was Smart TV or Smart Plug in the pop up window. 
            consLabel.grid_remove()# consLabel.grid_remove and consEntry.grid_remove removes the entry box and label for consumption rate when view = smart TV but keeps options label and entry box for options.
            consEntry.grid_remove()    
            optionLabel.grid(row=7,column=0, padx=100) 
            optionEntry.grid(row=8,column=0, padx=100)
        elif self.selectValue.get()=='Smart Plug': #optionLabel.grid_remove and optionEntry.grid_remove removes the entry box and label for options when view = Smart Plug but keeps the label and entry box for consumption rate.
            consLabel.grid(row=5,column=0, padx=100)
            consEntry.grid(row=6,column=0, padx=100)          
            optionLabel.grid_remove()
            optionEntry.grid_remove()
        #Note: devNumber in addADevice etc is actually deviceNumber but shortened.
    def addADevice(self,top, deviceNameEntry, consumption, options, devNumber): #Adding name of the device in the deviceNameEntry box. Checks if it is Smart TV or Smart Plug. Does error checking for both which have different attributes e.g. Smart TV has options and Smart Plug has consumption rate entry box.
        isDataValid=False
        if self.selectValue.get() in ("Smart TV","Smart Plug"):
            if not deviceNameEntry.get():
                deviceNameEntry.config(text='Device Name is mandatory"',background="red") #Ensures that entry box does not accept null/blank inputs
                raise ValueError('Device Name is mandatory')
        if self.selectValue.get()=='Smart TV':
            if options.get():   #Try except method; caching errors for options e.g. an input for options which isn't an integer.
                try:
                    int(options.get())            
                    options.config(                
                    foreground="green")
                    isDataValid = True
                except ValueError:
                    options.config(                
                    foreground="orange red") #chose orange red since due to visibility
                    isDataValid = False
                    self.errorMessage(top, "Option value must be an integer with value between 1 to 734.", "red")
            else:
                options.config(
                text="Entry is empty",
                background="red4")
                isDataValid = False
                self.errorMessage(top, "This can not be left empty", "red")
        elif self.selectValue.get()=='Smart Plug': #Try except method; caching errors for consumption rate e.g. an input for consumption rate which isn't an integer.        
            try:
                int(consumption.get())
                consumption.config(              
                foreground="green"
            )
                isDataValid = True
                
            except ValueError:
                consumption.config(               
                foreground="orange red"
                        
            )
                isDataValid = False
                self.errorMessage(top, "Consumption value must be an integer.", "red") #Highlights user's input in red since it doesn't meet the required input/condition.
        else:
            consumption.config(            
            foreground="red4")
            isDataValid = False
            self.errorMessage(top, "This can not be left empty", "red") #Highlights user's input in red since it doesn't meet the required input/condition.
                    
                    
        if devNumber<0 and isDataValid == True:  # insert device mode (when entering the device, it will have positional place less than 0 e.g. -1 since the first element will be the first device which will have positional value of 0.)
            if self.selectValue.get()=="Smart TV":        
                tv=SmartTV(deviceNameEntry.get())
                tv.setOptions(int(options.get()))      
                self.home.addDevice(tv)
                
            elif self.selectValue.get()=="Smart Plug":
                plug=SmartPlug(consumption.get(), deviceNameEntry.get())    
                plug.setConsumptionRate(consumption.get())
                self.home.addDevice(plug)        
            self.addDeviceLabel()
            self.showDevicesOnScreen()
            top.destroy() #Once all the values are obtained and displayed, the pop up window is destroyed/closed however whatever was entered remains saved providing all the conditions for each field/entry box has been sastified.
        elif devNumber>-1 and isDataValid == True: # edit device mode
            aDevice=self.home.devices[devNumber]
            if isinstance(aDevice, SmartTV):
                aDevice.setDeviceName(deviceNameEntry.get())
                aDevice.toggleSwitch()
                aDevice.setOptions(int(options.get()))
                self.rebuildGrid() #Removes all rows and button and creates them again.
                    
            elif isinstance(aDevice,SmartPlug):
                aDevice.setDeviceName(deviceNameEntry.get())
                aDevice.setConsumptionRate(consumption.get())
                aDevice.toggleSwitch()
                self.rebuildGrid()
            top.destroy()
        
        
    def toggleDevice(self,devNumber):
        self.home.toggleSwitch(devNumber)
        self.rebuildGrid()
       
        
    def deleteDevice(self,devNumber): #Deletes device from the pop up window; removes/destroys items in the gridItems list. 
        for item in self.gridItems:
            item.destroy()
        
        self.gridItems.clear()   
        self.home.removeDevice(devNumber)    
        self.addDeviceLabel()
        self.showDevicesOnScreen()
        

        
    def rebuildGrid(self): #Removes all buttons and labels and then redraws them. It has 3 steps: Clears the grid from buttons and labels, add device labels, and then add devices again.
        for item in self.gridItems:
            item.destroy()
            
        self.gridItems.clear()        
        self.addDeviceLabel()
        self.showDevicesOnScreen()
    
    def addDeviceLabel(self):
        deviceNumber = 0
        rowIndex=1
        for device in self.home.devices:
            deviceSwitchStatus=""
            if device.switchedOn:
                deviceSwitchStatus="On"
            else:
                deviceSwitchStatus="Off"
                
            if isinstance(device,SmartTV):
                deviceNameLabel = Label(self.root, text="TV: "+deviceSwitchStatus+',' + ' Channel:' + str(device.getOptions()))
                deviceNameLabel.grid(row=2+rowIndex, column=1)
                deviceNumber = deviceNumber + 1
                rowIndex= rowIndex+1
            elif isinstance(device, SmartPlug):
                deviceNameLabel = Label(self.root, text="Plug: "+ deviceSwitchStatus + ',' + 'Consumption Rate:' + str(device.getConsumptionRate()))
                deviceNameLabel.grid(row=2+rowIndex, column=1)
                deviceNumber = deviceNumber + 1
                rowIndex= rowIndex+1
            self.gridItems.append(deviceNameLabel)
        
    def showDevicesOnScreen(self):
        
        deviceNumber = 0  
        rowIndex=1
        for device in self.home.devices:
            
                
            buttonToggle=Button(self.root, text="Toggle", command=lambda deviceNumber=deviceNumber: self.toggleDevice(deviceNumber))
            buttonToggle.grid(row=2+rowIndex, column=4)
            buttonEdit=Button(self.root,text = "Edit", command=lambda deviceNumber=deviceNumber:  self.openPopUp(deviceNumber))
            buttonEdit.grid(row=2+rowIndex, column= 5)
            buttonDelete=Button(self.root,text = "Delete", command=lambda deviceNumber=deviceNumber: self.deleteDevice(deviceNumber))
            buttonDelete.grid(row=2+rowIndex,column=6)
        
            self.gridItems.append(buttonToggle)
            self.gridItems.append(buttonEdit)
            self.gridItems.append(buttonDelete)
            deviceNumber = deviceNumber + 1
            rowIndex= rowIndex+1
        
def main():  
    mysmartHome = smartHomeSystem()
    mysmartHome.setUpHome()
main()
