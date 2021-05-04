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

from planning.libs.player import PlayerCharacter, Explosion
from planning.libs.room import Room
from planning.utils.config import ConfigFile

from planning.problems.problem import Problem
from planning.libs.actions import Actions

import time


# SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING_ROOM)

# SCREEN_WIDTH = SPRITE_SIZE * 14
# SCREEN_HEIGHT = SPRITE_SIZE * 10


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, configurations, weapons):
        self.configurations = ConfigFile(configurations)
        self.weapons = {unit['key']: unit for unit in weapons['units']}

        # Variables that will hold sprite lists
        self.player_list = None
        # Sprite lists
        self.current_room = 0

        # Set up the player
        self.rooms = None
        # self.player_sprite = None
        problem = {}
        problem['max_x'] = self.configurations.general.map.screen_width
        problem['max_y'] = self.configurations.general.map.screen_height
        problem['troops'] = []
        problem['objectives'] = []
        self.problem = ConfigFile(problem)

        self.sprite_size = int(self.configurations.general.sprite_native_size * self.configurations.general.sprite_scaling_room)
        self.screen_width = self.sprite_size * self.configurations.general.map.screen_width
        self.screen_height = self.sprite_size * self.configurations.general.map.screen_height
        self.explosion()

        super().__init__(self.screen_width,
                         self.screen_height,
                         self.configurations.general.screen_title)

        # Don't show the mouse cursor
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Create your sprites and sprite lists here
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.objectives = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.current_player = 0
        self.map_chars = {}

        i = 0
        for player in self.configurations.render:
            troop = {}
            list_positions = []
            list_index = []
            for position in player['positions']:
                player_infos = ConfigFile(self.configurations.characters[player['type']])
                self.load_player(player_infos,
                                 position)
                list_positions.append(position)
                list_index.append(i)
                i += 1
            self.map_chars[player['name']] = {"positions": list_positions,
                                              "index": list_index}
            troop['name'] = player['name']
            troop['army'] = player['army']
            troop['psyker'] = player['psyker']
            troop['position'] = position.replace(',', '-')
            troop['melee'] = player['melee']
            troop['ranged'] = player['ranged']
            troop.update(self.weapons[player['stat']])
            self.problem.troops.append(troop)

        self.total_players = len(self.player_list)-1

        self.load_rooms()

        # Create a physics engine for this room
        self.physics_engines = [
            arcade.PhysicsEngineSimple(player, self.rooms[self.current_room].wall_list)
            for player in self.player_list
        ]
        # Start AI processing
        self.aiMotor()

    def startplan(self):
        i = 0
        while i <= 20:
            self.actions.execute()
            i+=1
            time.sleep(0.5)

    def explosion(self):
        # Pre-load the animation frames. We don't do this in the __init__
        # of the explosion sprite because it
        # takes too long and would cause the game to pause.
        self.explosion_texture_list = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(file_name,
                                                              sprite_width,
                                                              sprite_height,
                                                              columns,
                                                              count)

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
        self.walls = room1.loadMap(self.configurations.general.map.terrain)
        self.rooms.append(room1)

        for objective in self.configurations.general.map.objectives:
            self.objectives.append(room1.addMarker(objective))
            self.problem.objectives.append(objective)
        print(len(self.objectives))

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
        self.objectives.draw()
        self.explosions_list.draw()
        self.bullet_list.draw()

        # Put the text on the screen.
        # output = f"Score: {self.score} \n Position: {self.player.center_x} {self.player.center_y}"
        # output = f"""
        # Number: {self.current_player}
        # Name: {self.player_list[self.current_player].name}
        # Position: {self.player_list[self.current_player].center_x} {self.player_list[self.current_player].center_y}
        # """
        output = f"Score: {self.actions.get_score()}\nPhase: {self.actions.get_phase()}\nAction: {self.actions.get_action()}"
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

        # Call update on bullet sprites
        self.bullet_list.update()
        self.explosions_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet,
                                                            self.player_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                # Make an explosion
                explosion = Explosion(self.explosion_texture_list)

                # Move it to the location of the coin
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y

                # Call update() because it sets which image we start on
                explosion.update()

                # Add to a list of sprites that are explosions
                self.explosions_list.append(explosion)
                # Get rid of the bullet
                bullet.remove_from_sprite_lists()

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

    def updateRoom(self, room):
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.rooms[room].wall_list)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        # if key == arcade.key.UP:
        #     self.player_list[self.current_player].change_y = self.player_list[self.current_player].movement_speed
        # elif key == arcade.key.DOWN:
        #     self.player_list[self.current_player].change_y = -self.player_list[self.current_player].movement_speed
        # elif key == arcade.key.LEFT:
        #     self.player_list[self.current_player].change_x = -self.player_list[self.current_player].movement_speed
        # elif key == arcade.key.RIGHT:
        #     self.player_list[self.current_player].change_x = self.player_list[self.current_player].movement_speed
        # if key == arcade.key.N:
        #     self.readPlan()

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # if key == arcade.key.UP or key == arcade.key.DOWN:
        #     self.player_list[self.current_player].change_y = 0
        # elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
        #     self.player_list[self.current_player].change_x = 0
        # elif key == arcade.key.N:
        #     self.current_player = self.current_player + 1
        #     if self.current_player >= self.total_players:
        #         self.current_player = self.current_player % self.total_players
        #     print(f"{self.current_player}:{self.total_players}")
        if key == arcade.key.N:
            self.actions.execute()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ User clicks mouse """
        self.startplan()

    def aiMotor(self):
        problem = Problem('Warhammer40k',
                          self.problem,
                          'deathguard',
                          'ultramarines',
                          self.walls)
        problem.print('planning/problems/problem_1.pddl')
        problem.solve('../downward/fast-downward.py')

        self.actions = Actions(self.player_list,
                               self.sprite_size,
                               self.bullet_list,
                               {player['name']: self.weapons[player['stat']]
                                for player in self.configurations.render})
        self.actions.map_chars = self.map_chars

