import arcade

# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
UPDATES_PER_FRAME = 7

# Constants used to track if the player is facing left or right

class PlayerCharacter(arcade.Sprite):
    def __init__(self,
                 width,
                 height,
                 scaling,
                 movement_speed,
                 name,
                 army):
        # Set up parent class
        super().__init__()
        # Constants used to track if the player is facing left or right
        self.screen_width = width
        self.screen_height = height
        self.right_facing = 0
        self.left_facing = 1
        self.up_facing = 2
        self.idle = 3
        self.scale = scaling
        self.attacking = False
        self.idle_texture = []
        self.dead_texture = []
        self.attack_texture = []
        self.walk_textures_up = []
        self.walk_textures_right = []
        self.walk_textures_left = []
        self.cur_texture = 0
        # Default to face-right
        self.character_face_direction = self.right_facing
        self.lateralMargin = 21
        self.verticalMargin = 29
        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-20, -28], [20, -28], [20, 28], [-20, 28]]
        self.movement_speed = movement_speed
        self.name = name
        self.army = army


    def set_walk_textures_up(self, texture):
        self.walk_textures_up=texture

    def set_walk_textures_right(self, texture):
        self.walk_textures_right=texture

    def set_walk_textures_left(self, texture):
        self.walk_textures_left=texture

    def set_idle_texture(self, texture):
        self.idle_texture=texture

    def set_dead_texture(self, texture):
        self.dead_texture=texture

    def set_attack_texture(self, texture):
        self.attack_texture=texture


    def load_sprite(self, images, target, nframes, frame, width, height, offset):
        """
        Load sprite:
        @images:  file containing the sprite sequence
        @target:  of the sprites
        @nframes: number of frames for the sprite
        @frame:   how long (in pixels) each frame is
        @width:   of the image in the frame
        @height:  of the image in the frame
        @offset:  of image wrt the frame
        """
        # images = "assets/sprites/walk_front.png"
        # width = 40
        # height = 56
        # offset = 16
        # frame = 64
        # textures = []

        for i in range(nframes):
            # self.textures.append(arcade.load_texture(images, x=offset+i*frame, y=0, width=width, height=height))
            getattr(self, target).append(arcade.load_texture(images, x=offset+i*frame, y=0, width=width, height=height))

        # return textures

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0:
            self.character_face_direction = self.left_facing
            # self.textures = self.walk_textures_left
        elif self.change_x > 0:
            self.character_face_direction = self.right_facing
            # self.textures = self.walk_textures_right
        elif self.change_y > 0 and self.change_x == 0:
            self.character_face_direction = self.up_facing
        else:
            self.character_face_direction = self.idle

        # Update current texture animation
        self.cur_texture += 1
        if self.cur_texture > 5 * UPDATES_PER_FRAME and self.attacking:
            self.cur_texture = 0
            self.attacking = False
        if self.cur_texture > 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        # Attacking animation
        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture[self.cur_texture // UPDATES_PER_FRAME]
            return

        if self.character_face_direction == self.left_facing:
            self.texture = self.walk_textures_right[self.cur_texture // UPDATES_PER_FRAME]
        elif self.character_face_direction == self.right_facing:
            self.texture = self.walk_textures_left[self.cur_texture // UPDATES_PER_FRAME]
        elif self.character_face_direction == self.up_facing:
            self.texture = self.walk_textures_up[self.cur_texture // UPDATES_PER_FRAME]
        else:
            self.texture = self.idle_texture[self.cur_texture // UPDATES_PER_FRAME]


    def setCoordenates(self, x, y):
        self.center_x = x
        self.center_y = y


    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check to see if we hit the limits of the screen
        if self.left < 0:
            self.left = 0
            self.change_x = 0 # Zero x speed
        elif self.right > self.screen_width - 1:
            self.right = self.screen_width - 1
            self.change_x = 0

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > self.screen_height - 1:
            self.top = self.screen_height - 1
            self.change_y = 0


class Attack(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):
        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()