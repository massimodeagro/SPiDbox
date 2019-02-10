include <clip.scad>
include <e-paper2.9.scad>


difference(){
    union(){ //ll the box body
        translate([7,0,0])cube([70,84,48]); //overall box
        hull(){ 
            translate([-2,-2,43]) cube([88,88,5]); //lid holder
            translate([0,0,41]) cube([84,84,7]);
        }
        hull(){
         translate([42,-4,13]) rotate([270,0,0]) cylinder(d1=18,d2=22,h=4); //spider access
            translate([42,-2,1]) cube([22,4,1],center=true);
        }   
    }
    
    
    
    translate([9,2,5]) cube([66,80,70]); //box hole
    translate([0,0,45]) cube([84,84,7]); //lid hole

    translate([42,-0,13]) rotate([270,0,0]) guides(16); //enter hole
    
    //3 holders
    translate([42,75,2.5]) guides();
    translate([22,75,2.5]) guides();
    translate([62,75,2.5]) guides();
//    translate([22,60,2.5]) guides();
//    translate([62,60,2.5]) guides();

   translate([42-3.075,88,19]) rotate([90,0,0]) epaperscreen(); // hole for screen
}


difference(){
    union(){       
        difference(){
            translate([-10,-10,0]) cube([104,104,2]); //box base
            translate([5,89,0]) rotate([0,0,65]) cube([150,25,7],center=true); // angle cut 1
            translate([78,89,0]) rotate([0,0,-65]) cube([150,25,7],center=true); //angle cut 2
        }
        
        translate([-10,77,0]) cube([104,10,5]); //back base
        hull(){ //screen holder back R
            translate([-7,77,0]) cube([14,7,38]);   
            translate([5,77,38]) cube([4,7,4]);
        }
        translate([77,77,0]) cube([8,7,45]);   //screen holder back L
    }

    translate([42-3.075,89,0]) cube([150,10,30],center=true); //remove the back

    translate([42-3.075,84,19]) rotate([90,0,0]) epaperholes();
    translate([42-3.075,81,19]) rotate([90,0,0]) epaperholes();

    translate([9,2,5]) cube([66,80,70]); // boxhole

    translate([42,75,2.5]) guides();
    translate([22,75,2.5]) guides();
    translate([62,75,2.5]) guides();
}

//translate([42-3.075,87,19]) rotate([90,0,0]) epaper();

hull(){ //oblique
    translate([0,0,41]) cube([7,84,1]);
    translate([7,0,34]) cube([0.1,84,1]);
}
hull(){ //oblique
    translate([77,0,41]) cube([7,84,1]);
    translate([77,0,34]) cube([0.1,84,1]);
}

//support material
translate([42-3.075,82,5.4]) cube([5,2,27.2]);
translate([20,82,5.4]) cube([5,2,27.2]);
translate([62-3.075,82,5.4]) cube([5,2,27.2]);

difference(){
    union(){ //two covers
        translate([-7,77,0]) cube([6,8,38]);   
        translate([79,77,0]) cube([6,8,45]);   
    }
    translate([42-3.075,87,19]) rotate([90,0,0]) epaperholes();
    translate([42-3.075,84,19]) rotate([90,0,0]) epaperholes();
    translate([42-3.075,82,19]) rotate([90,0,0]) epaperholes();
    
    translate([40,85,19]) cube([100,2,26],center=true);   

}