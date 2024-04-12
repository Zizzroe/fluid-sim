import pygame
import fluid_square
from fluid_square import fluidSquareCreate
from fluid_square import N, scale
import fluid_bounds

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen_size = (N * scale, N * scale)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Fluid Simulation")

# Create the fluid object
fluid = fluidSquareCreate(N, 0.1, 0, 0)

# Initialize pmouseX and pmouseY to the initial mouse position
pmouseX, pmouseY = pygame.mouse.get_pos()

# Function to add density and velocity to the fluid at the mouse position
def add_density_and_velocity(x, y):
    global pmouseX, pmouseY  # Declare pmouseX and pmouseY as global variables
    # Scale down the mouse coordinates
    x_scaled = int(x / scale)
    y_scaled = int(y / scale)
    
    amtx = x - pmouseX
    amty = y - pmouseY
    pmouseX, pmouseY = x, y
        
    fluid.fluidSquareAddDensity(x_scaled, y_scaled, 100)
        
    fluid.fluidSquareAddVelocity(x_scaled, y_scaled, amtx, amty)

# Main loop
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # Check if the left mouse button is pressed
            if pygame.mouse.get_pressed()[0]:
                # Get the current mouse position
                mouseX, mouseY = pygame.mouse.get_pos()
                # Add density and velocity to the fluid at the mouse position
                add_density_and_velocity(mouseX, mouseY)

    # Fill the screen with white
    screen.fill((255, 255, 255))
    
    # Render the fluid simulation
    fluid.render(screen)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame when the main loop exits
pygame.quit()

