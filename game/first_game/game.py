import os
import pygame

from first_game.spaceship import Spaceship
from first_game.ai_spaceship import AiSpaceship
from first_game.infos_box import InfosBox

from model.model import Population, Individual


class Game():
    
    pygame.display.set_caption("Jeu IA")
    screen = pygame.display.set_mode((1080, 720))
    
    new_pop = Population()
    new_pop.create_population(input_shape=(34,))
    individual = 0
    
    def __init__(self):

        # Fenêtre du jeu
        
        # Génère la boîte d'informations de la partie
        self.infos_box = InfosBox(self)
                
        self.clock = pygame.time.Clock()
        self.clock.tick(60)  # limits FPS to 60
        
        # Touche appuyer par le joueur
        self.keys_pressed = {}
        
        # Générer les vaisseaux
        self.all_ships = pygame.sprite.Group()

        self.my_ship = Spaceship(name='my_ship', game=self)
        self.all_ships.add(self.my_ship)

        self.ai_ship = AiSpaceship(name='ai_ship', game=self, ai_individual=self.new_pop.all_individuals[self.individual])
        print('\nNew individual selected :', self.individual)
        self.individual += 1
        
        self.all_ships.add(self.ai_ship)
        
        self.is_playing = False
            
    def run(self):
        
        # Boucle du jeu
        running = True
        self.laps = 0
    
        while running:
            # Remplis le fond du jeu
            self.screen.fill((6, 2, 40))
            # current_directory = os.getcwd()
            # root_directory = os.path.abspath(current_directory)
            # images_directory = os.path.join(root_directory, 'game/images/')
            
            # original_image = pygame.image.load(f'{images_directory}/background.jpg')
            # original_rect = original_image.get_rect()
            # background_image_width = self.screen.get_width()
            # background_image_height = background_image_width * original_image.get_height() / original_image.get_width()
            # background_image = pygame.transform.scale(original_image, (background_image_width, background_image_height))
            # background_rect = background_image.get_rect()
            # self.screen.blit(background_image, background_rect)
            
            # Définit les variables projectile lancé
            my_launch_projectile = False
            ai_launch_projectile = False
            
            # Fermer l'application si l'utilisateur ferme la fenêtre
            for event in pygame.event.get():
                event_type = event.type
                if event_type == pygame.QUIT:
                    running = False
                    pygame.quit()
                
                elif event_type == pygame.KEYDOWN:
                    self.keys_pressed[event.key] = True
                    
                    # lance un projectile
                    if event.key == pygame.K_SPACE and len(self.my_ship.all_projectiles) < self.my_ship.max_projectile:
                        my_launch_projectile = True
                    if event.key == pygame.K_i and len(self.ai_ship.all_projectiles) < self.ai_ship.max_projectile:
                        ai_launch_projectile = True
                    if event.key == pygame.K_m:
                        if self.is_playing:
                            print('\nSTOP\n')
                            self.is_playing = False
                        else:
                            print('\nGO\n')
                            self.is_playing = True
                
                elif event_type == pygame.KEYUP:
                    self.keys_pressed[event.key] = False
                    
            if self.is_playing:
                self.update(my_launch_projectile, ai_launch_projectile)
            
            # Mettre à jour la fenêtre
            pygame.display.flip()
    
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
        
    def update(self, my_launch_projectile, ai_launch_projectile):
            
            self.laps += 1
            
            infos_make_prediction = {
                'ai_pos_x' : self.ai_ship.rect.x / self.screen.get_width(),
                'ai_pos_img_width' : self.ai_ship.image_width / self.screen.get_width(),
                
                'ennemy_pos_x' : self.my_ship.rect.x / self.screen.get_width(),
                'ennemy_pos_img_width' : self.my_ship.image_width / self.screen.get_width(),
            }
            
            n_ai_laser = 0
            for l, ai_laser in enumerate(self.ai_ship.all_projectiles):
                
                infos_make_prediction[f'ai_laser_pos_{l}_x'] = float(ai_laser.rect.x / self.screen.get_width())
                infos_make_prediction[f'ai_laser_pos_{l}_y'] = float(ai_laser.rect.y / self.screen.get_height())
                infos_make_prediction[f'ai_laser_pos_{l}_image_width'] = float(ai_laser.image_width / self.screen.get_width())
                n_ai_laser = l
            
            while n_ai_laser < self.ai_ship.max_projectile:
                    
                infos_make_prediction[f'ai_laser_pos_{n_ai_laser}_x'] = 0.0
                infos_make_prediction[f'ai_laser_pos_{n_ai_laser}_y'] = 0.0
                infos_make_prediction[f'ai_laser_pos_{n_ai_laser}_image_width'] = 0.0
                n_ai_laser += 1
                
            n_my_laser = 0
            for m, my_laser in enumerate(self.my_ship.all_projectiles):
                
                infos_make_prediction[f'my_laser_pos_{m}_x'] = float(my_laser.rect.x / self.screen.get_width())
                infos_make_prediction[f'my_laser_pos_{m}_y'] = float(my_laser.rect.y / self.screen.get_height())
                infos_make_prediction[f'my_laser_pos_{m}_image_width'] = float(my_laser.image_width / self.screen.get_width())
                n_my_laser = m
            
            while n_my_laser < self.my_ship.max_projectile:
                    
                infos_make_prediction[f'my_laser_pos_{n_my_laser}_x'] = 0.0
                infos_make_prediction[f'my_laser_pos_{n_my_laser}_y'] = 0.0
                infos_make_prediction[f'my_laser_pos_{n_my_laser}_image_width'] = 0.0
                n_my_laser += 1

            # Dessine le vaisseau et réalise son tour de jeu
            self.screen.blit(self.my_ship.image, self.my_ship.rect)
            self.screen.blit(self.ai_ship.image, self.ai_ship.rect)
            self.my_ship.play_turn(launch_projectile=my_launch_projectile)
            self.ai_ship.play_turn(launch_projectile=ai_launch_projectile, infos_make_prediction=infos_make_prediction)
            
            # Supprime les lasers hors terrain
            for ship in self.all_ships:
                for projectile in ship.all_projectiles:
                    if projectile.rect.y > self.screen.get_height() or projectile.rect.y < 0:
                        projectile.remove()
                    
            # Dessine les projectiles
            self.my_ship.all_projectiles.draw(self.screen)
            self.ai_ship.all_projectiles.draw(self.screen)
            
            # Dessine la boîte d'infos
            self.infos_box.draw_infos_box()
            
            # Game Over si un des deux joueurs meurt
            for ship in self.all_ships:
                if ship.health <= 0:
                    print(f'{ship.name} a perdu!')
                    self.__init__()