# Install the software

This readme will guide you in the process of installing the software onto your raspberry Pi. Before starting, be sure to have:
* Your Raspberry Pi zero, that will drive the SPiDbox
  if your Raspberry Pi zero does not have a wifi receiver (not the W version), you will also need a Raspberry Pi 3B for the installation process
* A usb keyboard
* A usb to micro-usb adapter
* A monitor with HDMI connector
* A HDMI to micro-HDMI adapter or cable
* A wifi internet connection
* A micro-sd card
* A computer thatcan read micro-sd cards

## Install Raspbian

The first step to install the SPiDbox is to install the raspberry Pi OS. You will need a micro sd card. The minimum workable size is 8gb,but the bigger it is the longer you can work with it before needing to empty the card from the videos.

1. connect the SD card to your computer and download the raspbian OS https://www.raspberrypi.org/downloads/raspberry-pi-os/. The SPiDbox can work with the "Lite" version of Raspbian. Be aware however that this version has no desktop, so if you don't feel confident with working only with the command line, download the "desktop" version.
2. Connect the SD card, Download and install on your computer etcher https://www.balena.io/etcher/. Launch the software and follow instruction to flash the Raspbian os onto the SD card. **This process will wipe any contnent on your sd-card, so be sure there are no important files inside and that you are selecting the right device**
3. Let the process finish

Note that you can read and write on this sd card only with a linux computer, or you will need to install dedicated software on your windows or mac computer to make it able to mount and read EXT4 partitions. 

Once able to read the sd, you should be able to see two partitions: one called "boot" and one called "rootfs"

## Setup your Raspbian

On this guide I will describe steps for the "Lite" version of Raspbian, and I will assume you have keyboard and an HDMI monitor. If you do not have them around and you have experience with raspberry pi, you can setup your Raspbian in "headless" mode by enabling ssh.

1. Connect to your raspbberry the keyboard, the screen, insert the sd-card and connect to power
  You do not necessarly need the camera connected for setting up your system, but you can connect it now for testing purposes
2. Once connected to power the raspberry pi will boot. In some minutes it should bring you to the command line
3. First, you will need to connect to your wifi. Enter the configuration gui
  ```
  $ sudo raspi-config
  ```
  note, the command sudo will prompt a request for password. The default password for the raspberry is "raspberry"
  select "Localisation Options" -> "Change wireless country" and specfy your location. Then close the config
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
4. now, activate the camera. Go back in the configuration
  ```
  $ sudo raspi-config
  ```
  select "Interfacing Options" -> "Camera"  and enable it. Close settings and reboot the system by
   ```
  $ sudo reboot
  ```
4. next, update your system
  ```
  $ sudo apt update
  $ sudo apt upgrade
  ```
