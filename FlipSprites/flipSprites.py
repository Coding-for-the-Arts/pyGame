import pygame
import pygame.sprite
import os
pygame.init()

speed = 5
WIDTH, HEIGHT = 500,300
BG_COLOR = pygame.Color('white')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#class this time with a sprite instead of image as an object
class FlipSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(FlipSprite, self).__init__()
        self.direction = "idle"
        self.images = []

        #iterate through all frames in folder
        for number in sorted(os.listdir("walk/")) :
            print(number)
            self.images.append(pygame.image.load(os.path.join("walk", number)))

        self.index = 0
        self.image = self.images[self.index]
        #get_rect() since sprite is a surface
        self.rect = self.image.get_rect()
        
        #set inital position
        self.rect.x = 300
        self.rect.y = 200

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0

        #change directions
        if self.direction == "right":
            self.image = self.images[self.index]
            self.rect.x +=speed
        elif self.direction == "left":
            self.image = pygame.transform.flip(self.images[self.index], True, False)
            self.rect.x -=speed
        else:
            self.image = self.images[1]
           

def main() :
    clock = pygame.time.Clock()
    walking_sprite = FlipSprite()
    sprite_group = pygame.sprite.Group(walking_sprite)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    walking_sprite.direction = "left"

                if event.key == pygame.K_RIGHT:
                    walking_sprite.direction = "right"

            #if key is released return to idle
            if event.type == pygame.KEYUP:
                walking_sprite.direction = "idle"

            if event.type == pygame.QUIT:
                pygame.exit()

        sprite_group.update()
        screen.fill(BG_COLOR)
        sprite_group.draw(screen)
        pygame.display.update()
        clock.tick(15)

if __name__ == "__main__":
    main()