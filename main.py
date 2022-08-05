import pygame
import os

pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Game")

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

white = (255, 255, 255)
black = (0, 0, 0)
redc = (255, 0, 0)
yellowc = (255, 255, 0)

border = pygame.Rect(width // 2 - 5, 0, 10, height)

bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

health_font = pygame.font.SysFont('comicsans', 40)
winner_font = pygame.font.SysFont('comicsans', 100)

velocity = 5
bullet_velocity = 7
FPS = 60
spaceship_width, spaceship_height = 55, 40

yellow_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(
    pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height)), 90)

red_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
red_spaceship = pygame.transform.rotate(
    pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height)), 270)

space = pygame.transform.scale(pygame.image.load(os.path.join('Assets', '1212.png')), (width, height))


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - velocity > 0:  # LEFT MOVE
        yellow.x -= velocity
    if key_pressed[pygame.K_d] and yellow.x + velocity + yellow.width < border.x + border.width:  # right MOVE
        yellow.x += velocity
    if key_pressed[pygame.K_w] and yellow.y - velocity > 0:  # up MOVE
        yellow.y -= velocity
    if key_pressed[pygame.K_s] and yellow.y + velocity + yellow.height < height - 15:  # down MOVE
        yellow.y += velocity


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - velocity > border.x + border.width:  # LEFT MOVE
        red.x -= velocity
    if key_pressed[pygame.K_RIGHT] and red.x + velocity + red.width < width:  # right MOVE
        red.x += velocity
    if key_pressed[pygame.K_UP] and red.y - velocity > 0:  # up MOVE
        red.y -= velocity
    if key_pressed[pygame.K_DOWN] and red.y + velocity + red.height < height - 15:  # down MOVE
        red.y += velocity


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    window.blit(space, (0, 0))
    pygame.draw.rect(window, black, border)

    red_health_text = health_font.render("Health: " + str(red_health), True, white)
    yellow_health_text = health_font.render("Health: " + str(yellow_health), True, white)
    window.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    window.blit(yellow_health_text, (10, 10))

    window.blit(yellow_spaceship, (yellow.x, yellow.y))
    window.blit(red_spaceship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(window, redc, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(window, yellowc, bullet)

    pygame.display.update()


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_velocity
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > width:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_velocity
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = winner_font.render(text, True, white)
    window.blit(draw_text, (width // 2 - draw_text.get_width() // 2, height // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 + 2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 + 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()
            if event.type == yellow_hit:
                yellow_health -= 1
                bullet_hit_sound.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
