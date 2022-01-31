import pygame
import os
pygame.font.init()
pygame.mixer.init()

# HELP FUNCIONS
def aspect_scale(img, bx, by):
    ix, iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (sx, sy))


WIDTH, HEIGHT = 1000, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
pygame.display.set_caption("Bomb Love")

HEALTH_FONT = pygame.font.Font(os.path.join("Assets", "I-pixel-u.ttf"), 40)
WIN_FONT = pygame.font.Font(os.path.join("Assets", "I-pixel-u.ttf"), 80)
FPS = 60
VEL = 5
MAX_BULLET = 5
BULLET_VEL = 8

IMG_WIDTH, IMG_HEIGHT = 120, 120
BULLET_WIDTH, BULLET_HEIGHT = 50,50
GOOD_GUY = pygame.image.load(os.path.join("Assets", "goodguy.png"))
GOOD_GUY = aspect_scale(GOOD_GUY, IMG_WIDTH, IMG_HEIGHT)
BAD_GUY = pygame.image.load(os.path.join("Assets", "badguy.png"))
BAD_GUY = aspect_scale(BAD_GUY, IMG_WIDTH, IMG_HEIGHT)

HEART = pygame.image.load(os.path.join("Assets", "heart.png"))
BOMB = pygame.image.load(os.path.join("Assets", "bomb.png"))

HEART = aspect_scale(HEART, BULLET_WIDTH, BULLET_HEIGHT)
BOMB = aspect_scale(BOMB, BULLET_WIDTH, BULLET_HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "ouch.mp3"))
BOMB_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "bomb.mp3"))
HEART_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "heart.mp3"))

GG_HIT= pygame.USEREVENT + 1
BD_HIT = pygame.USEREVENT + 2
RESTART = pygame.USEREVENT + 3

YELLOW = (255,255, 0)
BLACK = (0,0,0)
RED = (255,0, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


def draw(badguy, goodguy, rB, yB, badguy_health, goodguy_health):
    WIN.fill(WHITE)
   
    pygame.draw.rect(WIN, BLACK, BORDER)

    badguy_health_text = HEALTH_FONT.render("Health: " + str(badguy_health), 1, BLACK)
    goodguy_health_text = HEALTH_FONT.render("Health: " + str(goodguy_health), 1, BLACK)

    WIN.blit(goodguy_health_text, (WIDTH - goodguy_health_text.get_width() - 150, 10))
    WIN.blit(badguy_health_text, (badguy_health_text.get_width()/2 + 50, 10))
    
    WIN.blit(GOOD_GUY, (goodguy.x, goodguy.y))
    WIN.blit(BAD_GUY, (badguy.x, badguy.y))

    for bullet in yB:
        WIN.blit(HEART, (bullet.x, bullet.y))

    for bullet in rB:
        WIN.blit(BOMB, (bullet.x, bullet.y))

    pygame.display.update()


def draw_winner(text, color):
    draw_text = WIN_FONT.render(text, 10, color)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    restart_text = HEALTH_FONT.render('Restart?', 1, BLACK)
    restart_text2 = HEALTH_FONT.render('Yes = 1   No = 0', 1, BLACK)
    WIN.blit(restart_text, (WIDTH/2 - restart_text.get_width() / 2 , HEIGHT/2 - restart_text.get_height()/2  + 100))
    WIN.blit(restart_text2, (WIDTH/2 - restart_text2.get_width() / 2 , HEIGHT/2 - restart_text2.get_height()/2  + 150))
    pygame.display.update()
    pygame.time.delay(100)

    restart_key = pygame.key.get_pressed()
    if restart_key[pygame.K_1] == True:
        pygame.event.post(pygame.event.Event(RESTART))
    elif restart_key[pygame.K_0] == True:
        pygame.quit()

def moveCharacter(character, keyUp, keyDown, keyLeft, keyRight):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[keyUp] and character.y - VEL > 0:
        character.y -= VEL
    if keysPressed[keyDown] and character.y + VEL + character.height < HEIGHT:
        character.y += VEL
    if keysPressed[keyLeft]:
        if keyLeft == pygame.K_LEFT and character.x - VEL > BORDER.x + BORDER.width:
            character.x -= VEL
        if keyLeft == pygame.K_a and character.x - VEL > 0:
            character.x -= VEL
    if keysPressed[keyRight]:
        if keyRight == pygame.K_RIGHT and character.x + VEL < WIDTH - character.width:
           character.x += VEL
        if keyRight == pygame.K_d and character.x + VEL + character.width < BORDER.x - BORDER.width:
           character.x += VEL


def gotHit(rB, yB, badguy, goodguy):

    for bullet in yB:
        bullet.x -= BULLET_VEL
        if badguy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BD_HIT))
            yB.remove(bullet)
        elif bullet.x < 0:
            yB.remove(bullet)

    for bullet in rB:
        bullet.x += BULLET_VEL
        if goodguy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GG_HIT))
            rB.remove(bullet)
        elif bullet.x > WIDTH:
            rB.remove(bullet)


def main():
    clock = pygame.time.Clock()
    badguy = pygame.Rect(100, HEIGHT/2, BAD_GUY.get_width(),
                      BAD_GUY.get_height())
    goodguy = pygame.Rect(
        900, HEIGHT/2, GOOD_GUY.get_width(), GOOD_GUY.get_height())

    bullets_badguy = []
    bullets_goodguy = []

    GG_HEALTH = 10
    BG_HEALTH = 10

    run = True
 
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(bullets_badguy) < MAX_BULLET:
                    bullet = pygame.Rect(badguy.x + badguy.width//2, badguy.y , 10, 5)
                    bullets_badguy.append(bullet)
                    BOMB_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(bullets_goodguy) < MAX_BULLET:
                    bullet = pygame.Rect(goodguy.x + goodguy.width//2, goodguy.y , 10, 5)
                    bullets_goodguy.append(bullet)
                    HEART_FIRE_SOUND.play()
            
            if event.type == BD_HIT:
                BG_HEALTH -= 2
                BULLET_HIT_SOUND.play()

            if event.type == GG_HIT:    
                GG_HEALTH -= 2
                BULLET_HIT_SOUND.play()
            
            if event.type == RESTART:
                main()


        winner_text = ""
        if BG_HEALTH <= 0:
            winner_text = "Love wins!"
            pygame.draw.rect(WIN, WHITE, BORDER)   
            draw_winner(winner_text, RED)
                         

        if GG_HEALTH <= 0:
            winner_text = "Violence wins!"
            draw_winner(winner_text, BLACK)

     
        moveCharacter(goodguy, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        moveCharacter(badguy, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        gotHit(bullets_badguy, bullets_goodguy, badguy, goodguy)
        
        draw(badguy, goodguy, bullets_badguy, bullets_goodguy, BG_HEALTH, GG_HEALTH)


if __name__ == "__main__":
    main()
