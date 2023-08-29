import os
import pygame


class Laser(pygame.sprite.Sprite):
    
    def __init__(self, ship, ennemy_ship):
        super().__init__()
        
        self.ship = ship
        self.ennemy_ship = ennemy_ship
        
        # Créer le vaisseau à partir de l'image
        current_directory = os.getcwd()
        root_directory = os.path.abspath(current_directory)
        images_directory = os.path.join(root_directory, 'game/images/')
        
        original_image = pygame.image.load(f'{images_directory}/pink_laser.png')
        if self.ship.name == 'my_ship':
            fliped_image = pygame.transform.flip(original_image, False, True)
        else:
            fliped_image = original_image
        self.image = pygame.transform.scale(fliped_image, (25, 25))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.rect.x = ship.rect.x + (ship.image_width / 2) - (self.image_width / 2)
        if self.ship.name == 'my_ship':
            self.rect.y = ship.rect.y
        else:
            self.rect.y = ship.rect.y + self.ship.image_height
        
        self.i = 0
        self.velocity = 2
        self.attack = 1
    
    def move(self):
        
        if self.ship.name == 'my_ship':
            self.rect.y -= self.velocity
        else:
            self.rect.y += self.velocity
        
        # si le projectile entre en collision avec un des vaisseaux
        if self.ship.game.check_collision(self, self.ship.game.all_ships):
            # Supprimer le projectile ennemi
            for ship in self.ship.game.all_ships:
                if ship.name != self.ship.name:
                    if pygame.sprite.collide_mask(self, ship):
                        ship.damage_attack()
                        self.remove()
        
        # si le projectile entre en collision avec un projectile ennemi
        if self.ship.game.check_collision(self, self.ennemy_ship.all_projectiles):
            # Supprimer le projectile ennemi
            for enemy_projectile in self.ennemy_ship.all_projectiles:
                if pygame.sprite.collide_mask(self, enemy_projectile):
                    enemy_projectile.remove()

            # Supprimer le projectile courant
            self.remove()

            
    def remove(self):
        
        self.ship.all_projectiles.remove(self)