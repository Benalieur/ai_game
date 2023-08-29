import os
import pygame


class InfosBox():
    
    def __init__(self, game):
        
        self.game = game
        self.screen = game.screen
        
        self.background_width = self.screen.get_width() / 5
        self.background_height = self.screen.get_height()
        self.background_color = (255, 255, 255)
        self.background_position = [0, 0, self.background_width, self.background_height]

        self.border_thickness = 3
        self.front_width = self.background_width - (self.border_thickness * 2)
        self.front_height = self.background_height - (self.border_thickness * 2)
        self.front_color = (85, 85, 85)
        self.front_position = [self.border_thickness, self.border_thickness, self.front_width, self.front_height]
        
    def draw_infos_box(self):
        
        self.background_image = pygame.draw.rect(self.screen, self.background_color, self.background_position)
        self.front_image = pygame.draw.rect(self.screen, self.front_color, self.front_position)
        
        self.draw_hearts()
    
    def draw_hearts(self):
        
        current_directory = os.getcwd()
        root_directory = os.path.abspath(current_directory)
        images_directory = os.path.join(root_directory, 'game/images/')
        
        for j, ship in enumerate([self.game.ai_ship, self.game.my_ship]):
            for i in range(ship.max_health):
                
                # Dessine les coeurs vides
                self.image_empty_heart = pygame.image.load(f'{images_directory}/empty_heart.png')
                img_size = 64
                # self.image_empty_heart = pygame.transform.scale(original_empty_heart, (img_size, img_size))
                
                self.rect_empty_heart = self.image_empty_heart.get_rect()
                self.rect_empty_heart.x = self.front_image.x + 10 + i * img_size / 1.6
                if j == 0:
                    self.rect_empty_heart.y = self.front_image.y + 15
                else:
                    self.rect_empty_heart.y = self.front_image.y + 15 + img_size
                
                self.image_empty_heart_width = self.image_empty_heart.get_width()
                self.image_empty_heart_height = self.image_empty_heart.get_height()
                
                self.game.screen.blit(self.image_empty_heart, self.rect_empty_heart)
                
                # Dessine les coeurs pleins
                if i < ship.health:
                    self.image_full_heart = pygame.image.load(f'{images_directory}/full_heart.png')
                    # self.image_full_heart = pygame.transform.scale(original_full_heart, (img_size, img_size))
                    
                    self.rect_full_heart = self.image_full_heart.get_rect()
                    self.rect_full_heart.x = self.front_image.x + 10 + i * img_size / 1.6
                    if j == 0:
                        self.rect_full_heart.y = self.front_image.y + 15
                    else:
                        self.rect_full_heart.y = self.front_image.y + 15 + img_size
                    
                    self.image_full_heart_width = self.image_full_heart.get_width()
                    self.image_full_heart_height = self.image_full_heart.get_height()
                    
                    self.game.screen.blit(self.image_full_heart, self.rect_full_heart)