import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Shooter")
clock = pygame.time.Clock()

# Load images
background = pygame.transform.scale(pygame.image.load(r"D:\pyhton project\python project\bleh.png"), (WIDTH, HEIGHT))
spaceship_image = pygame.transform.scale(pygame.image.load(r"D:\pyhton project\python project\Spaceship.png"), (50, 50))
bullet_image = pygame.transform.scale(pygame.image.load(r"D:\pyhton project\python project\image-removebg-preview.png"), (15, 30))
heart_image = pygame.transform.scale(pygame.image.load(r"D:\pyhton project\python project\Pixel_Red_Heart_PNG_Images___Heart_Icons__Pixel_Icons__Red_Icons_PNG_Transparent_Background_-_Pngtree-removebg-preview.png"), (30, 30))
game_over_background = pygame.transform.scale(
    pygame.image.load(r"D:\pyhton project\python project\Game_Over_Pixel_Vector_Design_Images__Pixelate_Game_Over_Word_Text_Effect__Pixel__Font__Digital_PNG_Image_For_Free_Download-removebg-preview.png"), 
    (350, 160)  # Increased height and slightly wider
)
restart_button_img = pygame.transform.scale(pygame.image.load(r"D:\pyhton project\python project\Gaming_SVG_Collection__Gaming_SVG_Designs___Cut_File___Craftpi-removebg-preview.png"), (100, 100))
restart_button_rect = restart_button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

# Asteroid images
asteroid_imgs = [
    pygame.transform.scale(pygame.image.load(rf"D:\\pyhton project\\python project\\asteroid {i}.png"), (50, 50)) for i in range(1, 5)
]

# Explosion frames
explosion_frames = [
    pygame.transform.scale(pygame.image.load(r"D:\pyhton project\python project\Screenshot_2025-04-18_101245-removebg-preview.png"), (70, 70)),
    pygame.transform.scale(pygame.image.load(r"D:\pyhton project\python project\Screenshot_2025-04-18_101109-removebg-preview.png"), (70, 70))
]

# Game variables
ship = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 60, 50, 50)
ship_speed = 6
bullets = []
bullet_speed = 10
asteroids = []
asteroid_spawn_delay = 2000
last_asteroid_spawn = pygame.time.get_ticks()
last_shot = 0
cooldown = 300
score = 0
lives = 3
font = pygame.font.SysFont("Arial", 30)

# Heart blink timer
blink_time = 200
blink_start = 0
blink_index = -1

# Score values
asteroid_scores = [5, 10, 15, 20]

def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def play_explosion():
    for _ in range(6):
        for frame in explosion_frames:
            screen.blit(background, (0, 0))
            screen.blit(game_over_background, (WIDTH//2 - 150, HEIGHT//2 - 50))
            screen.blit(frame, (ship.x - 10, ship.y - 10))
            pygame.display.flip()
            pygame.time.wait(100)

def restart_game():
    global ship, bullets, asteroids, score, lives, blink_index, last_asteroid_spawn, running
    ship.x, ship.y = WIDTH // 2 - 25, HEIGHT - 60
    bullets.clear()
    asteroids.clear()
    score = 0
    lives = 3
    blink_index = -1
    last_asteroid_spawn = pygame.time.get_ticks()
    running = True

# Main game loop
running = True
while True:
    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship.left > 0:
            ship.x -= ship_speed
        if keys[pygame.K_RIGHT] and ship.right < WIDTH:
            ship.x += ship_speed
        if keys[pygame.K_SPACE] and current_time - last_shot > cooldown:
            bullet_rect = bullet_image.get_rect(center=(ship.centerx, ship.top))
            bullets.append(bullet_rect)
            last_shot = current_time

        if len(asteroids) < 4 and current_time - last_asteroid_spawn > asteroid_spawn_delay:
            x = random.randint(50, WIDTH - 100)
            kind = random.randint(0, 3)
            rect = pygame.Rect(x, -50, 50, 50)
            asteroids.append({"rect": rect, "image": asteroid_imgs[kind], "type": kind, "dx": random.choice([-2, 2])})
            last_asteroid_spawn = current_time

        for b in bullets[:]:
            b.y -= bullet_speed
            if b.bottom < 0:
                bullets.remove(b)

        for a in asteroids[:]:
            a_type = a["type"]
            if a_type == 0:
                a["rect"].y += 6
            elif a_type == 1:
                a["rect"].y += 2 if current_time % 1000 < 500 else 6
            elif a_type == 2:
                a["rect"].x += a["dx"]
                if a["rect"].left <= 0 or a["rect"].right >= WIDTH:
                    a["dx"] *= -1
                a["rect"].y += 4 if current_time % 800 < 400 else 7
            elif a_type == 3:
                a["rect"].y += random.choice([4, 6, 8])

            if a["rect"].top > HEIGHT or a["rect"].colliderect(ship):
                asteroids.remove(a)
                blink_start = current_time
                blink_index = lives - 1
                lives -= 1

            for b in bullets[:]:
                if a["rect"].colliderect(b):
                    bullets.remove(b)
                    try:
                        asteroids.remove(a)
                        score += asteroid_scores[a_type]
                    except:
                        pass

        if lives > 0:
            screen.blit(spaceship_image, ship)

        for b in bullets:
            screen.blit(bullet_image, b)

        for a in asteroids:
            screen.blit(a["image"], a["rect"])

        for i in range(lives):
            if i == blink_index and (current_time - blink_start) % 300 < 150:
                continue
            screen.blit(heart_image, (10 + i * 35, 50))

        draw_text(f"Score: {score}", 10, 10)

        if lives <= 0:
            play_explosion()
            pygame.time.wait(1000)
            running = False
            break

        pygame.display.flip()
        clock.tick(60)

    while not running:
        screen.blit(background, (0, 0))
        screen.blit(game_over_background, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        screen.blit(restart_button_img, restart_button_rect)
        draw_text("Score: " + str(score), WIDTH // 2 - 60, HEIGHT // 2 + 60)
        draw_text("Press 'R' to Restart", WIDTH // 2 - 100, HEIGHT // 2 + 180)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(event.pos):
                restart_game()
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
                break

        pygame.display.flip()
        clock.tick(60)
