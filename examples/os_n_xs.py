import time
import math
import badger2040
import badger_os

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# Function to render the game screen
def draw():
    display.set_pen(15)  # White background
    display.clear()

    # Draw the game grid with thicker lines
    display.set_pen(0)  # Black pen
    for i in range(-1, 2):  # Simulate line thickness
        display.line(103 + i, 49, 193 + i, 49)
        display.line(103 + i, 79, 193 + i, 79)
        display.line(133, 19 + i, 133, 109 + i)
        display.line(163, 19 + i, 163, 109 + i)

    # Draw played positions
    for gy in range(3):
        for gx in range(3):
            if grid[gx][gy] == 0:
                draw_cross(gx, gy)
            elif grid[gx][gy] == 1:
                draw_nought(gx, gy)

    # Display game state
    if state == "play":
        display.text("Player", 20, 20, scale=0.5)
        if player == 0:
            draw_x(40, 50)
        elif player == 1:
            draw_circle(40, 50)
        draw_cursor(*cursor)
    elif state == "gameover":
        display.text("Game Over", 10, 20, scale=0.5)
        winner = is_won()
        if winner >= 0:
            display.line(*winning_line)
            display.text("Winner", 10, 40, scale=0.5)
            if winner == 0:
                draw_x(40, 70)
            elif winner == 1:
                draw_circle(40, 70)
        else:
            display.text("Draw", 10, 40, scale=0.5)

        # Move "Press B to Restart" to the bottom-left corner
        display.text("Press B to Restart", 10, HEIGHT - 20, scale=0.4)

    display.update()  # Refresh screen after drawing

# Draw a nought
def draw_nought(gridx, gridy):
    (cx, cy) = grid_to_coord(gridx, gridy)
    draw_circle(cx, cy)

# Draw a circle
def draw_circle(cx, cy, radius=10):
    degree_step_size = 10
    points = [
        (
            int(cx + radius * math.cos(math.radians(i))),
            int(cy + radius * math.sin(math.radians(i)))
        )
        for i in range(0, 360, degree_step_size)
    ]
    for i in range(len(points) - 1):
        display.line(*points[i], *points[i + 1])
    display.line(*points[-1], *points[0])

# Draw a cross
def draw_cross(gridx, gridy):
    (cx, cy) = grid_to_coord(gridx, gridy)
    draw_x(cx, cy)

# Draw an X
def draw_x(cx, cy):
    display.line(cx - 10, cy - 10, cx + 10, cy + 10)
    display.line(cx + 10, cy - 10, cx - 10, cy + 10)

# Highlight cursor position
def draw_cursor(gridx, gridy):
    (cx, cy) = grid_to_coord(gridx, gridy)
    display.rectangle(cx - 4, cy - 4, 8, 8)

# Convert grid to screen coordinates
def grid_to_coord(gridx, gridy):
    x = int(118 + 30 * gridx)
    y = int(34 + 30 * gridy)
    return (x, y)

# Check for a winner
def is_won():
    global winning_line
    for col in range(3):
        if grid[col][0] != -1 and grid[col][0] == grid[col][1] == grid[col][2]:
            winning_line = [118 + col * 30, 19, 118 + col * 30, 109]
            return grid[col][0]
    for row in range(3):
        if grid[0][row] != -1 and grid[0][row] == grid[1][row] == grid[2][row]:
            winning_line = [103, 34 + row * 30, 193, 34 + row * 30]
            return grid[0][row]
    if grid[0][0] != -1 and grid[0][0] == grid[1][1] == grid[2][2]:
        winning_line = [103, 19, 193, 109]
        return grid[0][0]
    if grid[2][0] != -1 and grid[2][0] == grid[1][1] == grid[0][2]:
        winning_line = [193, 19, 103, 109]
        return grid[2][0]
    return -1

# Initialize the display
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_MEDIUM)

state = "play"
player = 0
cursor = [0, 0]
played = 0
grid = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
winning_line = [0, 0, 0, 0]

# Draw the initial state
draw()

while True:
    button_pressed = False

    if state == "play":
        if display.pressed(badger2040.BUTTON_A) and cursor[0] > 0:
            cursor[0] -= 1
            button_pressed = True
        elif display.pressed(badger2040.BUTTON_C) and cursor[0] < 2:
            cursor[0] += 1
            button_pressed = True
        elif display.pressed(badger2040.BUTTON_UP) and cursor[1] > 0:
            cursor[1] -= 1
            button_pressed = True
        elif display.pressed(badger2040.BUTTON_DOWN) and cursor[1] < 2:
            cursor[1] += 1
            button_pressed = True
        elif display.pressed(badger2040.BUTTON_B):
            if grid[cursor[0]][cursor[1]] == -1:  # Place mark
                grid[cursor[0]][cursor[1]] = player
                played += 1
                button_pressed = True

                # Check for a winner or a draw
                if is_won() >= 0 or played >= 9:
                    state = "gameover"
                    draw()  # Final draw after game ends
                else:
                    player = 1 - player

    elif state == "gameover":
        # Wait for Button B to restart without refreshing
        if display.pressed(badger2040.BUTTON_B):
            grid = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
            played = 0
            player = 0
            cursor = [0, 0]
            state = "play"
            button_pressed = True

    # Update display only when necessary
    if state == "play" and button_pressed:
        draw()
