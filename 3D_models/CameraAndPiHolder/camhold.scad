module leg(){
    cube([3,10,140]);
    cube([10,3,140]);
}

module camback(){
    color("blue") translate([-14.9,-12,0]) import("camera_back.STL");
}

module raspholeint(){
    translate([-29,-11.5,0])
    cylinder(h=15,d=3,$fn=30);
    translate([29,-11.5,0])
    cylinder(h=15,d=3,$fn=30);
    translate([-29,11.5,0])
    cylinder(h=15,d=3,$fn=30);
    translate([29,11.5,0])
    cylinder(h=15,d=3,$fn=30);
}
//translate([-14.9,-12,0]) import("camera_front.STL");


camback();
    translate([-45,-45,0]) leg();
    translate([45,-45,0]) rotate([0,0,90]) leg();
    translate([45,45,0])rotate([0,0,180]) leg();
    translate([-45,45,0]) rotate([0,0,-90]) leg();

linear_extrude(height=2) difference(){
square([90,90],center=true);
polygon(points=[[-35,-40],[35,-40],[8,-12],[-8,-12]]);
    rotate([0,0,90]) polygon(points=[[-35,-40],[35,-40],[8,-12],[-8,-12]]);
    rotate([0,0,180]) polygon(points=[[-35,-40],[35,-40],[8,-12],[-8,-12]]);
    rotate([0,0,270]) polygon(points=[[-35,-40],[35,-40],[8,-12],[-8,-12]]);


}

translate([-45,-45,4]) rotate([0,37,0]) cube([5,2,140]);
translate([45,-45,4]) rotate([0,37,90]) cube([5,2,140]);
translate([45,45,4]) rotate([0,37,180]) cube([5,2,140]);
translate([-45,45,4]) rotate([0,37,270]) cube([5,2,140]);

translate([40,-45,4]) rotate([0,-37,0]) cube([5,2,140]);
translate([+45,+40,4]) rotate([0,-37,90]) cube([5,2,140]);
translate([-40,45,4]) rotate([0,-37,180]) cube([5,2,140]);
translate([-45,-40,4]) rotate([0,-37,270]) cube([5,2,140]);

translate([0,-88,-00]) difference(){
    translate([-45,45-2,35]) cube([90,2,70]);

translate ([0,50,70]) rotate([90,90,0]) raspholeint();
}

