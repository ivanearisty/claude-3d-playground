$fn=128;
radius=150;      // radius of the shelf
thickness=5;    // thickness of the in mm 
previs=thickness+5; // this is the front side of the shelf (let's make it a bit bigger) - default value should be OK
support_l=40;   // length of support for screw in mm
screw_d=4.2;      // screw hole diameter in mm
support_thickness=5;        // thickness of the "leg" (default value is usually OK)
support_width=screw_d+10; //  width of the "leg" (defined as screw hole + 10mm)
corner_hole=10;             // radius of corner hole (for cables etc.)
angle=90;             // shelf angle. Default is 90 degrees  

min_angle=10;       // minimal value for angle
max_angle=180;      // maximum value for angle

assert(angle >= min_angle && angle <= max_angle, "Angle out of allowed range 10-180!");

// main code
//rotate([0,180,0])
difference() {
    union() {
     shelf(radius,thickness,previs,angle);
    
     translate([radius/2+support_width/2,0,thickness]) rotate([90,0,180]) 
      support(support_l,screw_d,support_width,support_thickness);
    
    rotate([0,0,angle-90])
     translate([0,radius/2-support_width/2,thickness]) 
      rotate([90,0,90]) 
       support(support_l,screw_d,support_width,support_thickness);
    }
    translate([0,0,-0.1])
    cylinder(r=corner_hole,h=thickness+0.2); // corner hole
}
    

module shelf(radius,thickness,previs,angle) {
difference() {
  cylinder(r=radius,h=previs);
  translate([0,0,thickness]) cylinder(r=radius-thickness,h=thickness+100);
  rotate([0,0,angle-90])
    translate([-radius-0.1,-radius-0.1,-0.1]) 
     cube([radius+0.1,radius*2+0.1,thickness+previs+0.2]);
  translate([-radius-0.1,-radius,-0.1]) cube([radius*2+0.2,radius,thickness+previs+0.2]);
 }
}

module support(support_l,screw_d,support_width,support_thickness) {
    difference() {
     union() {
      cube([support_width,support_l-support_width/2,support_thickness]);
      translate([support_width/2,support_l-support_width/2,0]) cylinder(d=support_width,h=support_thickness);
     }
     translate([support_width/2,support_l*0.75,-0.1]) cylinder(d=screw_d,h=support_thickness+0.2);
    }
    
    difference() {
    translate([0,0,support_thickness]) 
    cube([support_width,support_l*0.70,support_l*0.70]);
      translate([-0.1,support_l*0.70,support_thickness+support_l*0.70])
        rotate([0,90,0])  
         cylinder(r=support_l*0.70,h=support_width+0.2);
    }
}