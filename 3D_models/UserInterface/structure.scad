use<parts/oledSSD1306.scad>
use <parts/pcb.scad>

module holding() {
difference(){
cube([110,10,10]);
rotate([-45,0,0]) cube([110,10,15]);
}
}

module pins(){
for (n=[0:19]){
    translate([2.54*3,2.54*(12.5-n),3])rotate([180,0,0])pinfemale();
    translate([2.54*-3,2.54*(12.5-n),3])rotate([180,0,0])pinfemale();
}
}

module holdings(){
    translate([-5,2,135]) holding();
translate([103,0,135]) rotate([0,0,90]) holding();
translate([-3,110,135]) rotate([0,0,-90]) holding();
translate([105,108,135]) rotate([0,0,180]) holding();
}

module oledholes(){
        translate([28/2-2.1,27.5/2-2.1]) cylinder(d=2.5,h=5,$fn=30);
        translate([-28/2+2.1,-27.5/2+2.1]) cylinder(d=2.5,h=5,$fn=30);
        translate([-28/2+2.1,27.5/2-2.1]) cylinder(d=2.5,h=5,$fn=30);
        translate([28/2-2.1,-27.5/2+2.1]) cylinder(d=2.5,h=5,$fn=30);
}

module oledperns(){
        translate([28/2-2.1,27.5/2-2.1]) cylinder(d=4,h=4,$fn=30);
        translate([-28/2+2.1,-27.5/2+2.1]) cylinder(d=4,h=4,$fn=30);
        translate([-28/2+2.1,27.5/2-2.1]) cylinder(d=4,h=4,$fn=30);
        translate([28/2-2.1,-27.5/2+2.1]) cylinder(d=4,h=4,$fn=30);
}

module pcbholes(){
        translate([-41.75,33.24,-0.7]) cylinder(d=3,h=20,$fn=30);
     translate([41.75,33.24,-0.7]) cylinder(d=3,h=20,$fn=30);
     translate([-41.75,-33.24,-0.7]) cylinder(d=3,h=20,$fn=30);
     translate([41.75,-33.24,-0.7]) cylinder(d=3,h=20,$fn=30);
}

module pcbperns(){
        translate([-41.75,33.24,-0.7]) cylinder(d1=10,d2=5,h=5,$fn=30);
     translate([41.75,33.24,-0.7]) cylinder(d1=10,d2=5,h=5,$fn=30);
     translate([-41.75,-33.24,-0.7]) cylinder(d1=10,d2=5,h=5,$fn=30);
     translate([41.75,-33.24,-0.7]) cylinder(d1=10,d2=5,h=5,$fn=30);
}

module box(){
    translate([-50,-55,0]) holdings();
    difference(){
     difference(){
             union(){
        linear_extrude(height=150)    square([110,110],center=true);
                 hull(){
                 linear_extrude(height=10)    square([110,110],center=true);
                    linear_extrude(height=0.1)    square([130,130],center=true);
                     }
                     

             }
                 translate([0,0,-1]) linear_extrude(height=202) square([106,106],center=true);

    
translate([0,0,120]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
translate([0,25,120]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
translate([0,-25,120]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
             
translate([0,12.5,95]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
translate([0,-12.5,95]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
translate([0,-37.5,95]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
translate([0,37.5,95]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
             

translate([0,0,70]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
translate([0,25,70]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
translate([0,-25,70]) rotate([0,90,0]) cylinder(d=20,h=200,center=true);
             
translate([12.5,100,30]) rotate([90,0,0]) cylinder(d=20,h=100);
translate([-12.5,100,30]) rotate([90,0,0]) cylinder(d=20,h=100);
translate([-37.5,100,30]) rotate([90,0,0]) cylinder(d=20,h=100);
translate([37.5,100,30]) rotate([90,0,0]) cylinder(d=20,h=100);  
 }
        translate([26,-52,70]) rotate([90,0,0])cylinder(d=8,h=5,$fn=30);
         
         translate([0,-51,70]) rotate([90,0,0]) oledholes();

         translate([0,-51,72.5]) rotate([90,0,0]) linear_extrude(height=9) square([28,14.5],center=true);
   
}
    }


//translate([0,-50,30]) rotate([90,0,0]) SSD1306(1);
//translate([0,48,145]) rotate([90,0,0]) pcb();
//translate([0,48,145]) rotate([90,0,0]) pins();
difference(){
union(){
box();
    
translate([-54,-55,20])scale([0.7,0.7,0.7]) color("red")
   rotate([90,0,0])
   minkowski(){
    linear_extrude(height=0.1)import ("spidereyes.dxf");
       sphere(d=2);
   }
   
translate([-35,50,90]) rotate([0,90,90]) perns7x3();
translate([35,50,90]) rotate([0,90,90]) perns7x3();
   
translate([0,50,90]) rotate([0,90,90]) perns8x2(); 
   translate([50,0,35]) rotate([90,0,90]) perns6x4(); 
  
}  
translate([-35,50,90]) rotate([0,90,90]) holes7x3();
translate([35,50,90]) rotate([0,90,90]) holes7x3();
   
translate([0,50,90]) rotate([0,90,90]) holes8x2(); 
   translate([50,0,35]) rotate([90,0,90]) holes6x4();
   }
   
//   
//      
//translate([-35,50,90]) rotate([0,90,90]) pcb7x3();
//translate([35,50,90]) rotate([0,90,90]) pcb7x3();
//   
//translate([0,50,90]) rotate([0,90,90]) pcb8x2();   
//
//translate([50,0,40]) rotate([90,0,90]) pcb6x4();    