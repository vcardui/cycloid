# ------------ Authors -------------
# Vanessa Reteguín
# Martín Isaí Núñez
# Paola Osorio
# Alexis Zúñiga


# ------------ Resources / Documentation involved -------------
# Manim Community https://docs.manim.community/en/stable/

# ------------------------- Libraries -------------------------
from manim import *

# ------------------------- Variables -------------------------
# Circle's radius
redRadius = 2
greenRadius = 1
blueRadius = 4

scaleFactor = 0.5 # Resize to fit in plane

# -------------------------- Classes --------------------------
class Trayectory(MovingCameraScene):
    def construct(self):
        # Create axes with adjusted y-range
        axes = Axes(
            x_range=[-6, 6, 1],  # X-axis range
            y_range=[-4, 4, 1],  # Y-axis range
            tips=False,
            axis_config={"color": BLUE, "include_numbers": True},
        )

        labels = axes.get_axis_labels(
            x_label="x", y_label="y"
        )

        self.add(axes, labels)
        
        # Circles
        redCircle = Circle(radius=redRadius*scaleFactor, color=RED, stroke_width=2)
        greenCircle = Circle(radius=greenRadius*scaleFactor, color=GREEN, stroke_width=2)
        blueCircle = Circle(radius=blueRadius*scaleFactor, color=BLUE, stroke_width=2)
        
        # Initial positions
        blueCircle.move_to([0, 0, 0])
        redCircle.move_to([0, 0, 0])
        greenCircle.move_to([0, 0, 0])
        
        # Creación de los puntos
        redCircle_dot = Dot(color=RED)
        greenCircle_dot = Dot(color=GREEN)
        blueCircle_dot = Dot(color=BLUE)

        # Red Dot (0,-2)
        redCircle_dot.move_to([0, -redRadius*scaleFactor, 0])
        # Green Dot (0,-1)
        greenCircle_dot.move_to([0, -greenRadius*scaleFactor, 0])
        # Blue Dot (0,-4)
        blueCircle_dot.move_to([0, -blueRadius*scaleFactor, 0])
        
        
        # Initial positon labels
        redCircle_dot_label = Text(f"(0,-{redRadius})", font_size=24, color=RED).next_to(redCircle_dot, RIGHT)
        greenCircle_dot_label = Text(f"(0,-{greenRadius})", font_size=24, color=GREEN).next_to(greenCircle_dot, RIGHT)
        blueCircle_dot_label = Text(f"(0,-{blueRadius})", font_size=24, color=BLUE).next_to(blueCircle_dot, DOWN)
        initialLabels = VGroup(redCircle_dot_label, greenCircle_dot_label, blueCircle_dot_label)
        
        self.add(redCircle, blueCircle, redCircle_dot, blueCircle_dot, greenCircle_dot, initialLabels)
        
        # Zoom de la cámara
        self.camera.frame.scale(1)
        
        # Point's Strokes
        redCircle_dot_trace = TracedPath(redCircle_dot.get_center, stroke_color=RED, stroke_width=3)
        greenCircle_dot_trace = TracedPath(greenCircle_dot.get_center, stroke_color=GREEN, stroke_width=3)
        blueCircle_dot_trace = TracedPath(blueCircle_dot.get_center, stroke_color=BLUE, stroke_width=3)
        self.add(redCircle_dot_trace, greenCircle_dot_trace, blueCircle_dot_trace,)
        
        self.wait(5)

        # Center point between the circles for tracking
        center_point = [0, 0, 0]
        
        # Animation duration
        duration = 30
        
        # Rotation speed (radians per second)
        rotation_speed = -1  # Clockwise (negative)
        
        # Movement speed (units per second)
        movement_speed = 0.8
        
        # Define a VGroup object to update points and circles together
        allObjects = VGroup(redCircle, greenCircle, blueCircle, redCircle_dot, greenCircle_dot, blueCircle_dot)
        
        # Function to update the positions of circles and points
        def update_all_objects(mob, dt):
            nonlocal rotation_speed, movement_speed, center_point
            
            # Move circles to the right
            displacement = RIGHT * movement_speed * dt
            redCircle.shift(displacement)
            greenCircle.shift(displacement)
            blueCircle.shift(displacement)
            
            # Actualizar el punto central
            center_point[0] += movement_speed * dt
            
            # Updated centers
            redCenter = redCircle.get_center()
            greenCenter = greenCircle.get_center()
            blueCenter = blueCircle.get_center()
            
            # Rotate circles on their own axis
            redCircle.rotate(rotation_speed * dt, about_point=redCenter)
            greenCircle.rotate(rotation_speed * dt, about_point=greenCenter)
            blueCircle.rotate(rotation_speed * dt, about_point=blueCenter)
            
            # Update the position of the points
            # Calculate the current angle (clockwise)
            angle = self.renderer.time * rotation_speed
            
            # Small circle point (clockwise)
            redCircle_dot.move_to([
                redCenter[0] + (redRadius*scaleFactor) * np.sin(angle),
                redCenter[1] - (redRadius*scaleFactor) * np.cos(angle),  # The negative sign here ensures clockwise rotation
                0
            ])
            
            # Point of the great circle (clockwise)
            blueCircle_dot.move_to([
                blueCenter[0] + (blueRadius*scaleFactor) * np.sin(angle),
                blueCenter[1] - (blueRadius*scaleFactor) * np.cos(angle),  # Changed to - for clockwise
                0
            ])
            
            # Point of the great circle (clockwise)
            greenCircle_dot.move_to([
                greenCenter[0] + (greenRadius*scaleFactor) * np.sin(angle),
                greenCenter[1] - (greenRadius*scaleFactor) * np.cos(angle),  # Changed to - for clockwise
                0
            ])
            
            # Update camera position to follow circles
            self.camera.frame.move_to(center_point)
        
        # We remove the initial tags after a brief moment
        self.play(FadeOut(initialLabels), run_time=2)
        
        # Add updater
        allObjects.add_updater(update_all_objects)
        self.add(allObjects)
        
        # Wait while the animation runs using the updater
        self.wait(duration)
        
        # Remove updater
        allObjects.remove_updater(update_all_objects)
        
        # Wait before exiting
        self.wait(1)