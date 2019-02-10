
module leg(){
    cube([4,11,11]);
    cube([11,4,11]);
}

difference(){
difference(){
    translate([0,0,5]) cube([95,95,16],center=true);
    cube([89,89,7],center=true); 
    color("red")translate([0,0,4]) cube([80,80,50], center=true);
    translate([-45.5,-45.5,4]) leg();
    translate([45.5,-45.5,4]) rotate([0,0,90]) leg();
    translate([45.5,45.5,4]) rotate([0,0,180]) leg();
    translate([-45.5,45.5,4]) rotate([0,0,-90]) leg();
}

translate([0,49,10]) rotate([22,0,0]) cube([65,10,30],center=true);
rotate([0,0,90]) translate([0,49,10]) rotate([22,0,0]) cube([65,10,30],center=true);
rotate([0,0,180]) translate([0,49,10]) rotate([22,0,0]) cube([65,10,30],center=true);
rotate([0,0,270]) translate([0,49,10]) rotate([22,0,0]) cube([65,10,30],center=true);
}

