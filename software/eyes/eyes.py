
import math
import random
import pygame


# Size of the drawing area
WIDTH = 800
HEIGHT = 480

# Eye colors
CYAN = (0, 230, 255)
RED = (255, 35, 55)
BLACK = (0, 0, 0)

# Starting expression
state = "IDLE"
emotion = "NORMAL"


def draw_eye(surface, x, y, width, height, angle=0, color=CYAN):
    """Draw a rounded eye."""

    width = max(4, int(width))
    height = max(4, int(height))

    layer = pygame.Surface(
        (width + 24, height + 24),
        pygame.SRCALPHA
    )

    rectangle = pygame.Rect(12, 12, width, height)

    pygame.draw.rect(
        layer,
        color,
        rectangle,
        border_radius=min(width, height) // 2
    )

    rotated = pygame.transform.rotozoom(layer, angle, 1)

    surface.blit(
        rotated,
        rotated.get_rect(center=(int(x), int(y)))
    )


def draw_curved_eye(surface, x, y, happy=True):
    """Draw curved eyes for happy or sad expressions."""

    points = []

    for i in range(31):
        px = x - 65 + i * 130 / 30
        angle = (i / 30) * math.pi
        curve = math.sin(angle) * 34

        py = y - curve if happy else y + curve
        points.append((int(px), int(py)))

    pygame.draw.lines(surface, CYAN, False, points, 15)


def draw_error_face(surface, positions, center_y):
    """Show red, glitching eyes when something goes wrong."""

    surface.fill((12, 0, 0))

    shake_x = random.randint(-9, 9)
    shake_y = random.randint(-5, 5)

    for index, x in enumerate(positions):
        # Sometimes hide an eye for the glitch effect
        if random.random() < 0.10:
            continue

        angle = 12 if index == 0 else -12

        draw_eye(
            surface,
            x + shake_x + random.randint(-3, 3),
            center_y + shake_y,
            115,
            85,
            angle,
            RED
        )

    # Occasionally draw a glitch line
    if random.random() < 0.15:
        y = random.randint(140, 340)

        pygame.draw.line(
            surface,
            (110, 0, 20),
            (150, y),
            (650, y),
            random.randint(1, 3)
        )


def draw_face(surface, mode, mood, timer, openness, look_x, look_y):
    """Draw Sakhi's eyes based on her current state and mood."""

    surface.fill(BLACK)

    center_x = WIDTH / 2
    center_y = HEIGHT / 2

    positions = (center_x - 135, center_x + 135)

    # Error mode takes priority over emotions
    if mode == "ERROR":
        draw_error_face(surface, positions, center_y)
        return

    # Happy and sad eyes
    if mood in ("HAPPY", "SAD"):
        for x in positions:
            draw_curved_eye(
                surface,
                x,
                center_y,
                happy=(mood == "HAPPY")
            )
        return

    # Angry eyes
    if mood == "ANGRY":
        draw_eye(surface, positions[0], center_y, 125, 75, 20)
        draw_eye(surface, positions[1], center_y, 125, 75, -20)
        return

    # Surprised eyes
    if mood == "SURPRISED":
        for x in positions:
            draw_eye(surface, x, center_y, 95, 160)
        return

    # Sleepy eyes
    if mood == "SLEEPY":
        for x in positions:
            draw_eye(surface, x, center_y, 125, 28)
        return

    # Normal expressions for each state
    for x in positions:
        eye_width = 115
        eye_height = 145 * openness

        dx = look_x
        dy = look_y

        if mode == "IDLE":
            dy += math.sin(timer * 1.5) * 4

        elif mode == "LISTENING":
            eye_width = 120
            eye_height = 165 * openness

        elif mode == "THINKING":
            eye_height = 105 * openness
            dx += math.sin(timer * 2) * 28
            dy -= 24

        elif mode == "SPEAKING":
            eye_height = (
                115 + math.sin(timer * 9) * 25
            ) * openness

            dy += math.sin(timer * 9) * 5

        draw_eye(
            surface,
            x + dx,
            center_y + dy,
            eye_width,
            eye_height
        )


def get_blink_openness(now, blink_started):
    """Calculate how open the eyes should be."""

    elapsed = now - blink_started

    if 0 <= elapsed < 240:
        openness = abs(elapsed - 120) / 120
        return max(0.04, openness)

    return 1


def main():
    """Run Sakhi's animated eye display."""

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("SAKHI - Expressive Eyes")

    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()

    canvas = pygame.Surface((WIDTH, HEIGHT))

    running = True

    current_state = state
    current_emotion = emotion

    blink_at = pygame.time.get_ticks() + 2000
    blink_started = -1000

    look_x = 0
    look_y = 0

    target_x = 0
    target_y = 0

    next_look = 0

    while running:
        now = pygame.time.get_ticks()
        timer = now / 1000

        # Keyboard controls for testing expressions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_ESCAPE:
                    running = False

                elif key == pygame.K_1:
                    current_state, current_emotion = "IDLE", "NORMAL"
                elif key == pygame.K_2:
                    current_state, current_emotion = "LISTENING", "NORMAL"
                elif key == pygame.K_3:
                    current_state, current_emotion = "THINKING", "NORMAL"
                elif key == pygame.K_4:
                    current_state, current_emotion = "SPEAKING", "NORMAL"
                elif key == pygame.K_5:
                    current_state, current_emotion = "ERROR", "NORMAL"

                elif key == pygame.K_h:
                    current_emotion = "HAPPY"
                elif key == pygame.K_s:
                    current_emotion = "SAD"
                elif key == pygame.K_a:
                    current_emotion = "ANGRY"
                elif key == pygame.K_u:
                    current_emotion = "SURPRISED"
                elif key == pygame.K_z:
                    current_emotion = "SLEEPY"
                elif key == pygame.K_n:
                    current_emotion = "NORMAL"

        # Blink at random intervals
        if now >= blink_at:
            blink_started = now
            blink_at = now + random.randint(2200, 5000)

        openness = get_blink_openness(now, blink_started)

        # Move the eyes in random directions
        if now >= next_look:
            target_x = random.randint(-20, 20)
            target_y = random.randint(-12, 12)

            next_look = now + random.randint(1800, 3500)

        # Smooth eye movement
        look_x += (target_x - look_x) * 0.035
        look_y += (target_y - look_y) * 0.035

        draw_face(
            canvas,
            current_state,
            current_emotion,
            timer,
            openness,
            look_x,
            look_y
        )

        # Fit the drawing to the connected screen
        scale = min(
            screen_width / WIDTH,
            screen_height / HEIGHT
        )

        new_size = (
            int(WIDTH * scale),
            int(HEIGHT * scale)
        )

        scaled_canvas = pygame.transform.smoothscale(
            canvas,
            new_size
        )

        screen.fill(BLACK)

        screen.blit(
            scaled_canvas,
            (
                (screen_width - new_size[0]) // 2,
                (screen_height - new_size[1]) // 2
            )
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
