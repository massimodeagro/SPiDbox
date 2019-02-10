include<threads.scad>

translate([0,0,12]) cylinder (d=15.5, h=4.2,$fn=100);
difference(){
    translate([0,0,6]) cylinder(d=15.5,h=6,$fn=30);
    translate([12,0,3]) sphere(d=20);
    translate([12,0,0]) cylinder(d=20,h=5, $fn=40);
    translate([-12,0,3]) sphere(d=20);
    translate([-12,0,0]) cylinder(d=20,h=5, $fn=40);
}

translate([0,15.5/2,14.2]) sphere(d=2,$fn=100); 
translate([0,-15.5/2,14.2]) sphere(d=2,$fn=100);