from .game import MyGame, InstructionView
import yaml
import arcade
from planning.utils.config import ConfigFile

def main():
    """ Main method """
    # instantiate
    with open("planning/assets/games/game1.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    with open("planning/assets/games/stats.yaml", 'r') as stream:
        stats = yaml.safe_load(stream)
    
    configurations = ConfigFile(config)
    sprite_size = int(configurations.general.sprite_native_size * configurations.general.sprite_scaling_room)
    screen_width = sprite_size * configurations.general.map.screen_width
    screen_height = sprite_size * configurations.general.map.screen_height
    window = arcade.Window(screen_width,
                           screen_height,
                           configurations.general.screen_title)
    start_view = InstructionView(screen_width, screen_height, stats, config)
    window.show_view(start_view)
    # start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
