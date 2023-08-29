import os
import pygame
import numpy as np

from model.model import Population, Individual

from first_game.laser import Laser


class AiSpaceship(pygame.sprite.Sprite):
    
    def __init__(self, name, game, ai_individual : Individual):
        super().__init__()
        
        self.ai_individual = ai_individual
        
        self.name = name
        self.game = game
        
        # Créer le vaisseau à partir de l'image
        current_directory = os.getcwd()
        root_directory = os.path.abspath(current_directory)
        images_directory = os.path.join(root_directory, 'game/images/')
        
        original_image = pygame.image.load(f'{images_directory}/ai_ship_1.png')
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect()
        
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.rect.x = (self.game.screen.get_width() + self.game.infos_box.background_width) / 2 - self.image_width / 2
        self.rect.y = 0
        
        # Les coordonnées x minimales et maximales possibles pour le vaisseau
        self.min_x = self.game.infos_box.background_width
        self.max_x = self.game.screen.get_width() - self.image_width
        
        # Définit les caractéristiques du vaisseau
        self.health = 3
        self.max_health = 3
        self.attack = 1
        self.velocity = 5
        self.max_projectile = 5
        self.all_projectiles = pygame.sprite.Group()
    
    def lauch_projectile(self):
        
        self.all_projectiles.add(Laser(self, self.game.my_ship))
    
    def damage_attack(self):
        
        self.health -= 1
        
    def move(self, class_predict : int):
        
        # Déplacement vers la droite
        if any([class_predict == 1, class_predict == 3]) and self.rect.x < self.max_x:
            self.rect.x += self.velocity

        # Déplacement vers la gauche
        elif any([class_predict == 2, class_predict == 4]) and self.rect.x > self.min_x:
            self.rect.x -= self.velocity
        
    def play_turn(self, launch_projectile : bool, infos_make_prediction : dict):
        
        # print(infos_make_prediction)
        my_array_prediction = np.array(list(infos_make_prediction.values())).reshape(1, -1)
        # print(my_array_prediction.shape)
        
        prediction = self.ai_individual.make_prediction(my_array_prediction)
        class_predict = int(np.argmax(prediction))
        print(class_predict)
        
        if class_predict != 0 and class_predict != 5:
            self.move(class_predict)
            
        # if self.keys_pressed:
        #     self.move()
        
        if any([class_predict == 3, class_predict == 4, class_predict == 5]):
            launch_projectile = True
        
        if launch_projectile:
            self.lauch_projectile()
        
        for projectile in self.all_projectiles:
            projectile.move()