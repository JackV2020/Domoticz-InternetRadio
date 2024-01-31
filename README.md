This Domoticz plugin was developed on a Raspberry Pi and may work on other platforms also.

It is a configurable Internet Radio and is already preconfigured in internetradio.conf.

The plugin can be used to play radio stations from the web browser with which you access your Domoticz.

I have it running on a Raspberry 4 with bullseyse, Domoticz 2024.1 and it works with Bluetooth and also with a JACK connection. I did not test with HDMI.

Remember that when you use it over the Internet while away from home, and you have a speaker connected to your Pi, your Pi will produce the same music although you are not at home.

Remote control, something I can not do with my Sonos.... 

Okay so now you know it is "better than Sonos" you want it, but how do you get it in place ?

There are a few requirements you need to have in place first.

 - Before installing make sure that the requests module is installed :
    sudo apt-get install python3-requests
    ( When already installed it will skip installation and explain it is already installed )
 - to play the radio stations via the speaker of your Raspberry Pi you need mplayer : 
    sudo apt install mplayer
    ( When already installed it will skip installation and explain it is already installed )
    When you do/can not install mplayer it wil still play radio in the browser on your phone / pc

To test your speaker you may use the next command : speaker-test -c1 -twav -l5

To install the plugin you need to get the contents in your plugin folder :

On a Raspberry Pi you could :

Start a terminal and go to your plugins folder and the next will get it for you into an internetradio folder : 

 ....../plugins$ git clone https://github.com/JackV2020/Domoticz-InternetRadio.git internetradio

To get it into Domoticz restart your domoticz like :

    sudo systemctl restart domoticz

After this you can add a device of the Type 'Jacks Internet Radio'.

NOTES:
 - After selecting a station you click on the link in the 'Actief' device to play on your phone / laptop.
 - Configuring internetradio.conf is easy. How to is in the file itself.
 - A lot of station URLs are available on https://www.hendrikjansen.nl/henk/streaming.html
 - Many thanks to Hendrik Jansen for maintaining this list.

Thanks for reading and enjoy.
