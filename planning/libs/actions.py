import arcade
import math
from .plan import Plan
from Genetic.rollsimulator import roll

BULLET_SPEED = 5
SPRITE_SCALING_LASER = 0.8


class Actions():
    def __init__(self,
                 player_list,
                 size,
                 bullets,
                 stats):
        self.stored_commands = []
        self.current_action = "Reading plan"
        self.phases = ['Movement',
                       'Psychic',
                       'Shooting Phase',
                       'Combat Phase']
        self.current_phase = 0
        self.line_counter = 0

        self.walls = []
        self.plan = []
        self.score = 0

        self.map_chars = {}
        self.sprite_size = size
        self.player_list = player_list
        self.bullet_list = bullets
        self.player_sheet = stats
        # # 0 phase - move
        # self.allowed_orders[0] = ['move', 'hold']
        # # 1 phase - psyker
        # self.allowed_orders[1] = ['smite']
        # # 2 phase - shoot
        # self.allowed_orders[2] = ['shot', 'kill']
        self.plan = Plan()
        # with open('sas_plan', 'r') as f:
        #     for line in f:
        #         self.plan.append(line)

    def get_score(self):
        return self.score

    def get_phase(self):
        return self.phases[self.current_phase]

    def get_action(self):
        return self.current_action

    def readPlan(self):
        try:
            action = self.plan.readPlan(self.current_phase,
                                        self.line_counter)
            # s = self.plan[self.line_counter]
            self.line_counter += 1
            # print(s.strip("\n"))
            self.current_action = action[0]
            if action[0].startswith(';'):
                return "comment"
            return action
        except Exception:
            self.current_phase += 1
            self.line_counter = 0
            return "eop"

    def execute(self):
        command = self.readPlan()
        if command == "eop":
            print("Plan finished")
            return
        if command == "comment":
            print("Detected comment")
            return
        print(command)
        getattr(self, command[0])(command)

    def hold(self, order):
        self.score += 1

    def move(self, order):
        unit = self.map_chars[order[1]]
        for troop in unit['index']:
            _from = order[2]
            from_x = int(_from.split('-')[0])
            from_y = int(_from.split('-')[1])

            to = order[3]
            to_x = int(to.split('-')[0])
            to_y = int(to.split('-')[1])

            diff_x = to_x - from_x
            diff_y = to_y - from_y
            self.player_list[troop].center_x += diff_x * self.sprite_size
            self.player_list[troop].center_y += diff_y * self.sprite_size

    def smite(self, order):
        # Create a bullet
        bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", SPRITE_SCALING_LASER)
        # shooter = self.map_chars[order[1]]
        target = self.map_chars[order[2]]['index'][0]
        # Position the bullet at the player's current location
        for shooter in self.map_chars[order[1]]['index']:
            start_x = self.player_list[shooter].center_x + self.sprite_size
            start_y = self.player_list[shooter].center_y + self.sprite_size

            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            dest_x = self.player_list[target].center_x
            dest_y = self.player_list[target].center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            bullet_angle = math.tan(x_diff/y_diff)
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            # bullet.angle = angle
            bullet.angle = math.degrees(bullet_angle) - 90
            print(f"Bullet angle: {bullet.angle:.2f}")

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    def shot(self, order):
        # Create a bullet
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)
        # shooter = self.map_chars[order[1]]
        target = self.map_chars[order[2]]['index'][0]

        # Position the bullet at the player's current location
        for shooter in self.map_chars[order[1]]['index']:
            start_x = self.player_list[shooter].center_x + self.sprite_size
            start_y = self.player_list[shooter].center_y + self.sprite_size

            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            dest_x = self.player_list[target].center_x
            dest_y = self.player_list[target].center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            bullet_angle = math.tan(x_diff/y_diff)
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            bullet.angle = math.degrees(bullet_angle) - 90
            print(f"Bullet angle: {bullet.angle:.2f}")

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    def kill(self, order):
        dice = roll(2)
        result = sum(dice)
        targets = self.map_chars[order[2]]['positions']
        attackers = self.map_chars[order[1]]['positions']

        # get minimal distance between attacker and target
        for target in targets:
            x_1 = int(target.split(',')[0])
            y_1 = int(target.split(',')[1])
            for attacker in attackers:
                x_2 = int(attacker.split(',')[0])
                y_2 = int(attacker.split(',')[1])
                if (abs(x_1-x_2) + (abs(y_1-y_2))) <= result:
                    print("Successfull charge!")
                    return
        print("Unsuccessfull charge!")
