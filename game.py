import pygame
import sys
from os.path import exists as file_exists
import math

class Game:
    screen = None
    aliens = []
    rockets = []
    game_continue = True
    score = 0


    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.highscore = self.highScore()

        main_character = Spaceship(self)
        main_sprite = pygame.sprite.Group()
        main_sprite.add(main_character)
        speed = [0,0]

        generator = Generator(self)
        alien_sprite = pygame.sprite.Group()
        for alien in self.aliens:
            alien_sprite.add(alien)

        while True:
            
            if len(self.aliens) == 0:
                self.displayText("You survived!", 60, (self.width/5, self.height/4))
                self.displayText(f"Final Score: {self.score}", 50,  (self.width/6, self.height/2))
                if self.score > self.highscore:
                    self.displayText(f"New High Score!", 55,  (self.width/6, self.height/2 + 70))
                    with open("highscore.txt", "w") as f:
                        f.write(str(self.score))
                else:
                    self.displayText(f"Current High Score: {self.highscore}", 45,  (self.width/6, self.height/2 + 60))

            if self.game_continue:
                alien_sprite.draw(self.screen)
                alien_sprite.update(self)
                self.displayText(f"Score: {self.score}", 25, (10, 10))
            else:
                self.displayText("You died!", 60, (self.width/5, self.height/4))
                self.displayText(f"Final Score: {self.score}", 50,  (self.width/6, self.height/2))
                if self.score > self.highscore:
                    self.displayText(f"New High Score!", 55,  (self.width/6, self.height/2 + 70))
                    with open("highscore.txt", "w") as f:
                        f.write(str(self.score))
                else:
                    self.displayText(f"Current High Score: {self.highscore}", 45,  (self.width/6, self.height/2 + 60))
            
            key = pygame.key.get_pressed()
    
            if key[pygame.K_a] or key[pygame.K_LEFT] and speed[0] >=-15:
                speed[0]-= 1 if main_character.rect.x >10 else 0
            if key[pygame.K_d] or key[pygame.K_RIGHT] and speed[0] <=15:
                speed[0]+= 1 if main_character.rect.x <self.width-60 else 0
            
            if speed[0] > 0:
                speed[0] -= 0.5
            if speed[0] < 0:
                speed[0] += 0.5

            if main_character.rect.x <10:
                speed[0] = 0
                main_character.rect.x = 10
            if main_character.rect.x >540:
                speed[0] = 0
                main_character.rect.x = 540

            main_character.rect = main_character.rect.move(speed)

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game_continue:
                    self.rockets.append(Rocket(self, main_character.rect.x, main_character.rect.y))
            for rocket in self.rockets:
                rocket.draw()
            for alien in self.aliens:
                alien.checkCollision(self)

            if self.game_continue: main_sprite.draw(self.screen)
            main_character.alienCollision(self)
        
    def displayText(self, text, size, pos):
        pygame.font.init()
        font = pygame.font.SysFont("Times New Roman", size)
        text_rendered = font.render(text, 1, (250, 250, 250))
        self.screen.blit(text_rendered, pos)
    
    def highScore(self):
        if file_exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                current_highscore = f.readline()                
                return int(current_highscore)
        else:
            return 0


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x = game.width/2
        self.y = game.height-50
        self.image = pygame.image.load("assets/spaceship.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    def alienCollision(self, game):
        for alien in game.aliens:
            if math.sqrt(math.pow(self.rect.centerx-alien.rect.centerx,2) + math.pow(self.rect.centery-alien.rect.centery,2))<=50:
                game.aliens.remove(alien)
                alien.kill()
                game.game_continue = False
                self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.game = game
        self.size = 50
        self.image = pygame.image.load("assets/alien.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = [0,1]
    def update(self, game):
        self.rect = self.rect.move(self.speed)
        if self.rect.y > game.height:
            game.aliens.remove(self)
            self.kill()
    def checkCollision(self, game):
        for rocket in game.rockets:
            if math.sqrt(math.pow(self.rect.centerx-rocket.x,2) + math.pow(self.rect.centery-rocket.y,2))<=30:
                game.rockets.remove(rocket)
                game.aliens.remove(self)
                if game.game_continue: game.score+=1
                self.kill()


class Generator:
    def __init__(self, game):
        margin = 30
        width = 60
        for x in range(margin, game.width-margin, width):
            for y in range(margin, int(game.height/2), width):
                game.aliens.append(Alien(game, x, y))


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen, 
                         (255, 50, 100), #crimson
                         pygame.Rect(self.x, self.y, 3, 10))
        self.y -= 2  


if __name__ == "__main__":
    game = Game(600, 800)