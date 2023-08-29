import os
import pygame

from first_game.laser import Laser


class Spaceship(pygame.sprite.Sprite):
    
    def __init__(self, name, game):
        super().__init__()
        
        self.name = name
        self.game = game
        
        # Créer le vaisseau à partir de l'image
        current_directory = os.getcwd()
        root_directory = os.path.abspath(current_directory)
        images_directory = os.path.join(root_directory, 'game/images/')
        
        original_image = pygame.image.load(f'{images_directory}/ship_1.png')
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect()
        
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.rect.x = self.game.infos_box.background_width + self.image_width / 2
        self.rect.y = self.game.screen.get_height() - self.image_height
        # self.rect.x = (self.game.screen.get_width() + self.game.infos_box.background_width) / 2 - self.image_width / 2
        # self.rect.y = self.game.screen.get_height() - self.image_height
        
        # Les coordonnées x minimales et maximales possibles pour le vaisseau
        self.min_x = self.game.infos_box.background_width
        self.max_x = self.game.screen.get_width() - self.image_width
        
        # Définit les caractéristiques du vaisseau
        self.health = 3
        self.max_health = 3
        self.attack = 1
        self.velocity = 1
        self.max_projectile = 5
        self.all_projectiles = pygame.sprite.Group()
        
        self.right = True
    
    def lauch_projectile(self):
        
        self.all_projectiles.add(Laser(self, self.game.ai_ship))
    
    def damage_attack(self):
        
        self.health -= 1
        
    def move(self):
        
        # # Déplacement vers la droite
        # if any([self.keys_pressed.get(pygame.K_d), self.keys_pressed.get(pygame.K_RIGHT)]) and self.rect.x < self.max_x:
        #     self.rect.x += self.velocity

        # # Déplacement vers la gauche
        # elif any([self.keys_pressed.get(pygame.K_q), self.keys_pressed.get(pygame.K_LEFT)]) and self.rect.x > self.min_x:
        #     self.rect.x -= self.velocity
        
        if (self.game.laps % 800) == 0:
            if self.right:
                self.right = False
            elif not self.right:
                self.right = True
            
        if self.right and self.rect.x < self.max_x:
            self.rect.x += self.velocity
        elif not self.right and self.rect.x > self.min_x:
            self.rect.x -= self.velocity
        
    def play_turn(self, launch_projectile : bool = False):
        
        if (self.game.laps % 150) == 0 and len(self.all_projectiles) < self.max_projectile:
            launch_projectile = True
            
        self.keys_pressed = self.game.keys_pressed
        
        if self.keys_pressed:
            self.move()
        
        if launch_projectile:
            self.lauch_projectile()
        
        for projectile in self.all_projectiles:
            projectile.move()