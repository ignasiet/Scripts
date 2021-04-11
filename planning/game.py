"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random
import yaml

from planning.libs.player import PlayerCharacter
from planning.libs.room import Room
from planning.utils.config import ConfigFile

# SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING_ROOM)

# SCREEN_WIDTH = SPRITE_SIZE * 14
# SCREEN_HEIGHT = SPRITE_SIZE * 10



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, configurations):
        
        self.configurations = ConfigFile(configurations)
        # Variables that will hold sprite lists
        self.player_list = None
        # Sprite lists
        self.current_room = 0

        # Set up the player
        self.rooms = None
        # self.player_sprite = None
        self.score = 0
        self.sprite_size = int(self.configurations.general.sprite_native_size * self.configurations.general.sprite_scaling_room)
        self.screen_width = self.sprite_size * self.configurations.general.map.screen_width
        self.screen_height = self.sprite_size * self.configurations.general.map.screen_height

        super().__init__(self.screen_width, self.screen_height, self.configurations.general.screen_title)

        # Don't show the mouse cursor
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Create your sprites and sprite lists here
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.current_player = 0
        
        
        for player in self.configurations.render:
            print(player)
            for position in player['positions']:
                self.load_player(ConfigFile(self.configurations.characters[player['type']]),
                                 position)
        
        self.total_players = len(self.player_list)-1

        self.load_rooms()

        # Create a physics engine for this room
        self.physics_engines = [
            arcade.PhysicsEngineSimple(player, self.rooms[self.current_room].wall_list)
            for player in self.player_list
        ]

    def load_rooms(self):
        # Create the rooms
        # Our list of rooms
        self.rooms = []
        # Create the rooms. Extend the pattern for each room.
        room1 = Room(self.screen_width,
                     self.screen_height,
                     self.sprite_size,
                     self.configurations.general.sprite_scaling_room)
        room1.setup("brickGrey.png", "planning/assets/backgrounds/black1.png")
        # room1.addWall(6,5)
        # room1.addWall(7,6)
        # room1.addWall(7,5)
        # room1.addWall(7,4)
        # room1.addWall(7,3)
        room1.loadMap(self.configurations.general.map.terrain)
        self.rooms.append(room1)

        # Our starting room number1
        self.current_room = 0


    def load_player(self, player_infos, position):
        player = PlayerCharacter(self.screen_width,
                                 self.screen_height,
                                 player_infos.sprite_scaling_player,
                                 player_infos.movement_speed,
                                 player_infos.name)
        # Load textures of the sprite
        if 'textures' not in player_infos.data:
            raise Exception('No textures for the player found')
        for texture in player_infos.textures:
            player.load_sprite(texture['file'], 
                               texture['name'],
                               texture['nframes'],
                               texture['frame'],
                               texture['width'],
                               texture['height'],
                               texture['offset'])
        player.textures = player.textures + player.idle_texture

        # self.player.textures = []
        # for i in range(9):
        #     self.player.textures.append(arcade.load_texture("assets/sprites/walk_front.png", x=16+i*64, y=0, width=40, height=56))
        player.textures.append(player.idle_texture)
        # self.coin_list = arcade.SpriteList()

        # Set up the player
        x_coordinate = self.sprite_size * int(position.split(',')[0])
        y_coordinate = self.sprite_size * int(position.split(',')[1])
        player.setCoordenates(x_coordinate,
                              y_coordinate)
        self.player_list.append(player)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        # Call draw() on all your sprite lists below
        """ Draw everything """
        arcade.start_render()
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0,
                                            0,
                                            self.screen_width,
                                            self.screen_height,
                                            self.rooms[self.current_room].background)

        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        # output = f"Score: {self.score} \n Position: {self.player.center_x} {self.player.center_y}"
        output = f"""
        Number: {self.current_player}
        Name: {self.player_list[self.current_player].name}
        Position: {self.player_list[self.current_player].center_x} {self.player_list[self.current_player].center_y}"""
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        """ Movement and game logic """
        for physicsEngine in self.physics_engines:
            physicsEngine.update()
        # Call update on all sprites 
        self.player_list.update()
        self.player_list.update_animation()
        
    def updateRoom(self, room):    
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.rooms[room].wall_list)
    

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.UP:
            self.player_list[self.current_player].change_y = self.player_list[self.current_player].movement_speed
        elif key == arcade.key.DOWN:
            self.player_list[self.current_player].change_y = -self.player_list[self.current_player].movement_speed
        elif key == arcade.key.LEFT:
            self.player_list[self.current_player].change_x = -self.player_list[self.current_player].movement_speed
        elif key == arcade.key.RIGHT:
            self.player_list[self.current_player].change_x = self.player_list[self.current_player].movement_speed
        # elif key == arcade.key.N:
        #     self.current_player = self.current_player % self.total_players


    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_list[self.current_player].change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_list[self.current_player].change_x = 0
        elif key == arcade.key.N:
            self.current_player = self.current_player + 1
            if self.current_player >= self.total_players:
                self.current_player = self.current_player % self.total_players
            print(f"{self.current_player}:{self.total_players}")



def main():
    """ Main method """
    # instantiate
    with open("planning/assets/games/game1.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    
    configurations = ConfigFile(config)
    game = MyGame(config)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()