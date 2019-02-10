module guides(d=10){
    translate([0,0,-5])cylinder(d=d,h=10,$fn=50);
difference(){
rotate_extrude(angle=90,$fn=50) translate([d/2,0]) circle(d=2,$fn=50);
rotate([0,0,10]) translate([d/2+0.7,0,-1.7]) sphere(d=2,$fn=50);

}
   
hull(){
translate([0,d/2,0]) sphere(d=2,$fn=50); 
translate([0,d/2,-5]) sphere(d=2,$fn=50); 
}

translate([d/2,0,0]) sphere(d=2,$fn=50); 

difference(){
rotate([0,0,180]) rotate_extrude(angle=90,$fn=50) translate([d/2,0]) circle(d=2,$fn=50);
rotate([0,0,10]) translate([-(d/2+0.7),0,-1.7]) sphere(d=2,$fn=50);  
}
hull(){
translate([0,-d/2,0]) sphere(d=2,$fn=50);
translate([0,-d/2,-3]) sphere(d=2,$fn=50); 
}

translate([-d/2,0,0]) sphere(d=2,$fn=50); 


}
//
//translate([0,0,2]) difference(){
//    difference(){
//        cylinder(d=20,h=4,$fn=50);
//        translate([0,0,-1])cylinder(d=10,h=6,$fn=50);
//    }
//    translate([0,0,2.3]) guides();
//}
//
//cylinder(d=9.5,h=6,$fn=50);
//translate([4.75,0,4]) sphere(d=1.8,$fn=50); 
//translate([-4.75,0,4]) sphere(d=1.8,$fn=50); 
//
//

