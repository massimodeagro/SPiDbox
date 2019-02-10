include<threads.scad>

translate([0,0,12]) cylinder (d=9.8, h=5,$fn=100);
difference(){
    cylinder(d=9.8,h=12,$fn=30);
    translate([12,0,5]) sphere(d=20);
    translate([12,0,0]) cylinder(d=20,h=5, $fn=40);
    translate([-12,0,5]) sphere(d=20);
    translate([-12,0,0]) cylinder(d=20,h=5, $fn=40);
}

translate([0,9.7/2,14.2]) sphere(d=2,$fn=100); 
translate([0,-9.7/2,14.2]) sphere(d=2,$fn=100);