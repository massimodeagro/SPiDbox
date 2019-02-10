module epaper(){
color("SteelBlue") linear_extrude(height=2) difference(){
square([89.50,38],center=true);
translate([89.5/2-2.5,38/2-2.5]) circle(d=3,$fn=20);
translate([-89.5/2+2.5,-38/2+2.5]) circle(d=3,$fn=20);
translate([-89.5/2+2.5,38/2-2.5]) circle(d=3,$fn=20);
translate([89.5/2-2.5,-38/2+2.5]) circle(d=3,$fn=20);
}

translate([0,0,2]){ 
color("Silver") linear_extrude(height=0.7) square([79,36.7],center=true);
color("Gainsboro") linear_extrude(height=1.05) translate([3.075,0,0]) square([66.85,29.1],center=true);
}
}

module epaperscreen(){
color("Gainsboro") linear_extrude(height=10) translate([3.075,0,0]) square([66,28],center=true);
}

module epaperholes(){
linear_extrude(height=5){
translate([89.5/2-2.5,38/2-2.5]) circle(d=3,$fn=20);
translate([-89.5/2+2.5,-38/2+2.5]) circle(d=3,$fn=20);
translate([-89.5/2+2.5,38/2-2.5]) circle(d=3,$fn=20);
translate([89.5/2-2.5,-38/2+2.5]) circle(d=3,$fn=20);
}
}

module epapernut(){
linear_extrude(height=5){
translate([89.5/2-2.5,38/2-2.5]) rotate([0,0,90]) circle(d=5.2,$fn=6);
translate([-89.5/2+2.5,-38/2+2.5]) rotate([0,0,90])circle(d=5.5,$fn=6);
translate([-89.5/2+2.5,38/2-2.5]) rotate([0,0,90])circle(d=5.2,$fn=6);
translate([89.5/2-2.5,-38/2+2.5]) rotate([0,0,90])circle(d=5.2,$fn=6);
}
}