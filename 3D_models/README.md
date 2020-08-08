# 3D printing the SPiDbox

This folder contains all the files needed to fully 3d print the system. the objects have been designed with [OpenSCAD](https://github.com/openscad/openscad).

Currently, I am working on a more aesthestically pleasing version of all the files on [FreeCAD](https://github.com/FreeCAD/FreeCAD), which will be uploaded as soon as it is usable. For now however there are still some fitting problems between the parts, the .scad files will do just fine.

**Table of Content:**


## Folders description

### UserInterface

This folder contains only the file `CircuitBox.scad`, which is placed at the bottom of the SPiDbox. The part has a frontal window, in which an oledSSD1306 can be fitted, and a hole, that can contain a rotary encoder. These two components are the core of the user interface. The empty space inside this part will contain the circuit, other than cables and tubings (see building guide).

### ExperimentalBox

From this folder you will need to print `Exp_box.scad` and `Exp_box_lid.scad`. The other files are imported into the first two for construction. These need to be printed in white, as they will be seen by the spider. You will only need one copy of each.

### CameraAndPiHolder

From this folder you will need to print one copy of `camhold.scad`. The two stl files are imported into the .scad to construct the camera enclosure. These two stls have been downloaded from https://www.thingiverse.com/thing:92208. 
Depending on where you buy the camera and depending on its version, it may not fit inside the holder enclosure. If that is the case, you will need to modify slightly that section, either in the file or manually once printed.

### ExchangablePieces

These files represent the exchangable parts and actuators for the box. You will need at least one `EntranceLid.scad` (that coloses the round opening on the front wall of the `Exp_box.scad`), and one `DropDispenser.scad`. `ResistorHolder.scad` is the case for the photo-resistor, you will need to print one for each sensor you want to use. `Cover.scad` is used to plug the unused holes left.

## Printing Suggestions

All pieces should print fine without the need for any support. All the pieces that will get in contact with the spider should be white, meaning the `Exp_box.scad`, the `EntranceLid.scad` and the `DropDispenser.scad` (unless for some experimental reasons you decide otherwise.)

You will need to be aware of your own 3D printer capabilities, especially for the tolerances, as there are many pieces that need to fit together.
The most challenging component will be the `DropDispenser.scad`, as its legs do not represent the most stable base. Adding a brim to the print should be enough to have it print just fine on most printer.
The `DropDispenser.scad` will also have to be printed at a higher temperature to ensure high layer adesion, and with 100% infill, as it is vital that the piece comes out water tight

**_Beware:_ depending on the material you will use to print the pieces, you may need to substitute them over time. Especially the `DropDispenser.scad` will inevitably absorb humidity and may become clogged or start dripping if made in PLA. Either choose another material, or change the piece every 3 to 4 weeks.**

## Building guide

### List of components

Before you start assemblying, be sure to have printed:
* one `CircuitBox.scad` from the *UserInterface* folder
* both `Exp_box.scad` and `Exp_box_lid.scad` files from the *ExperimentalBox* folder
* the `camhold.scad` file from the *CameraAndPiHolder* folder
* at least one `EntranceLid.scad` and one `DropDispenser.scad`, plus two other pieces of your choice between `Cover.scad` and `ResistorHolder.scad` (either one of each or two copies of one of the two) from the folder *ExchangablePieces*

Moreover, you will also need to have:
* the built circuit with all its modules (see the circuit building instructions for more information)
* the OledSSD1306
* a rotary encoder
* a peristaltic pump based on a Nema17 motor
* a second peristaltic pump based on any 5V DC motor
* a Raspberry Pi Zero
* a Raspberry Pi Camera
* flexible tubing with internal diameter of 2mm (how much you will needs depends on your own setup. A couple of meters in total should be enough for most people)
* one photo-resistor for every `ResistorHolder.scad` you printed (but have on the side quite a lot more, they are cheap and can break easly)
* some liquid container, like falcon tubes.
* a square piece of plexiglas

Lastly, you will also need some M2 and M3 nuts and bolts, depending on the circuit board you choose. You will for sure need at least 6 short M2 bolts with their corresponding nuts, to secure the Raspberry and its camera to the printed pieces.

### Assembly

_pictures coming_

1. Screw the Raspberry Pi Zero to the back of `camhold.scad`
  The camera connector on the Raspberry **needs to be oriented towards the top**
2. Insert the camera in its enclosure with the ribbon cable already connected, as it will not be accessible anymore once the camera enclosure is assembled
3. Connect the ribbon cable to the Raspberry Pi
4. Screw the circuit board inside the `CircuitBox.scad`, on the back wall
5. Screw the Oled Screen in the front wall of the `CircuitBox.scad` from the inside
6. Insert the rotary encoder in the hole on the front wall of the `CircuitBox.scad` and screw it in place
7. Place both the DC and the stepper peristaltic pumps near the `CircuitBox.scad`, and insert their cables from the side holes in the circuitbox. Connect each one to its designated connector.
8. Fit the output tube of the stepper pump and the imput tube of the DC pump inside the `CircuitBox.scad` from the same holes.
9. Connect these two tubes to the two couplers of the `DropDispenser.scad`. You should now have the drop dispenser _inside_ the `CircuitBox.scad`
10. Fit a resistor inside every `ResistorHolder.scad` you printed. Solder to the two legs of the resistor coming out to cables, and connect them to their designated connector on the circuit board. You should now have also the `ResistorHolder.scad` inside the `CircuitBox.scad`
11. Fit the `ResistorHolder.scad` and the `DropDispenser.scad` in their designated holes from the bottom of the `Exp_box.scad`. these pieces can be fit and then rotated 90° to click in place.
12. Lay the `Exp_box.scad` on top of the `CircuitBox.scad`
13. Put a rectangle of plexiglas on top of the `Exp_box.scad`. The plexiglas piece should fit inside the designated groove on top of the `Exp_box.scad`.
14. Place the `Exp_box_lid.scad` on top. It should stop the plexiglas in place.
15. Put the `camhold.scad` on top of the `Exp_box_lid.scad`. Its legs should fit in the 4 holes of the `Exp_box_lid.scad`
16. Connect the raspberry to the circuit board
17. Connect the raspberry to power
