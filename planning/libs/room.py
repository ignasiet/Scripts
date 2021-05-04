import arcade

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self, width, height, size, scaling):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None
        self.screen_width  = width
        self.screen_height = height
        self.sprite_size = size
        self.sprite_scaling = scaling
        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None
    
    def setup(self, tile, background_file):
        """
        Load sprite:
        @tile: model of the tile used
        """
        # Sprite lists
        self.wall_list = arcade.SpriteList()

        # -- Set up the walls
        # Create bottom and top row of boxes
        # This y loops a list of two, the coordinate 0, and just under the top of window
        for y in (0, self.screen_height - self.sprite_size):
            # Loop for each box going across
            for x in range(0, self.screen_width, self.sprite_size):
                wall = arcade.Sprite(f":resources:images/tiles/brickGrey.png", self.sprite_scaling)
                wall.left = x
                wall.bottom = y
                self.wall_list.append(wall)

        # Create left and right column of boxes
        for x in (0, self.screen_width - self.sprite_size):
            # Loop for each box going across
            for y in range(self.sprite_size, self.screen_height - self.sprite_size, self.sprite_size):
                # Skip making a block 4 and 5 blocks up on the right side
                # if (y != self.sprite_size * 4 and y != self.sprite_size * 5) or x == 0:
                wall = arcade.Sprite(f":resources:images/tiles/brickGrey.png", self.sprite_scaling)
                wall.left = x
                wall.bottom = y
                self.wall_list.append(wall)

        

        # If you want coins or monsters in a level, then add that code here.

        # Load the background image for this level.
        self.background = arcade.load_texture(background_file)

    def addWall(self, x, y):
        # Random blocks
        wall = arcade.Sprite(f":resources:images/tiles/brickGrey.png", self.sprite_scaling)
        wall.left = x * self.sprite_size
        wall.bottom = y * self.sprite_size
        self.wall_list.append(wall)

    def addMarker(self, position: str):
        objective = arcade.Sprite(":resources:images/items/coinGold.png", self.sprite_scaling)
        # Position the coin
        objective.center_x = int(position.split(',')[0]) * self.sprite_size
        objective.center_y = int(position.split(',')[1]) * self.sprite_size
        return objective

    def loadMap(self, terrains: dict):
        walls = []
        for item in terrains:
            for k,v in item.items():
                for coordinate in v:
                    self.addWall(int(coordinate.split(',')[0]),
                                 int(coordinate.split(',')[1]))
                    walls.append(coordinate.replace(',', '-'))
        return walls

    def removeWall(self, x, y):
        # Random blocks
        for wall in self.wall_list:
            if wall.left == x * self.sprite_size and wall.bottom == y * self.sprite_size:
                self.wall_list.remove(wall)

