include <threads.scad>

 module adapter(){
 difference(){
    union(){
        //translate([0,0,8]) cylinder(d2=6,d1=4,h=1.5, $fn=30);
        translate([0,0,9.5]){
            cylinder(d=4,h=5.5, $fn=30);
            cylinder(d2=4,d1=5.5,h=3, $fn=30);
        }
        cylinder(d=4.3,h=10, $fn=30);

    }
    translate([0,0,-30]) cylinder(d=1.5,h=50, $fn=30);
}
}

module key(){
    difference(){
    cylinder(d1=13, d2=9.8,h=12,$fn=30);
    translate([13,0,2]) sphere(d=20);
    translate([13,0,0]) cylinder(d=20,h=2, $fn=40);
    translate([-13,0,2]) sphere(d=20);
    translate([-13,0,0]) cylinder(d=20,h=2, $fn=40);
}
}

difference(){
    union(){
        difference(){
                union(){
                    translate([0,0,12]) cylinder (d=9.8, h=5,$fn=100);
                    key();

                }
                
            translate([0,0,2]) cylinder(d2=1.5,d1=1.5,h=9,$fn=20); 
            translate([0,0,11]) cylinder(d1=1.5,d2=3,h=6,$fn=50);
            //rotate([0,-2,0]) translate([3.9,0,-5]) cylinder(d=1.5,h=30,$fn=20);
            translate ([0,4.5,2.3]) rotate([90,0,0]) cylinder(d=3,h=9,$fn=30);
            translate ([0,4,-1]) cylinder(d=1.5,h=3,$fn=30);
            translate ([0,-4,-1]) cylinder(d=1.5,h=3,$fn=30);
        }

        translate([0,4,0]) rotate([180,0,0]) adapter();
        translate([0,-4,0]) rotate([180,0,0]) adapter();
        difference(){
            union(){
            translate([0,-4,-5]) rotate([-11.6,0,0]) cylinder(d1=4,d2=8,h=6,$fn=30);
            translate([0,4,-5]) rotate([11.6,0,0]) cylinder(d1=4,d2=8,h=6,$fn=30);
            }
                      
        difference(){
        cylinder(d=20, h=20);
            key();
        }
    }
    }
     translate ([0,4,-20]) cylinder(d=1.5,h=22,$fn=30);
     translate ([0,-4,-20]) cylinder(d=1.5,h=22,$fn=30);
    translate([0,0,20]) cylinder(d=70,h=20);
    

//translate([0,0,7]) cylinder(d=200,h=20);
}

translate([0,9.7/2,14.2]) sphere(d=2,$fn=100); 
translate([0,-9.7/2,14.2]) sphere(d=2,$fn=100);


