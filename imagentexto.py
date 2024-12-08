# Personaliced class with a button and text to the rigth
class ImageTextButton:
    def __init__(self,x,y,image,text,font,text_color,padding=10):
        self.image = image
        self.text = text
        self.font = font
        self.text_color = text_color
        self.padding = padding

        #create rectangles for images and text
        self.image_rect = self.image.get_rect(topleft=(x,y))
        text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = text_surf.get_rect(topleft=(self.image_rect.right + self.padding, y))

        # define total area of the button
        self.rect = self.image_rect.union(self.text_rect)

    def draw(self, surface):
        #draw image and text
        surface.blit(self.image,self.image_rect)
        text_surf = self.font.render(self.text,True ,self.text_color)
        surface.blit(text_surf, self.text_rect)

    def is_clicked(self,pos):
        return self.rect.collidepoint(pos)