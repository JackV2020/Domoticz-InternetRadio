#
# Title : Jacks Internet Radio
# Author: Jack Veraart
# Date  : 2021-04-15
# 
"""
<plugin key="JacksInternetRadio" name="Jacks Internet Radio" author="Jack Veraart" version="2.0">
    <description>
        <font size="4" color="white">Internet Radio</font><font color="white">...Notes...</font>
        <ul style="list-style-type:square">
            <li><font color="yellow">Requirements:</font></li>
            <li><font color="yellow"> - Install audio player mplayer : sudo apt install mplayer -y </font></li>
            <li><font color="yellow">Preconfigured radio is available in plugin folder in internetradio.conf</font></li>
            <li><font color="yellow">When you have a Password on your domoticz and want an Internet Radio Room, enter admin Username and Password below, otherwise leave as is.</font></li>
            <li><font color="yellow">To develop your own plugin...check this web site... <a href="https://www.domoticz.com/wiki/Developing_a_Python_plugin" ><font color="cyan">Developing_a_Python_plugin</font></a></font></li>
        </ul>
    </description>
    <params>
        <param field="Username" label="Username."       width="120px" default="Username"/>

        <param field="Password" label="Password."       width="120px" default="Password" password="true"/>

        <param field="Mode6" label="Debug."             width="75px">
            <options>
                <option label="True"  value="Debug"/>
                <option label="False" value="Normal"    default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz

# Prepare some global variables

StartupOK=0
LocalHostInfo=''
HeartbeatInterval= 5   # 5 seconds

HomeFolder=''   # plugin finds right value
IPPort=0        # plugin finds right value

Username=''     # plugin finds right value
Password=''     # plugin finds right value

DeviceLibrary={}

class BasePlugin:
    enabled = False
    def __init__(self):
        #self.var = 123
        return

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStart(self):
        
        import os
        global StartupOK
        
        global HomeFolder
        global Username
        global Password

        global LocalHostInfo

        self.pollinterval = HeartbeatInterval  #Time in seconds between two polls

        if Parameters["Mode6"] == 'Debug':
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)

        Domoticz.Log("onStart called")

        try:
#
# Set some globals variables to right values
#            
            HomeFolder      =str(Parameters["HomeFolder"])
            Username        =str(Parameters["Username"])
            Password        =str(Parameters["Password"])

            MyIPPort        =GetDomoticzPort()            

            LocalHostInfo='http://'+Username+':'+Password+'@localhost:'+MyIPPort

            ImportImages()

# Create devices as configured in internetradio.conf

            StartupOK = CreateDevices()
            
            if StartupOK == 1:
                
                Domoticz.Log('onStartup OK')

                Domoticz.Heartbeat(HeartbeatInterval)

            else:
                
                Domoticz.Log('ERROR starting up')
            
        except:

            StartupOK = 0

            Domoticz.Log('ERROR starting up')

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onStop(self):
        Domoticz.Log("onStop called")
        player('stop')

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onCommand(self, Unit, Command, Level, Hue):

        DeviceName=Devices[Unit].Name[8:-9] # remove <center> and </center>

        DeviceType=DeviceLibrary[DeviceName]['Type']
#        Domoticz.Log("onCommand called >"+str(Unit)+'< >'+DeviceName+'< >'+Command+'< >'+str(Level)+'< >'+DeviceType)
        
        if DeviceType == 'Dimmer':  # It is the volume slider

            if Command == 'Off':
                Level = 0
            if Command == 'On':
                Level = 25
            if Level == '100':
                Level = 25

            if Devices[Unit].sValue != str(Level):
                SoundDevice=player('getdevice')
#                Domoticz.Log('SoundDevice: '+SoundDevice)
                player('volume',SoundDevice,str(Level))
                Devices[Unit].Update(  nValue=2, sValue=str(Level))

                        
        elif DeviceType == 'StationList':  # It is a station list

            StationIndex=int(Level/10)-1
            StationName=DeviceLibrary[DeviceName]['StationNames'][StationIndex]
            if StationName.replace(' ','') != '':
                player('stop')
                StationURL=DeviceLibrary[DeviceName]['StationURLs'][StationIndex]
                SoundDevice=player('getdevice')
                Domoticz.Log('Tune into Station: >'+StationName+'< URL >'+StationURL)
                player('play'  ,SoundDevice,StationURL)

                for Device in DeviceLibrary:
                    if DeviceLibrary[Device]['Type'] == 'Text': 
                        if Devices[DeviceLibrary[Device]['Unit']].sValue != StationName:
                            message='<h4>'
                            message=message+'\n'
                            message=message+'\n'
                            message=message+ '<center><font color=blue>' + SoundDevice+'</font><font color=white>............</font></center>'
                            message=message+'\n'
                            message=message+ '<center><font color=blue>' + DeviceName+'</font><font color=white>............</font></center>'
                            message=message+'</h4>'
                            message=message+'\n'
                            message=message+'<h4>'
                            message=message+ '<marquee scrollamount="3"><a href="'+StationURL+'"><font color=blue>Station : </font><font color=green>' + StationName+'</font><font color=red> Click me 🔊 </font></a></marquee>'
                            message=message+'</h4>'
                            message=message+'\n'
                            message=message+'<h4>'
                            message=message+'</h4>'
                            Devices[DeviceLibrary[Device]['Unit']].Update(  nValue=0, sValue=message)

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")
# --------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat  called")
#
# This is to copy the volume slider from the host to the plugin so you can control the volume from host and plugin.
#
        if StartupOK == 1:
            for Device in DeviceLibrary:
                if DeviceLibrary[Device]['Type'] == 'Dimmer': # we have one dimmer and this is for the volume
                    Level=player('getvolume')
                    Domoticz.Debug('SoundDevice Level: '+str(Level))
                    onCommand(DeviceLibrary[Device]['Unit'], 'Set Level', Level, 0)
                
# --------------------------------------------------------------------------------------------------------------------------------------------------------

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Image Management Routines  -----------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetDomoticzPort():
#
# A friend of me runs Domoticz on a non standard port, so to make it working for him too.....
#
    global IPPort
    
    pathpart=Parameters['HomeFolder'].split('/')[3]
    searchfile = open("/etc/init.d/"+pathpart+".sh", "r")
    for line in searchfile:
        if ("-www" in line) and (line[0:11]=='DAEMON_ARGS'): 
            IPPort=str(line.split(' ')[2].split('"')[0])
    searchfile.close()
    Domoticz.Debug('######### GetDomoticzPort looked in: '+"/etc/init.d/"+pathpart+".sh"+' and found port: '+IPPort)
    
    return IPPort

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def GetImageDictionary(HostInfo):
#
# HostInfo : http(s)://user:pwd@somehost.somewhere:port
#
    import json
    import requests

    try:
        mydict={}

        url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?type=custom_light_icons'
        username=HostInfo.split(':')[1][2:]
        password=HostInfo.split(':')[2].split('@')[0]

        response=requests.get(url, auth=(username, password))
        data = json.loads(response.text)
        for Item in data['result']:
            mydict[str(Item['imageSrc'])]=int(Item['idx'])

    except:
        mydict={}
    
    return mydict

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def ImportImages():
#
# Import ImagesToImport if not already loaded
#
    import glob

    global ImageDictionary

    ImageDictionary=GetImageDictionary(LocalHostInfo)
    
    if ImageDictionary == {}:
        Domoticz.Log("ERROR I can not access the image library. Please modify the hardware setup to have the right username and password.")      
    else:

        for zipfile in glob.glob(HomeFolder+"CustomIcons/*.zip"):
            importfile=zipfile.replace(HomeFolder,'')
            try:
                Domoticz.Image(importfile).Create()
                Domoticz.Debug("Imported/Updated icons from "  + importfile)
            except:
                Domoticz.Log("ERROR can not import icons from "  + importfile)

        ImageDictionary=GetImageDictionary(LocalHostInfo)

        Domoticz.Debug('ImportImages: '+str(ImageDictionary))
         
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Device Creation Routines  ------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateDevice(deviceunit,devicename,devicetype,devicelogo="",devicedescription="",sAxis="",InitialValue=0.0):
    
    if deviceunit not in Devices:

        if ImageDictionary == {}:
            firstimage=0
            firstimagename='NoImage'
            Domoticz.Log("ERROR I can not access the image library. Please modify the hardware setup to have the right Username and Password.")      
        else:
            firstimage=int(str(ImageDictionary.values()).split()[0].split('[')[1][:-1])
            firstimagename=str(ImageDictionary.keys()).split()[0].split('[')[1][1:-2]
            Domoticz.Debug("First image id: " + str(firstimage) + " name: " + firstimagename)

        if firstimage != 0: # we have a dictionary with images and hopefully also the image for devicelogo

            try:

                deviceoptions={}
                deviceoptions['Custom']="1;"+sAxis
                Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=ImageDictionary[devicelogo], Description=devicedescription).Create()
                Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue))
                Domoticz.Debug("Created device : " + devicename + " with '"+ devicelogo + "' icon and options "+str(deviceoptions)+' Value '+str(InitialValue))
            except:

# when devicelogo does not exist, use the first image found, (TypeName values Text and maybe some others will use standard images for that TypeName.)

                try:
                    Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName=devicetype, Used=1, Image=firstimage, Description=devicedescription).Create()
                    Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=str(InitialValue))
                    Domoticz.Debug("Created device : " + devicename+ " with '"+ firstimagename + "' icon and Value "+str(InitialValue))
                except:
                    Domoticz.Log("ERROR Could not create device : " + devicename)
#
# Devices are created with as prefix the name of the Hardware device as you named it during adding your hardware
# The next replaces that prefix, also after every restart so names are fixed
#
    try:

# Note that deviceoptions needs to be a python dictionary so first create a dictionary and fill it with 1 entry

        deviceoptions={}
        deviceoptions['Custom']="1;"+sAxis

        NewName = '<center>'+devicename+'</center>'
        Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=Devices[deviceunit].sValue, Name=NewName, Options=deviceoptions, Description=devicedescription)
    except:
        dummy=1
# -----------------------------# --------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateSelectorSwitch(deviceunit,devicename,devicebuttons,devicelogo="",devicedescription="",SelectorStyle=0):
#
# Create a selector switch devicebuttons format : button1|.....|buttonx
#
    if deviceunit not in Devices:

        firstLevelName=devicebuttons.split('|')[0]
        Domoticz.Debug('First Level: '+firstLevelName)

        if (SelectorStyle == 0): 
            Options = {'LevelActions': '|'*(devicebuttons.count('|')+1),
                             'LevelNames': firstLevelName+'|'+devicebuttons,
                             'LevelOffHidden': 'true',
                             'SelectorStyle': '0'}
        else:
            Options = {'LevelActions': '|'*(devicebuttons.count('|')+1),
                             'LevelNames': firstLevelName+'|'+devicebuttons,
                             'LevelOffHidden': 'true',
                             'SelectorStyle': '1'}
        try:
            Domoticz.Device(Name=devicename, Unit=deviceunit, TypeName="Selector Switch", Switchtype=18, Image=ImageDictionary[devicelogo], Options=Options, Used=1,Description=devicedescription).Create()
            Domoticz.Debug("Created device : " + devicename + " with '"+ devicelogo + "' icon and options "+str(Options))
        except:
            Domoticz.Log("ERROR Could not create selector switch : " + devicename)
#
# Devices are created with as prefix the name of the Hardware device as you named it during adding your hardware
# The next replaces that prefix, also after every restart so names are fixed
#
    try:
#        NewName = LocationCode+devicename
        NewName = '<center>'+devicename+'</center>'

        index=int(Devices[deviceunit].nValue/10)-1
        firstLevelName=devicebuttons.split('|')[index]
#        Domoticz.Log('...'+devicebuttons+'...'+str(index)+'...'+firstLevelName)

        if (SelectorStyle == 0): 
            Options = {'LevelActions': '|'*(devicebuttons.count('|')+1),
                             'LevelNames': firstLevelName+'|'+devicebuttons,
                             'LevelOffHidden': 'true',
                             'SelectorStyle': '0'}
        else:
            Options = {'LevelActions': '|'*(devicebuttons.count('|')+1),
                             'LevelNames': firstLevelName+'|'+devicebuttons,
                             'LevelOffHidden': 'true',
                             'SelectorStyle': '1'}
        Domoticz.Debug('Update settings for: '+NewName)
        if NewName != Devices[deviceunit].Name or Options != Devices[deviceunit].Options :
            Devices[deviceunit].Update(nValue=Devices[deviceunit].nValue, sValue=Devices[deviceunit].sValue, Name=NewName,Options=Options,Description=devicedescription)

# the next forces the right logo to be set after startup

        UpdateSelectorSwitch(deviceunit,Devices[deviceunit].nValue)
    except:
        dummy=1

#---------------------------------------------------------------------------------------------------------------------------

def CreateDevices():

    global DeviceLibrary
    
    DeviceLibrary={}
    Name=''
    Type=''
    Units=''
    Command=''
    MyStatus=1
    ConfigFile='internetradio.conf'
    try:
        TheConfigFile=open(HomeFolder+ConfigFile, "r")
        TheConfigFile.close
        for Line in TheConfigFile:
            linea=Line

            if Line[0] not in ['#', ' ', '\t', '\n' ] and Line.replace(' ','').replace('\t','') != '\n':    # skip comments and empty lines

                Line=Line.replace('\n','')                  # remove EOL
                if Line.split('=')[0] == 'Description':
                    DeviceEntry={}
                    Description = Line.split('=')[1]
                    DeviceEntry['Description']   = Description
                    DeviceEntry['Unit']   = -1
                    StationCounter=0
                    StationLabels=''
                    StationNames=[]
                    StationURLs=[]
                elif Line.split('=')[0] == 'Name':
                    Name = Line.split('=',1)[1]
                    DeviceEntry['Name']   = Name
                elif Line.split('=')[0] == 'Type':
                    TypeName = Line.split('=')[1]
                    DeviceEntry['Type']   = TypeName
                elif Line.split('=')[0] == 'Units':
                    Units = Line.split('=')[1]
                    DeviceEntry['Units']   = Units
                elif Line.split('=')[0] == 'Station':
                    StationLabel = Line.split('=',1)[1]
                    StationLabel = StationLabel.split(';')[0]
                    StationName=StationLabel
                    StationURL = Line.split('=',1)[1]
                    StationURL = StationURL.split(';')[1]
                    StationLabels=StationLabels+'|'+StationLabel
                    StationNames.append(StationName)
                    StationURLs.append(StationURL)
                    StationCounter = StationCounter + 1
                    Domoticz.Debug('Stations: '+str(StationCounter)+' '+StationLabels)
                    Domoticz.Debug('URLs: '+str(StationCounter)+' '+str(StationURLs))
                elif Line.split('=')[0] == 'Image':
                    Image = Line.split('=')[1]
                    DeviceEntry['Image']  = Image
                    DeviceEntry['StationLabels']  = StationLabels[1:]
                    DeviceEntry['StationNames']  = StationNames
                    DeviceEntry['StationURLs']  = StationURLs
                    DeviceEntry['StationCounter']  = StationCounter
                    DeviceLibrary[Name]   = DeviceEntry
                    Domoticz.Debug(str(DeviceEntry))
                else:
                    Domoticz.Debug('Error Line: '+Line)
                    MyStatus=-1
        Domoticz.Debug(str(DeviceLibrary))
    except:
        MyStatus=-1
        Domoticz.Log('Error opening config file: '+HomeFolder+ConfigFile)

    if MyStatus == 1:

#
# Delete all my devices
#
        DeleteOne=1
        while DeleteOne == 1: # My implementation of repeat until, make sure to get into the loop and immediately make sure to get out of it
            DeleteOne = 0
            for Unit in Devices: # inner loop to find what to delete
                DeleteOne = 1                                               # stay in the loop because we may have to do our thing again
                UnitToDelete = Unit
                Item=Devices[Unit].Name
            if DeleteOne == 1: # out of the inner loop it is safe to delete
                Domoticz.Debug('.....')
                Domoticz.Debug('.....Delete  my own device:  **'+Item+'**  Unit: **'+str(UnitToDelete)+'**')
                Devices[UnitToDelete].Delete()
                Domoticz.Debug('.....Deleted my own device:  **'+Item+'**  Unit: **'+str(UnitToDelete)+'**')
#
# Create all my devices from internetradio.conf
#
        for Device in DeviceLibrary:
            if DeviceLibrary[Device]['Unit'] == -1:
                Unit = 1
                while Unit in Devices:
                    Unit = Unit + 1
                DeviceLibrary[Device]['Unit'] = Unit
                
            if DeviceLibrary[Device]['Type'] == 'StationList' :
                Domoticz.Debug('Create '+str(Device))
                CreateSelectorSwitch(Unit,DeviceLibrary[Device]['Name'],DeviceLibrary[Device]['StationLabels'],DeviceLibrary[Device]['Image'],DeviceLibrary[Device]['Description'],1)
            if DeviceLibrary[Device]['Type'] == 'Dimmer' :
                Domoticz.Debug('Create '+str(Device))
                CreateDevice(Unit,DeviceLibrary[Device]['Name'],'Dimmer',DeviceLibrary[Device]['Image'],DeviceLibrary[Device]['Description'],DeviceLibrary[Device]['Units'],0)
            if DeviceLibrary[Device]['Type'] == 'Text' :
                Domoticz.Debug('Create '+str(Device))
                CreateDevice(Unit,DeviceLibrary[Device]['Name'],'Text','',DeviceLibrary[Device]['Description'],'',0)
#
# Create Internet Radio Room internetradio.conf
#
        for Device in DeviceLibrary:

            if DeviceLibrary[Device]['Type'] == 'Room' :
                Domoticz.Debug('Create Room: '+DeviceLibrary[Device]['Name'])
                RoomIDX = CreateRoom(LocalHostInfo,DeviceLibrary[Device]['Name'])
                
#
# Add all items to Internet Radio Room
#
        for Device in DeviceLibrary:

            if DeviceLibrary[Device]['Type'] != 'Room' :
                Domoticz.Debug('Add Room Item: '+DeviceLibrary[Device]['Name']+' idx: '+str(Devices[DeviceLibrary[Device]['Unit']].ID))
                AddToRoom(LocalHostInfo,RoomIDX,Devices[DeviceLibrary[Device]['Unit']].ID)
#
# Make sure there is no mplayer process active
#                
        player('stop')

    return MyStatus

# --------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateRoom(HostInfo,RoomName):
#
# HostInfo : http(s)://user:pwd@somehost.somewhere:port
#
    import json
    import requests
    
    idx=0

    try:

        username=HostInfo.split(':')[1][2:]
        password=HostInfo.split(':')[2].split('@')[0]

        Domoticz.Debug('Find Room')
        
        url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?type=plans&order=name&used=true'
        response=requests.get(url, auth=(username, password))
        data = json.loads(response.text)
        if 'result' in data.keys():
            for Item in data['result']:
                if str(Item['Name']) == RoomName:
                    idx=int(Item['idx'])

        if idx != 0 :
            Domoticz.Debug('Delete Room')
            url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?idx='+str(idx)+'&param=deleteplan&type=command'
            response=requests.get(url, auth=(username, password))

        Domoticz.Debug('Create Room')
        
        url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?name='+RoomName+'&param=addplan&type=command'
        response=requests.get(url, auth=(username, password))
        data = json.loads(response.text)
        idx=int(data['idx'])

    except:
        idx=-1
    
    return idx
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def AddToRoom(HostInfo,RoomIDX,ItemIDX):
#
# HostInfo : http(s)://user:pwd@somehost.somewhere:port
#
    import json
    import requests
    
    idx=0

    try:

        username=HostInfo.split(':')[1][2:]
        password=HostInfo.split(':')[2].split('@')[0]

        Domoticz.Debug('Add Item To Room')
        
        url=HostInfo.split(':')[0]+'://'+HostInfo.split('@')[1]+'/json.htm?activeidx='+str(ItemIDX)+'&activetype=0&idx='+str(RoomIDX)+'&param=addplanactivedevice&type=command'

        response=requests.get(url, auth=(username, password))
        data = json.loads(response.text)

    except:
        idx=-1

    return idx
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------  Hardware Routines --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def player(action, device='', what=''):

    import subprocess
    import time
    
    returncode='None'
    
    if action == 'getdevice':
        command='su -c - pi "amixer | head -n 1 | cut -b 22-100"'
    elif action == 'play':
        command='su -c - pi "nohup mplayer -msglevel all=-1 '+ what + ' > /dev/null 2>&1 &"'
    elif action == 'volume':
        command='su -c - pi "amixer set '+device+' '+str(what)+'%"'
    elif action == 'getvolume':
        command='su -c - pi amixer | grep "%" | head -1 | cut -d "[" -f 2 | cut -d "%" -f 1'
    elif action == 'stop':
        command ='killall mplayer'
    Domoticz.Log("player command : "+command)
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if action in ['getdevice', 'getvolume']:
            timeouts=0
            while timeouts < 10:
                p_status = process.wait()
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    if action == 'getdevice':
                        device=str(output.strip())[2:-3]
                        returncode=device
                    if action == 'getvolume':
                        volume=str(output.strip())[2:-1]
                        returncode=volume
                    timeouts=10
                else:
                    time.sleep(0.2)
                    timeouts=timeouts+1
    except:
        returncode='None'

    return returncode


# --------------------------------------------------------------------------------------------------------------------------------------------------------
