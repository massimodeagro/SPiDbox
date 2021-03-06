# Install the software

This readme will guide you in the process of installing the software onto your Raspberry Pi. Before starting, be sure to have:
* Your Raspberry Pi zero, that will drive the SPiDbox
  if your Raspberry Pi Zero does not have a wifi receiver (not the W version), you will also need a Raspberry Pi 3B for the installation process
* A USB keyboard
* A USB to micro-USB adapter
* A monitor with HDMI connector
* A HDMI to micro-HDMI adapter or cable
* A wifi internet connection
* A micro-sd card
* A computer that can read micro-sd cards

## Install Raspbian

The first step to install the SPiDbox is to install the Raspberry Pi OS. You will need a micro sd card. The minimum workable size is 8gb, but the bigger it is the longer you can work with it before needing to empty the card from the videos.

1. connect the SD card to your computer and download the raspbian OS https://www.raspberrypi.org/downloads/raspberry-pi-os/. The SPiDbox can work with the "Lite" version of Raspbian. Be aware however that this version has no desktop, so if you don't feel confident with working only with the command line, download the "desktop" version.
2. Connect the SD card, download and install on your computer etcher https://www.balena.io/etcher/. Launch the software and follow instruction to flash the Raspbian os onto the SD card. **This process will wipe any content on your sd-card, so be sure there are no important files inside and that you are selecting the right device**
3. Let the process finish

Note that you can read and write on this sd card only with a Linux computer, or you will need to install dedicated software on your windows or mac computer to make it able to mount and read EXT4 partitions. 

Once able to read the sd, you should be able to see two partitions: one called "boot" and one called "rootfs"

Enter the configuration GUI

## Setup your Raspbian

On this guide, I will describe steps for the "Lite" version of Raspbian, and I will assume you have a keyboard and an HDMI monitor. If you do not have them around and you have experience with raspberry pi, you can set up your Raspbian in "headless" mode by enabling ssh.

1. While the sd-card is still connected to the computer, copy the files from this repository into the raspberry.
      * The files inside the 'OS' folder need to be placed in /home/pi/.
      * Note that 'OS' contains a subfolder, subjs. This folder defines the subjects available for testing. Here is also where the logs and the video will be saved. To insert a new subject, copy the '001' folder and paste it with a new name. The software will recognize the folder names here as the available subjects
      * Also copy the 'screenImages' folder here. Not the content, the whole folder
2. Connect to your Raspberry the keyboard, the screen, insert the sd-card and connect to power
  You do not necessarily need the camera connected for setting up your system, but you can connect it now for testing purposes
3. Once connected to power the raspberry pi will boot. In some minutes it should bring you to the command line
  Note that on your first login, you will be asked to provide the "login", or username, and password. The default username is "pi", the default password is "raspberry"
4. First, let's enable fast login, so you will not be prompted for username and password anymore. Enter the configuration GUI
    ```
    $ sudo raspi-config
    ```
    note, the command sudo will prompt a request for the password.
    choose "Boot Options" -> "Desktop/CLI" and choose "Console autologin".
 
    
5. Next, you will need to connect to your wifi. If you closed it from the step before, reopen the configuration GUI
    ```
    $ sudo raspi-config
    ```
    
    select "Localisation Options" -> "Change wireless country" and specify your location. Then close the config
    next, open the `wpa-supplicant` file by the command
    ```
    $ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
    ```
    go to the bottom of the file and add
    ```
    network={
      ssid="yourwifiname"
      psk="tyourwifiPassword"
    }
    ```
6. now, activate the various interfaces. Go back in the configuration
    ```
    $ sudo raspi-config
    ```
    select "Interfacing Options", from there you need to activate the camera, the SPI and I2C. Then close settings and reboot the system by
     ```
    $ sudo reboot
    ```
7. next, update your system
    ```
    $ sudo apt update
    $ sudo apt upgrade
    ```
8. install dependencies
    
    First, the OLED screen control. The package GitHub page is https://github.com/rm-hull/luma.oled/. We are installing old versions here as the current version only supports python >3.5
    ```
    $ sudo apt install python-dev python-pip libfreetype6-dev libjpeg-dev build-essential libopenjp2-7 libtiff5
    $ sudo -H pip install luma.core==1.6.0
    $ sudo -H pip install luma.oled==2.3.1
    ```
    next, the analog to digital converter control, from Adafruit. This is again an older version for pyton2.7 support
    ```
    $ sudo -H pip install adafruit-ads1x15
    ```
    the python raspberry pi camera module
    ```
    $ sudo -H pip install picamera
    ```
    lastly, fonts support 
    ```
    $ sudo apt install fontconfig
    ```
9. to make so that the software launches on boot, you need to add the code into the  `.bashrc` file. to do so, type
    ```
    $ sudo nano .bashrc
    ```
    scroll to the end of the file and write
    ```
    python mainMenu.py
    ```
    close the file and save.
