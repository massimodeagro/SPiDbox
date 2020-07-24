# 3D printing the SPiDbox

This folder contains all the files needed to fully 3d print the system. the objects have been designed with [OpenSCAD](https://github.com/openscad/openscad).

Currently, I am working on a more aesthestically pleasing version of all the files on [FreeCAD](https://github.com/FreeCAD/FreeCAD), which will be uploaded as soon as it is usable. For now however there are still some fitting problems between the parts, the .scad files will do just fine.

**Table of Content:**

[TOC]

##Folders description
###UserInterface
This folder contains only the file `CircuitBox.scad`, which is placed at the bottom of the SPiDbox. The part has a frontal window, in which an oledSSD1306 can be fitted, and a hole, that can contain a rotary encoder. These two components are the core of the user interface. The empty space inside this part will contain the circuit, other than cables and tubings (see building guide).

###ExperimentalBox
###CameraAndPiHolder
###ExchangablePieces
##Printing Suggestions
All pieces should print fine without the need for any support. All the pieces that will get in contact with the spider should be white, meaning the `Exp_box.scad`, the `EntranceLid.scad` and the `DropDispenser.scad` (unless for some experimental reasons you decide otherwise.)

You will need to be aware of your own 3D printer capabilities, especially for the tolerances, as there are many pieces that need to fit together.
The most challenging component will be the `DropDispenser.scad`, as its legs do not represent the most stable base. Adding a brim to the print should be enough to have it print just fine on most printer.
The `DropDispenser.scad` will also have to be printed at a higher temperature to ensure high layer adesion, and with 100% infill, as it is vital that the piece comes out water tight

**++Beware:++ depending on the material you will use to print the pieces, you may need to substitute them over time. Especially the `DropDispenser.scad` will inevitably absorb humidity and may become clogged or start dripping if made in PLA. Either choose another material, or change the piece every 3 to 4 weeks.**

##Building guide
###List of components
Before you start assemblying, be sure to have printed:
* one `CircuitBox.scad` from the *UserInterface* folder
* both `Exp_box.scad` and `Exp_box_lid.scad` files from the *ExperimentalBox* folder
* the `camhold.scad` file from the *CameraAndPiHolder* folder
* at least one `EntranceLid.scad` and one `DropDispenser.scad`, plus two other pieces of your choice between `Cover.scad` and `ResistorHolder.scad` (either one of each or two copies of one of the two) from the folder *ExchangablePieces*

Moreover, you will also need to have:
* the built circuit with all its modules (see the circuit building instructions for more information)
* a peristaltic pump based on a Nema17 motor
* a second peristaltic pump based on any 5V DC motor
* a Raspberry Pi Zero
* a Raspberry Pi Camera
* flexible tubing with internal diameter of 2mm (how much you will needs depends on your own setup. A couple of meters in total should be enough for most people)
* one resistor for every `ResistorHolder.scad` you printed (but have on the side quite a lot more, they are cheap and can break easly)
* some liquid container, like falcon tubes.

Lastly, you will also need some M2 and M3 nuts and bolts, depending on the circuit board you choose. You will for sure need at least 6 short M2 bolts with their corresponding nuts, to secure the Raspberry and its camera to the printed pieces.

###Assembly


