include<threads.scad>

difference(){
    union(){
    translate([0,0,12]) cylinder (d=9.6,h=7,$fn=100);
        difference(){
    cylinder(d=9.6,h=12,$fn=100);
            translate([0,12,5]) sphere(d=20,$fn=100);
    translate([0,12,0]) cylinder(d=20,h=5, $fn=100);
    translate([0,-12,5]) sphere(d=20,$fn=100);
    translate([0,-12,0]) cylinder(d=20,h=5, $fn=100);
        }
        
    }

   
    translate([0,0,16]) union(){ 
       intersection(){
            cylinder(d=5.5,h=3,$fn=100);
            translate([-2.75,-2.25]) cube([5.5,4.5,3]);
        }
    
        translate([-1.5,0,-18]) cylinder(d=2.5,h=20,$fn=100);
        translate([1.5,0,-18]) cylinder(d=2.5,h=20,$fn=100);
        
    }
 
}

translate([9.6/2,0,14.5]) sphere(d=2,$fn=100); 
translate([-9.6/2,0,14.5]) sphere(d=2,$fn=100);
