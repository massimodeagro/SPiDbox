# Preparing the ciruit

In this folder, you will find a PDF with the schematic of the circuit. If you wish to make your own circuit board, just follow the schematic. If you instead prefer, you can download the zip containing the gerber file (this have been generated with easyEDA https://easyeda.com/

## Things you will need

Before starting, you will need to acquire some components. The following are all trough hole components (THC):
* 49 male pin 2.54mm-pitch connectors, like [this](https://www.pololu.com/product/965). Specifically, you will need a 2x20 long strip, a 5 long strip and a 4 long strip.
* 26 female pin 2.54mm-pitch connectors, like [this](https://www.pololu.com/product/1030). Specifically, you will need two 8 long strips and one 10 long strip. If you buy a signle long female pin connector strip, be aware that by cutting it you will lose the connector on the cut position, so buy a slightly longer strip.
* A two pin 2.54mm-pitch jst-xh connector, like [this](https://www.pololu.com/product/2717)
* A four pin 2.54mm-pitch jst-xh connector, of the same type of the one above
* A stepper motor driver. In the schematic an A4988 is reported, but many drivers have the same pinout structure. Just be sure that the pins positions is the same as in the A4988
* A rotary encoder with its breakout board.
* A SSD1306 oled screen with its breakout board.
* An ADS1115 analog to digital converted with its breakout board.
* 5 1kohm resistor.
* 1 1N4448 diode.
* 1 BD139 transistor.
* 1 100uf electrolytic capacitor.
* 5 female 3.5mm jack connectors (to solder onto the board, so it needs to be a THC component).
* 5 male 3.5mm jack connectors (to solder to a cable).
* 1 female power jack connector (to solder onto the board, so THC).
* 1 lm2596 buck converter.
* 1 12V, at least 5A power supply.
* 1 female to famale 2x20 jumper wire. this is to connect the raspberry to the circuit board.
* 9 female to female jumper wire.
* A 12V led strip.
* A soldering iron and solder.

## Things to do to successfully solder your board

The process of building the board is straight forward, just solder the right components on their places. But you will need to take some care.

* Note that the board has a front and a back side. The front side present the name of the SPiDbox on the bottom right.
* Solder two 20 long male strips on the raspberry pi slot on the board. The strips need to end up having the long pin sticking out from the back side of the board. So while looking at the board back side, fit in the holes the short end of the pin, then solder the protruding end from the front.
* All other components will stick out from the front face.
* The connectors for the oled screen and the rotary encoder will be done with the remaining male strip pins, as these two components will not sit on the board, but will be attatched to the front of the SPiDbox. 
* For the stepper motor driver and the ADS, use female connectors.
* Next, solder the two jst-xh in their respective places
* Solder in the resistors, the diode and the capacitor (be aware of capacitor polarity)
* Solder in the 3.5mm jacks and the power jack
* Lastly, solder the buck converter

**ATTENTION -- at this point, connect the board to the 12V power supply, BEFORE connecting any components in (drivers, raspberry, ADS, oled screen, etc.) and regulate the buck converter output voltage to 5V. If you connect the raspberry and the voltage is to high you will burn it**

* Once the voltage is adjusted, you can connect everything up. Be aware of polarity and orientation of every component. For all of them there is an indication printed on the board. For the raspberry, there is a "+" sign on one side of the connector. That side is the side that has the 5V pins, so orient the connector on the raspberry so that those pins match.
* Use the jumper wires to connect the rotary encoder and the oled screen
* Lastly, connect the two motors to the 4 pins and 2 pins connector

The 5 3.5mm jacks are of two types. The 4 on the left are for photo-resistor. Connect each lead of the photoresistor with a cable and then to the jack ends. The photoresistor has no polarity, but if you have a 3 ends jack instead of a 2 ends jack, be aware of which 2 of the 3 you use to not create a short. In the current 3d model of the SPiDbox only 2 photo-resistors are used.
The right jack connector is for the LED strip, needed to illuminate the experimental box. For this, polarity is important, so check with a multimiter which lead gets the +12V
