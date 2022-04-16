class SpriteSheet():

    def __init__(self, image, rows, cols):
        self.spritesheet = image
        self.width = self.spritesheet.get_width()
        self.height = self.spritesheet.get_height()
        self.rows = rows
        self.cols = cols
        self.sqWidth = self.width / cols
        self.sqHeight = self.height / rows

    def getSubImageByIndex(self, row, col):
        subimage = self.spritesheet.subsurface(self.spritesheet.get_rect(topleft=(col * self.sqWidth, row * self.sqHeight), size=(self.sqWidth, self.sqHeight)))
        return subimage