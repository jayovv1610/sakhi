
import math
import pygame


# Screen size
WIDTH = 800
HEIGHT = 480

# Colors
BACKGROUND_COLOR = (12, 14, 22)
EYE_COLOR = (80, 220, 255)


def draw_eye(screen, x, y, width, height):
    """Draw one of Sakhi's eyes."""

    pygame.draw.ellipse(
        screen,
        EYE_COLOR,
        (x, y, width, height)
    )


def main():
    """Show Sakhi's animated eyes."""

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SAKHI")

    clock = pygame.time.Clock()

    running = True
    timer = 0

    while running:
        # Check if the window should close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen before drawing
        screen.fill(BACKGROUND_COLOR)

        # Make the eyes blink occasionally
        blinking = abs(math.sin(timer * 2)) > 0.985

        if blinking:
            eye_height = 8
        else:
            eye_height = 130

        # Draw both eyes
        draw_eye(screen, 200, 175, 150, eye_height)
        draw_eye(screen, 450, 175, 150, eye_height)

        pygame.display.flip()

        # Keep the animation running smoothly
        clock.tick(60)
        timer += 0.03

    pygame.quit()


if __name__ == "__main__":
    main()
