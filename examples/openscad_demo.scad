// Example: Parametric rounded box in OpenSCAD
// Render with: openscad -o models/stl/rounded_box.stl examples/openscad_demo.scad

width = 50;
depth = 30;
height = 20;
corner_radius = 3;

module rounded_box(w, d, h, r) {
    minkowski() {
        cube([w - 2*r, d - 2*r, h/2], center=true);
        cylinder(r=r, h=h/2, $fn=32);
    }
}

rounded_box(width, depth, height, corner_radius);
