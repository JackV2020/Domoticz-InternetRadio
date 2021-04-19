This plugin is a configurable Internet Radio and is already preconfigured in internetradio.conf.

A lot of station URLs are available on https://www.hendrikjansen.nl/henk/streaming.html

Many thanks to Hendrik Jansen for maintaining this list.

The plugin can be used to play music from the web browser with which you access your Domoticz.

So music will come out of your phone, tablet, PC etc.

When installed on a Raspberry Pi it will also play on the (bluetooth) speaker connected to the Raspberry Pi.

This plugin may ( be modified to ) work on other platforms too.

When you have access to your Domoticz over Internet you will have your personal Internet Radio available everywhere. 

To install the plugin you need the contents of the zip file.

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next wget command will download a zip file, unpack and remove the zipfile : 

 ....../plugins$ wget https://raw.githubusercontent.com/JackV2020/Domoticz-InternetRadio/main/internetradio.zip -O internetradio.zip && unzip -o internetradio.zip && rm internetradio.zip

After this you need to do some required actions.

REQUIRED ACTIONS :

The plugin uses 'mplayer' and so called 'passwordless ssh between root and pi'.

Both are easy to get in place :
( you may need to accept some things by giving right answers )

 - start a terminal window
 - sudo -i 
 - apt install mplayer -y
 - ssh-keygen  
        ( 3 x enter )
 - ssh-copy-id -i ~/.ssh/id_rsa.pub pi@localhost 
        ( answer questions to continue )
 - ssh pi@localhost amixer 
        ( should give : Simple mixer control 'Master',0 )
 - exit
 - exit

Configuring internetradio.conf is easy. Do it now or do it later.

 - Stations are grouped so they appear in drop down menus of selector switches.

 - Just add/remove/change stations and/or selector switches.

Now to get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks Internet Radio'.

When you do not like the Type name 'Jacks Internet Radio' feel free to edit plugin.py and modify it before you actually add your hardware.

NOTES:
 - click on the link in the marquee in the last device on your Domoticz to play on your phone / laptop.
 - after changing internetradio.conf restart the plugin.

Thanks for reading and enjoy.
