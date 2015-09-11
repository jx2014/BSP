#Author:  Jeremy Xue
#Date:    8/6/2015
import os
import sys
import re
import csv
from collections import OrderedDict

def FUNC_NAME(some_func):
    def Inner(*args, **kwargs):
        print "\n\n...Function Invoked: %s ..." % some_func.func_name            
        return some_func(*args)
    return Inner

class BSP():
    def __init__(self, log):
        # i.e. log = c:\temp\abc.txt
        if os.path.exists(log) == False:                
            self.__exit__('path does not exist: %s' % log)
        self.logFullPath = log
        self.logDirectory = os.path.dirname(log) # c:\temp
        self.logName = os.path.basename(log) # abc.txt
        self.logfName, self.logExt = os.path.splitext(self.logName) # abc and .txt
        self.outputName = self.logfName + '_output.csv' # abc_output.csv"
        self.outputFullPath = self.logDirectory+ '\\' + self.outputName # c:\temp\abc_output.txt
        self.fieldNames = ["Entry", "Th", "UUT", "IPv6", "MAC ID",
                           "Time Stamp",
                           "Last Battery Test",
                           "Stamp", 
                           "Pre-Test Charger Temp",
                           "Pre-Test Batt Temp",                                                                                               
                           "Pre-Test Batt Volt",                                                                                                
                           "Post-Test Charger Temp",                                                                               
                           "Post-Test Batt Temp",                                                                                               
                           "Post-Test Batt Volt",                                                                                                
                           "Power Mode",                                              
                           "Present Charger Temp",                                                                                               
                           "Present Batt Temp",                                                                                               
                           "Present Batt Volt",                                                                                               
                           "Present Batt Current",                                                                                              
                           "Time since last batt ev",
                           "Battery Capacity",
                           "Battery Capacity Status Change",
                           "Battery Algorithm",
                           "Coulomb Algorithm Level",
                           "Current Scaled Coulomb",
                           "Current Float Voltage",
                           ]
        self.uniqueLastBattTest = ''
        self.uniqueLastBatCap = ''

        
        #search started flag
        self.ssed = False
    
    def __exit__(self, msg=''):
        sys.exit("\n\n %s \n... Good bye ...\n" % msg)
        
    @FUNC_NAME
    def FileNames(self):        
        print "{0:.<25}: {1:<100}".format("log file directory", self.logDirectory)
        print "{0:.<25}: {1:<100}".format("log file name", self.logName)
        #print "{0:.<25}: {1:<100}".format("log file name", self.logfName)
        #print "{0:.<25}: {1:<100}".format("log extension", self.logExt)
        print "{0:.<25}: {1:<100}".format("output file name", self.outputName)
        print "{0:.<25}: {1:<100}".format("output file full path", self.outputFullPath)
    
    
    @FUNC_NAME
    def OutputFunc(self, log):
        '''
            nLine 1: REL_B:  fe80::213:50ff:fe11:e000
            nLine 2: 288
            nLine 3: Thu Aug  6 14:45:56 PDT 2015
            nLine 4: *******      Battery Status      *******
            nLine 5: Last Battery Test       :  Wed Aug  5 14:55:42 2015
            nLine 6: ******* Status before load test  *******
            nLine 7: Charger Temperature     :  31.00 C.
            nLine 8: Battery Temperature     :  23.36 C.
            nLine 9: Battery Voltage         :  9.55 V.
            nLine 10: *******  Status after load test  *******
            nLine 11: Charger Temperature     :  31.00 C.
            nLine 12: Battery Temperature     :  22.82 C.
            nLine 13: Battery Voltage         :  9.55 V.
            nLine 14: *******      Present State       *******
            nLine 15: Power Mode              :  Battery is OFF; device is operating on external power.
            nLine 16: Charger Temperature     :  31.37 C.
            nLine 17: Battery Temperature     :  25.87 C.
            nLine 18: Battery Voltage         :  12.39 V.
            nLine 19: Battery Charge Current  :  400.18 mA.
            nLine 20: Time since last batt ev :  172321 seconds.
            
            nLine 1: REL_B:  fe80::213:50ff:fe11:e000
            nLine 2: 288
            nLine 3: Thu Aug  6 14:45:56 PDT 2015
            nLine 4: *******      Battery Status      *******
            nLine 5: Last Battery Test       :  Wed Aug  5 14:55:42 2015
            nLine 6: ******* Status before load test  *******
            nLine 7: Charger Temperature     :  31.00 C.
            nLine 8: No Battery Attached            
            nLine 9: *******  Status after load test  *******
            nLine 10: Charger Temperature     :  31.00 C.
            nLine 11: No Battery Attached            
            nLine 12: *******      Present State       *******
            nLine 13: Power Mode              :  Battery is NOT attached; device is operating on external power.
            nLine 14: Charger Temperature     :  31.37 C.            
            nLine 15: Battery Voltage         :  0.00 V.
            nLine 16: Battery Charge Current  :  0.00 mA.
            nLine 17: Time since last batt ev :  172321 seconds.
            
            self.fieldNames = ["Th", "UUT", "IPv6", "MAC ID", 
                           "Time Stamp",
                           "Last Battery Test",
                           "Stamp", 
                           "Pre-Test Charger Temp",
                           "Pre-Test Batt Temp",                                                                                               
                           "Pre-Test Batt Volt",                                                                                                
                           "Post-Test Charger Temp",                                                                               
                           "Post-Test Batt Temp",                                                                                               
                           "Post-Test Batt Volt",                                                                                                
                           "Power Mode",                                              
                           "Present Charger Temp",                                                                                               
                           "Present Batt Temp",                                                                                               
                           "Present Batt Volt",                                                                                               
                           "Present Batt Current",                                                                                              
                           "Time since last batt ev"
        '''
        with open(log, 'r') as dataFile:
            #for testing
            with open(self.outputFullPath, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldNames, lineterminator='\n', )
                writer.writeheader()                
                line = dataFile.next()
                t = 0
                while True:                                  
                    if self.GetMACID(line) is not None:
                        t = t + 1
                        HR = t / 6
                        UUT, IPV6, MAC = self.GetMACID(line)
                        row = OrderedDict({"Th": HR, "UUT": UUT, "IPv6":IPV6, "MAC ID": MAC})                        
                        updateLastBatTest = False
                        
                        while line != '\n':                        
                            line = dataFile.next()
                            
                            if line in ["Erroneous request\n"]:
                                continue
                            
                            Entry = self.GetEntry(line)
                            if Entry is not None:
                                row.update({"Entry":Entry})
                                line = dataFile.next()                            
                            
                            TimeStamp = self.GetTimeStamp(line)
                            if TimeStamp is not None:
                                row.update({"Time Stamp":TimeStamp})
                                line = dataFile.next()
                            
                            if "Battery Status" in line:
                                line = dataFile.next()
                                LastBatteryTest, LBTUnique = self.GetLastBatTest(line)
                                if LBTUnique != self.uniqueLastBattTest:
                                    self.uniqueLastBattTest = LBTUnique                                    
                                    row.update({"Stamp":"1"})
                                else:                                    
                                    row.update({"Stamp":""})
                                row.update({"Last Battery Test":LastBatteryTest})                                                                                            
                                line = dataFile.next()
                            
                            if "Status before load test" in line:
                                line = dataFile.next()
                                if "Charger Temperature" in line:
                                    data = self.GetData(line)
                                    row.update({"Pre-Test Charger Temp":data})
                                    line = dataFile.next()
                                if "Battery Temperature" in line:
                                    data = self.GetData(line)
                                    row.update({"Pre-Test Batt Temp":data})
                                    line = dataFile.next()
                                if "Battery Voltage" in line:
                                    data = self.GetData(line)
                                    row.update({"Pre-Test Batt Volt":data})
                                    line = dataFile.next()
                                if "No Battery Attached" in line:                                    
                                    row.update({"Pre-Test Batt Temp":"0"})
                                    row.update({"Pre-Test Batt Volt":"0"})
                                    line = dataFile.next()
                            
                            if "Status after load test" in line:
                                line = dataFile.next()
                                if "Charger Temperature" in line:
                                    data = self.GetData(line)
                                    row.update({"Post-Test Charger Temp":data})
                                    line = dataFile.next()
                                if "Battery Temperature" in line:
                                    data = self.GetData(line)
                                    row.update({"Post-Test Batt Temp":data})
                                    line = dataFile.next()
                                if "Battery Voltage" in line:
                                    data = self.GetData(line)
                                    row.update({"Post-Test Batt Volt":data})
                                    line = dataFile.next()
                                if "No Battery Attached" in line:                                    
                                    row.update({"Post-Test Batt Temp":"0"})
                                    row.update({"Post-Test Batt Volt":"0"})
                                    line = dataFile.next()
                            
                            if "Present State" in line:
                                line = dataFile.next()
                                if "Power Mode" in line:
                                    pwrMode = self.GetPwrMode(line)
                                    row.update({"Power Mode":pwrMode})
                                    line = dataFile.next()                                    
                                if "Charger Temperature" in line:
                                    data = self.GetData(line)
                                    row.update({"Present Charger Temp":data})
                                    line = dataFile.next()
                                if "Battery Temperature" in line:
                                    data = self.GetData(line)
                                    row.update({"Present Batt Temp":data})
                                    line = dataFile.next()
                                if "Battery Voltage" in line:
                                    data = self.GetData(line)
                                    row.update({"Present Batt Volt":data})
                                    line = dataFile.next()
                                if "Battery Charge Current" in line:
                                    data = self.GetData(line)
                                    row.update({"Present Batt Current":data})
                                    line = dataFile.next()
                                if "Time since last batt ev" in line:
                                    lastBattEv = self.GetBattEvent(line)
                                    row.update({"Time since last batt ev":lastBattEv})
                            
                            if "Capacity" in line:
                                line = dataFile.next()
                                if "Battery Capacity" in line:
                                    result = self.GetText(line, text="Battery Capacity        :  ")                                    
                                    row.update({"Battery Capacity":result})
                                    
                                    if result != self.uniqueLastBatCap:
                                        self.uniqueLastBatCap = result                                    
                                        row.update({"Battery Capacity Status Change":"1"})
                                    else:                                    
                                        row.update({"Battery Capacity Status Change":""})
                                        
                                    row.update({"Last Battery Test":LastBatteryTest})   
                                    line = dataFile.next()
                                if "Battery Algorithm" in line:
                                    result = self.GetText(line, text="Battery Algorithm       :  ")
                                    row.update({"Battery Algorithm":result})
                                    line = dataFile.next()
                                if "Coulomb Algorithm Level" in line:
                                    data = self.GetData(line)
                                    row.update({"Coulomb Algorithm Level":data})
                                    line = dataFile.next()
                                if "Current Scaled Coulomb" in line:
                                    data = self.GetData(line)
                                    row.update({"Current Scaled Coulomb":data})
                                    line = dataFile.next()
                                if "Current Float Voltage" in line:
                                    data = self.GetData(line)
                                    row.update({"Current Float Voltage":data})
                                    line = dataFile.next()
                                    
                        print row
                        writer.writerow(row)                        
                                                                
                    else:
                        try:
                            line = dataFile.next()
                            print 
                        except StopIteration:
                            print "...End of file..."
                            return False
    
    #Not in use
    @FUNC_NAME
    def OutputFunc_2(self, log):
        '''
            nLine 1: REL_B:  fe80::213:50ff:fe11:e000
            nLine 2: 288
            nLine 3: Thu Aug  6 14:45:56 PDT 2015
            nLine 4: *******      Battery Status      *******
            nLine 5: Last Battery Test       :  Wed Aug  5 14:55:42 2015
            nLine 6: ******* Status before load test  *******
            nLine 7: Charger Temperature     :  31.00 C.
            nLine 8: Battery Temperature     :  23.36 C.
            nLine 9: Battery Voltage         :  9.55 V.
            nLine 10: *******  Status after load test  *******
            nLine 11: Charger Temperature     :  31.00 C.
            nLine 12: Battery Temperature     :  22.82 C.
            nLine 13: Battery Voltage         :  9.55 V.
            nLine 14: *******      Present State       *******
            nLine 15: Power Mode              :  Battery is OFF; device is operating on external power.
            nLine 16: Charger Temperature     :  31.37 C.
            nLine 17: Battery Temperature     :  25.87 C.
            nLine 18: Battery Voltage         :  12.39 V.
            nLine 19: Battery Charge Current  :  400.18 mA.
            nLine 20: Time since last batt ev :  172321 seconds.
            
            nLine 1: REL_B:  fe80::213:50ff:fe11:e000
            nLine 2: 288
            nLine 3: Thu Aug  6 14:45:56 PDT 2015
            nLine 4: *******      Battery Status      *******
            nLine 5: Last Battery Test       :  Wed Aug  5 14:55:42 2015
            nLine 6: ******* Status before load test  *******
            nLine 7: Charger Temperature     :  31.00 C.
            nLine 8: No Battery Attached            
            nLine 9: *******  Status after load test  *******
            nLine 10: Charger Temperature     :  31.00 C.
            nLine 11: No Battery Attached            
            nLine 12: *******      Present State       *******
            nLine 13: Power Mode              :  Battery is NOT attached; device is operating on external power.
            nLine 14: Charger Temperature     :  31.37 C.            
            nLine 15: Battery Voltage         :  0.00 V.
            nLine 16: Battery Charge Current  :  0.00 mA.
            nLine 17: Time since last batt ev :  172321 seconds.
        '''
        with open(log, 'r') as dataFile:
            #for testing
            with open(self.outputFullPath, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldNames, lineterminator='\n', )
                writer.writeheader()                
                line = dataFile.next()
                t = 0
                while True:                                  
                    if self.GetMACID(line) is not None:
                        t = t + 1
                        HR = t / 6
                        UUT, IPV6, MAC = self.GetMACID(line)
                        row = OrderedDict({"Th": HR, "UUT": UUT, "IPv6":IPV6, "MAC ID": MAC})                        
                        updateLastBatTest = False
                        nLine = 1
                        for field in self.fieldNames[4:]:
                            line = dataFile.next()
                            if line in ["Erroneous request\n", "", " ", "\n"]:
                                break
                            if line in ["No Battery Attached\n"]:
                                nLine = nLine + 1
                            if not line:
                                break
                            nLine = nLine + 1
                                               
                            if nLine in [2, 4, 10, 14]:
                                nLine = nLine + 1
                                line = dataFile.next()
                            
                            if nLine in [7,8,9,11,12,13,16,17,18,19]:
                                data = self.GetData(line)
                                row.update({field:data})
                                continue
                            
                            if nLine == 20:
                                lastBattEv = self.GetBattEvent(line)
                                row.update({field:lastBattEv})
                                continue

                            if nLine == 15:
                                pwrMode = self.GetPwrMode(line)
                                row.update({field:pwrMode})
                                continue
                            
                            if nLine == 6:
                                if updateLastBatTest == True:
                                    row.update({field:"1"})
                                else:
                                    row.update({field:""})                                                                    
                                continue
                            
                            if nLine == 5:                                
                                LastBatteryTest, LBTUnique = self.GetLastBatTest(line)
                                if LBTUnique != self.uniqueLastBattTest:
                                    self.uniqueLastBattTest = LBTUnique
                                    updateLastBatTest = True
                                else:
                                    updateLastBatTest = False
                                row.update({field:LastBatteryTest})
                                continue
                            
                            if nLine == 3:
                                TimeStamp = self.GetTimeStamp(line)
                                row.update({field:TimeStamp})
                                continue                                                                                                
                            
                        print row
                        writer.writerow(row)                        
                                                                
                    else:
                        try:
                            line = dataFile.next()
                            print 
                        except StopIteration:
                            print "...End of file..."
                            return False
    
    #Not in use
    @FUNC_NAME    
    def YieldLine(self, log):        
        with open(log, 'r') as dataFile:
            #for testing
            with open(self.outputFullPath, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = self.fieldNames)
                writer.writeheader()
                
                line = dataFile.next()
                while True:                
                    if self.GetMACID(line) is not None:
                        
                        UUT, IPV6, MAC = self.GetMACID(line)                        
                        print "{0:.<25}: {1:<100}\n{2:.<25}: {3:<100}\n{4:.<25}: {5:<100}".format("UUT: ", UUT, "IPV6: ", IPV6, "MAC: ", MAC)
                        #writer.writerow({"UUT": UUT, "IPv6": IPV6, "MAC": MAC})
                        
                        dataFile.next() #count number
                        
                        line = dataFile.next() #time stamp
                        TimeStamp = self.GetTimeStamp(line)
                        print "{0:.<25}: {1:<100}".format("Time stamp: ", TimeStamp)
                        
                        
                        dataFile.next() # ** Battery Status **
                        
                        line = dataFile.next() # last battery test
                        print "{0:.<25}: {1:<100}".format("Last Battery Test: ", self.GetLastBatTest(line))
                         
                        dataFile.next() # ** Status before load test **
                        
                        line = dataFile.next() # Charger Temp
                        print "{0:.<25}: {1:<100}".format("Pre-Test Charger Temp: ", self.GetData(line))
                        
                        line = dataFile.next() # Battery Temp
                        print "{0:.<25}: {1:<100}".format("Pre-Test Batt Temp: ", self.GetData(line))
                        
                        line = dataFile.next() # Battery Voltage
                        print "{0:.<25}: {1:<100}".format("Pre-Test Batt Volt: ", self.GetData(line))
                        
                        dataFile.next() # ** Status after load test **
                        
                        line = dataFile.next() # Charger Temp
                        print "{0:.<25}: {1:<100}".format("Post-Test Charger Temp: ", self.GetData(line))
                        
                        line = dataFile.next() # Battery Temp
                        print "{0:.<25}: {1:<100}".format("Post-Test Batt Temp: ", self.GetData(line))
                        
                        line = dataFile.next() # Battery Voltage
                        print "{0:.<25}: {1:<100}".format("Post-Test Batt Volt: ", self.GetData(line))
                        
                        dataFile.next() # ** Present Status **
                        
                        line = dataFile.next() # Power Mode
                        print "{0:.<25}: {1:<100}".format("Power Mode: ", self.GetPwrMode(line))
                        
                        line = dataFile.next() # Charger Temp
                        print "{0:.<25}: {1:<100}".format("Present Charger Temp: ", self.GetData(line))
                        
                        line = dataFile.next() # Battery Temp                    
                        #print "Post-Test Batt Temp: ", self.GetData(line)
                        print "{0:.<25}: {1:<100}".format("Present Batt Temp: ", self.GetData(line))
                        
                        line = dataFile.next() # Battery Voltage                    
                        print "{0:.<25}: {1:<100}".format("Present Batt Volt: ", self.GetData(line))
                        
                        line = dataFile.next() # Battery Current                   
                        print "{0:.<25}: {1:<100}".format("Present Batt Current: ", self.GetData(line))
    
                        line = dataFile.next() # Time since last batt ev
                        print "{0:.<25}: {1:<100}".format("Time since last batt ev: ", self.GetBattEvent(line))                                    
                                                                
                    else:
                        try:
                            line = dataFile.next()
                            print 
                        except StopIteration:
                            print "...End of file..."
                            return False
            
                
    #@FUNC_NAME
    def ConvIpMac(self, input):
        #determine its IPv6 or MacID
        ipv6Input = re.compile("([0-9a-fA-F]{4}::[0-9a-fA-F]{3}:([0-9a-fA-F]{4}:){2}[0-9a-fA-F]{4})")
        macInput = re.compile("([0-9a-fA-F]{2}:{0,1}){7}[0-9a-fA-F]{2}")
        macInput2 = re.compile("[0-9a-fA-F]{16}")
                
        if ipv6Input.match(input) is not None:
            #print input
            mac = re.sub(':', '', input, flags=re.IGNORECASE)
            mac = re.sub('^fe802', '00', mac, flags=re.IGNORECASE)
            return mac.upper() # return mac ID in upper case
        elif (macInput.match(input) or macInput2.match(input)) is not None:
            #print input
            ipv6 = re.sub(':', '', input, flags=re.IGNORECASE)
            ipv6 = re.sub('^00', 'fe802', ipv6, flags=re.IGNORECASE)
            ipv6 = re.sub('(?<=^([0-9a-f]){4})','::', ipv6, flags=re.IGNORECASE)
            ipv6 = re.sub('(?<=^([0-9a-f:]){9})',':', ipv6, flags=re.IGNORECASE)
            ipv6 = re.sub('(?<=^([0-9a-f:]){14})',':', ipv6, flags=re.IGNORECASE)
            ipv6 = re.sub('(?<=^([0-9a-f:]){19})',':', ipv6, flags=re.IGNORECASE)
            return ipv6
        else:
            print "No match for neither IPv6 nor MAC ID"
            return None
                
    
    #@FUNC_NAME
    def GetMACID(self, line, printInfo=0):
        '''
            i.e.
            line = "REL_B:  fe80::213:50ff:fe11:e000"
            return "REL_B", "fe80::213:50ff:fe11:e000", "1350FFFE11E000"
        '''
        #regex for
        #REL_B:  fe80::213:50ff:fe11:e000
        #match REL_B: (^(\w*|\d*|_*)(?=:\s*fe80))
        #match IPV6: ([0-9a-fA-F]{4}::[0-9a-fA-F]{3}:([0-9a-fA-F]{4}:){2}[0-9a-fA-F]{4})
#    if self.ssed == False:
        uutInput = re.compile("(^(\w*|\d*|_*)(?=:\s*fe80))")
        ipv6Input = re.compile("([0-9a-fA-F]{4}::[0-9a-fA-F]{3}:([0-9a-fA-F]{4}:){2}[0-9a-fA-F]{4})")            
        uut = uutInput.match(line)
        ipv6 = ipv6Input.search(line)            
        if uut is not None:
#            self.ssed = True
            #print line,
            #print uut.group(0)
            #print ipv6.group(0)
            #print self.ConvIpMac(ipv6.group(0))
            return uut.group(0), ipv6.group(0), self.ConvIpMac(ipv6.group(0))

    
    def GetTimeStamp(self, line):
        '''
            i.e.
            line = Tue Aug  4 16:33:02 PDT 2015
            return "Tue", "Aug", 4, 16, 33, 02, "PDT", 2015
        '''
        #regex for
        #Mon Tue Wed Thr Fri Sat Sun ^((Mon)|(Tue)|(Wed)|(Thr)|(Fri)|(Sat)|(Sun))
        #Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec 
        #
        #
#         timeStamp = re.compile(('(?P<wday>^((Mon)|(Tue)|(Wed)|(Thr)|(Fri)|(Sat)|(Sun))'
#                                 '(?P<month>(?=\s)((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec))'
#                                 '(?P<day>'
#                                 '(?P<sec>\d{2}(\.\d{3}|)))'
#                                 , line))
        Result = line.strip('\n')
        #print "Result: ", Result
        day = re.match(r"^.{3}", Result)
        #print "day: ", day
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        if day is not None:            
            if day.group(0) in days:
                return Result
            else:
                return None
    
    def GetEntry(self, line):
        Input = re.compile("^\d{1,4}$")
        Result = Input.search(line)
        if Result is not None:
            return Result.group(0)
        
    def GetText(self, line, text):
        '''
            i.e.
            line = "Any test                :  Any Text Result."
            return "Any Text Result."
        '''
        Input = re.compile("(?<=^%s).*" % text)
        Result = Input.search(line)
        if Result is not None:
            return Result.group(0)
    
    def GetPwrMode(self, line):
        '''
            i.e.
            line = "Power Mode              :  Battery is OFF; device is operating on external power."
            return "Battery is OFF; device is operating on external power."
        '''
        Input = re.compile("(?<=^Power Mode              :  ).*")        
        Result = Input.search(line)        
        if Result is not None:            
            return Result.group(0)
    
    def GetBattCap(self, line):
        '''
            i.e.
            line = "Battery Capacity        :  Faulty"
            return "Faulty"
            
            line = "Battery Capacity        :  Initializing"
            return "Initializing"
            
            line = "Battery Capacity        :  0.00 percent"
            return "0.00 percent"
        '''
        Input = re.compile("(?<=^Battery Capacity        :  ).*")
        Result = Input.search(line)       
        if Result is not None:            
            return Result.group(0)
    
    def GetData(self, line):
        '''
            i.e.
            line = "Charger Temperature     :  31.12 C."
            return 31.12
        '''
        Input = re.compile("(?<=^[\w\s:]{27})\d{1,3}.\d{1,2}")        
        Result = Input.search(line)        
        if Result is not None:
            return Result.group(0)
        else:
            return 0
    
    def GetChrTemp(self, line):
        '''
            i.e.
            line = "Charger Temperature     :  31.12 C."
            return 31.12
        '''
        Input = re.compile("(?<=^Charger Temperature     :  )\d{1,2}.\d{1,2}")        
        Result = Input.search(line)        
        if Result is not None:
            return Result.group(0)
    
    
    def GetBatTemp(self, line):
        '''
            i.e.
            line = "Battery Temperature     :  31.12 C."
            return 31.12
        '''
        Input = re.compile("(?<=^Battery Temperature     :  )\d{1,2}.\d{1,2}")        
        Result = Input.search(line)        
        if Result is not None:
            return Result.group(0)
    
    
    def GetBatVolt(self, line):
        '''
            i.e.
            line = "Battery Voltage         :  1.12 V."
            return 1.12
        '''
        Input = re.compile("(?<=^Battery Voltage         :  )\d{1,2}.\d{1,2}")        
        Result = Input.search(line)        
        if Result is not None:
            return Result.group(0)
    
    
    def GetBatCurr(self, line):
        '''
            i.e.
            line = "Battery Charge Current  :  11.12 mA."
            return 11.12
        '''
        Input = re.compile("(?<=^Battery Charge Current  :  )\d{1,2}.\d{1,2}")        
        Result = Input.search(line)        
        if Result is not None:
            return Result.group(0)

    def GetLastBatTest(self, line):
        '''
            i.e.
            line = "Last Battery Test       :  Tue Aug  4 14:54:42 2015"
            return  "Tue Aug  4 14:54:42 2015", "Tue Aug  4 14:54 2015"
        '''        
        Input = re.compile("(?<=^Last Battery Test       :  ).*")
        Result = Input.search(line)        
        if Result is not None:
            LastBatDate = re.sub(':\d{2}\s', '', Result.group(0), flags=re.IGNORECASE)
            return Result.group(0), LastBatDate
    
    
    def GetBattEvent(self, line):
        '''
            i.e.
            line = "Time since last batt ev :  3004 seconds."
            return 3004
        '''
        #regex for
        #(?<=^Time since last batt ev :  )\d{1,}
        Input = re.compile("(?<=^Time since last batt ev :  )\d{1,}")        
        Result = Input.search(line)        
        if Result is not None:            
            return Result.group(0)
    
    @FUNC_NAME
    def Test(self):
        for i in self.YieldLine(self.logFullPath):
            #print i
            print self.GetMACID(i[1])
            print self.GetBattEvent(i[1])

    