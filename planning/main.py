from .game import MyGame
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

    game = MyGame(config, stats)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
