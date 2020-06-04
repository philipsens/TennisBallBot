// Based on the scemetics found here: https://www.instructables.com/id/Arduino-dimensionshole-patterns-and-how-to-fasten/

hole_size = 3.2; // All Arduino holes are 3.2mm
board_length = 70;
board_width = 55;
board_depth=3;
tennis_mount_length = 9;
tennis_mount_width = 35;
tennis_mount_height = 14;
tennis_mount_holes_offset = 7;

tennis_ball_handle_width = 66;

$fn=100;

module tennis_ball_mount_arm_left() {
    arm_width = 10;
    
    difference() {
        union() {
            translate([-11.5,
                33, 
                -tennis_mount_height / 2 - board_depth / 2
            ])
                rotate([0, 0, -45])
                    cube([30, arm_width, tennis_mount_height], true);
            
            translate([-48.55, 42.15, -tennis_mount_height / 2 - board_depth / 2])
                cube([60, arm_width, tennis_mount_height], true);
        }
        translate([board_depth + 0.5,
            tennis_ball_handle_width / 2 - arm_width / 2, 
            -tennis_mount_height / 2 - board_depth / 2
        ])
            cube([10, 15, tennis_mount_height], true);
    }
   
}

module tennis_ball_mount_arm_right() {
    arm_width = 10;
    
    difference() {
        union() {
            translate([-11.5,
                -33, 
                -tennis_mount_height / 2 - board_depth / 2
            ])
                rotate([0, 0, 45])
                    cube([30, arm_width, tennis_mount_height], true);
            
            translate([-48.55, -42.15, -tennis_mount_height / 2 - board_depth / 2])
                cube([60, arm_width, tennis_mount_height], true);
        }
        
        translate([ board_depth + 0.5,
            -tennis_ball_handle_width / 2 + arm_width / 2, 
            -tennis_mount_height / 2 - board_depth / 2
        ])
            cube([10, 15, tennis_mount_height], true);

    }
}

module tennis_ball_mount_bottom_plate() {
    translate([
        -tennis_mount_length /2 + board_depth / 2,
        0, 
        -tennis_mount_height / 2 - board_depth / 2])
        translate([-5, 0, -tennis_mount_height / 2 + 1.5]) 
            cube([10, 60, 3], true);
}

module tennis_ball_mount() {
    difference() {
        
        translate([
                -tennis_mount_length /2 + board_depth / 2,
                0, 
                -tennis_mount_height / 2 - board_depth / 2
            ]) union() {
                cube([board_depth, tennis_ball_handle_width, tennis_mount_height], true);
                
                translate([13 / 2, -tennis_ball_handle_width/2 + 6, -tennis_mount_height / 2 + 1.5]) 
                    difference() {
                        union() {
                            cube([10,12,3], true);
                            
                            translate([-2.5, -6 + 1.5, 4])
                                rotate([0, 0, 270])
                                support(3, 5, 5, 45);
                        
                        }
                        
                        translate([1.5, 2, 0])
                        hull() { 
                            cylinder (h = board_depth * 2, r=hole_size/2, center = true); 

                            
                            translate([-3, 0, 0])
                                cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                        }
                    }
                
                translate([13 / 2, tennis_ball_handle_width/2 - 6, -tennis_mount_height / 2 + 1.5])  
                    difference() {
                        union() {
                            cube([10,12,3], true);
                            
                            translate([-2.5, 6 - 1.5, 4])
                                rotate([0, 0, 270])
                                support(3, 5, 5, 45);
                        
                        }
                        translate([1.5, -2, 0])
                        hull() { 
                            cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                            
                            translate([-3, 0, 0])
                                cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                        }
                    }

        }

        
        // Big holes on the standing part of the mount
        translate([-tennis_mount_length / 2, tennis_mount_width/2 - tennis_mount_holes_offset , -5])
            rotate([90, 0 ,90]) 
                hull() { 
                    cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                    
                    translate([0, -5, 0])
                        cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                }
                
        translate([-tennis_mount_length / 2, -tennis_mount_width/2 + tennis_mount_holes_offset , -5])
            rotate([90, 0 ,90]) 
                hull() { 
                    cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                    
                    translate([0, -5, 0])
                        cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                }

    }

}

module pi_camera_mount() {
    camera_width = 27;
    camera_height = 21.5;
    camera_hole_size = 2.5;
    
    camera_distance_between_horizontal = 21;
    camera_distance_between_vertical = 12.5;
    
    camera_hole_offset_bottom  = 5;
    hole_start_height = camera_height / 2 - camera_hole_size / 2 - camera_hole_offset_bottom;
    
    translate([
        -tennis_mount_length /2 + board_depth / 2,
        0, 
        camera_height / 2- board_depth / 2
    ]) difference() {
        cube([3, camera_width, camera_height], true);
       
        // Hole bottom left
        rotate([0, 90, 0])
            translate([
            hole_start_height, 
            camera_distance_between_horizontal / 2, 
            0])
                cylinder (h = board_depth * 2, r=camera_hole_size/2, center = true); 
        
        // Hole bottom right
        rotate([0, 90, 0])
            translate([
            hole_start_height, 
            -camera_distance_between_horizontal / 2, 
            0])
                cylinder (h = board_depth * 2, r=camera_hole_size/2, center = true); 
        
        // Hole top left
         rotate([0, 90, 0])
            translate([
            hole_start_height - camera_distance_between_vertical, 
            camera_distance_between_horizontal / 2, 
            0])
                cylinder (h = board_depth * 2, r=camera_hole_size/2, center = true); 

        // Hole top right
         rotate([0, 90, 0])
            translate([
            hole_start_height - camera_distance_between_vertical, 
            -camera_distance_between_horizontal / 2, 
            0])
                cylinder (h = board_depth * 2, r=camera_hole_size/2, center = true); 
    }
}

module tennis_ball_handle() {
  union() {  
    tennis_ball_mount();
    tennis_ball_mount_arm_left();
    tennis_ball_mount_arm_right();
    tennis_ball_mount_bottom_plate();
    pi_camera_mount();
  }    
}

module tennis_mount() {
    difference() {
        union() {
            cube([tennis_mount_length, tennis_mount_width, board_depth], true);
            
            translate([
                -tennis_mount_length /2 + board_depth / 2,
                0, 
                -tennis_mount_height / 2 - board_depth / 2
            ])
                cube([board_depth, tennis_mount_width, tennis_mount_height], true);

            translate([0,tennis_mount_width / 2 - board_depth / 2,  -tennis_mount_height / 2 - board_depth / 2])
                rotate([0, 180, 270])
                    support(board_depth, tennis_mount_length, tennis_mount_height, 33);
            
             translate([0,-tennis_mount_width / 2 + board_depth / 2,  -tennis_mount_height / 2 - board_depth / 2])
                rotate([0, 180, 270])
                    support(board_depth, tennis_mount_length, tennis_mount_height, 33);
            
        }
        
        translate([-tennis_mount_length / 2, tennis_mount_width/2 - tennis_mount_holes_offset , -5])
            rotate([90, 0 ,90]) 
                hull() { 
                    cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                    
                    translate([0, -5, 0])
                        cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                }
                
        translate([-tennis_mount_length / 2, -tennis_mount_width/2 + tennis_mount_holes_offset , -5])
            rotate([90, 0 ,90]) 
                hull() { 
                    cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                    
                    translate([0, -5, 0])
                        cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
                }

    }
}

module support(support_depth, support_width, support_height, deg) {
    difference() {
        cube([support_depth, support_width, support_height],true);
        rotate([deg, 0, 0])
            translate([0, support_width/2, 0])
                cube([support_depth, support_width, support_height * 2],true);
    }
}

module mount(board_length, board_width, board_depth, hole_size) {
    difference() {
        hole_radius=hole_size/2;
        
        slide_length_horizontal=5;
        slide_length_vertical=5;
       
        top_left_offset_left=14 + 1.4 / 2;
        top_left_offset_top=2.5 + 1.7/2;

        top_right_offset_right=2.5 + 1.4 / 2;
        top_right_offset_top=7.6 + 1.7/2;

        bot_left_offset_left=15.3 + 1.4/2;
        bot_left_offset_bot=2.5 + 1.7/2;

        bot_right_offset_right=2.5 + 1.4/2;
        bot_right_offset_bot=17.8 + 1.7/2;
        
        union() {
            cube([board_length, board_width, board_depth], true);
            
            translate([-board_length/2 - tennis_mount_length / 2, 0, 0])
                tennis_mount();
        }
        
        // Top left hole
        translate([
            (board_length/2 - top_left_offset_left - slide_length_horizontal /2), 
            (-board_width/2 + top_left_offset_top), 
            0]
        )  hull() {
            cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
            
            translate([slide_length_horizontal, 0, 0])
                cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
        }
        
        // Top right hole
        translate([
            (-board_length/2 + top_right_offset_right), 
            (-board_width/2 + top_right_offset_top - slide_length_vertical / 2), 
            0]
        ) hull() {
            cylinder (h = board_depth * 2, r=hole_size/2, center = true);
            
            translate([0, slide_length_vertical, 0])// translate([-70,0,0])
                cylinder (h = board_depth * 2, r=hole_size/2, center = true);
        }
        
        // Bottom left hole
        translate([
            (board_length/2 - bot_left_offset_left - slide_length_horizontal /2), 
            (board_width/2 - bot_left_offset_bot), 
            0]
        ) hull() { 
            cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
            
             translate([slide_length_horizontal, 0, 0])
                cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
        }
        
        // Bottom right hole
        translate([
            (-board_length/2 + bot_right_offset_right), 
            (board_width/2 - bot_right_offset_bot - slide_length_vertical / 2), 
            0]
        ) hull() { 
            cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
            
            translate([0, slide_length_vertical, 0])
                cylinder (h = board_depth * 2, r=hole_size/2, center = true); 
        }
        
        translate([19, 10, 0])
            plus(10.1, 3.1, 3);
        
        translate([19, -10, 0])
            plus(10.1, 3.1, 3);

        translate([-19, 10, 0])
            plus(10.1, 3.1, 3);
        
        translate([-19, -10, 0])
            plus(10.1, 3.1, 3);
    }
} 

module plus(size, width, depth) {
        union() {
                cube([size, width, depth], true);
                cube([width,  size, depth], true);
        }
}

module pi_mount() {
    pi_length = 70;
    pi_width = 56;
    pi_hole_size = 3;
    
    pi_hole_bot_left_corner_x = -pi_length / 2;
    pi_hole_bot_left_corner_y = -pi_width / 2;
    
    pi_hole_top_left_corner_x = -pi_length / 2;
    pi_hole_top_left_corner_y = pi_width / 2;
    
    pi_hole_bot_right_corner_x = pi_hole_bot_left_corner_x + 58;
    pi_hole_bot_right_corner_y = -pi_width / 2;
    
    pi_hole_top_right_corner_x = pi_hole_top_left_corner_x + 58;
    pi_hole_top_right_corner_y = pi_width / 2;
    
    union() {
        translate([0, 0, 4 + board_depth/2])
            difference() {
                cube([pi_length, pi_width, board_depth], true);
               
                // Bottom left corner
                translate([pi_hole_bot_left_corner_x + 3, pi_hole_bot_left_corner_y + 3.5, 0])
                    hull() {
                        cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                        
                        translate([5, 0, 0])
                            cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                    }
                   
                // Top left corner
                translate([pi_hole_top_left_corner_x + 3, pi_hole_top_left_corner_y - 3.5, 0])
                    hull() {
                        cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                        
                        translate([5, 0, 0])
                            cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                    }
                    
                // Bottom right corner
                translate([pi_hole_bot_right_corner_x + 3, pi_hole_bot_right_corner_y + 3.5, 0])
                    hull() {
                        cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                        
                        translate([5, 0, 0])
                            cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                    }
                    
                // Top right corner
                translate([pi_hole_top_right_corner_x + 3, pi_hole_top_right_corner_y - 3.5, 0])
                    hull() {
                        cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                        
                        translate([5, 0, 0])
                            cylinder (h = board_depth * 2, r=pi_hole_size/2, center = true); 
                    }
            }
        
        translate([19, 10, 0])
            plus(10, 3, 8);
            
        translate([19, -10, 0])
            plus(10, 3, 8);

        translate([-19, 10, 0])
            plus(10, 3, 8);
            
        translate([-19, -10, 0])
            plus(10, 3, 8);
    }
}

color("blue",  alpha=1)  {
    mount(board_length, board_width, board_depth, hole_size);
}

color("red", alpha=1) {
    translate([
        -board_length / 2 - tennis_mount_length - 1.5,
        0, 
        0
    ])
        tennis_ball_handle();
}

color("yellow", alpha=1) {
    translate([0, 0, 10])
        pi_mount();
}

// translate([-70,0,0])
//    cube([10, 74, 10], true);
