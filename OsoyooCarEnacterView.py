# Olivier Georgeon, 2021.
# This code is used to teach Developmental AI.
# Requires:
#   - A robot Osoyoo Car https://osoyoo.com/2019/11/08/omni-direction-mecanum-wheel-robotic-kit-v1/
#   - Project https://github.com/OlivierGeorgeon/osoyoo
#       (Tested with commit dcc64a2 January 23th 2022)
#   - Python libraries pyglet and keyboard
from EgoMemoryWindow import EgoMemoryWindow
from Controller import Controller
# import pyglet
import json


class OsoyooCarEnacter:
    def __init__(self):
        # Instantiating the robot's egocentric spatial memory window
        self.osoyoo_car_window = EgoMemoryWindow(600)
        self.osoyoo_car_window.zoom_level = 2

        # The controller
        self.controller = Controller(self.osoyoo_car_window)

        self.osoyoo_car_window.dispatch_events()
        self.osoyoo_car_window.on_draw()
        self.osoyoo_car_window.flip()

    def outcome(self, action):
        """ Enacting an action and returning the outcome """
        # Trigger the asynchronous communication
        if action == 0:
            self.controller.enact('8')
        if action == 1:
            self.controller.enact('1')
        if action > 1:
            self.controller.enact('3')

        # Wait for the outcome while processing pyglet events
        while self.controller.enact_step < 2:
            # Inspired by https://stackoverflow.com/questions/61217265/
            # pyglet.clock.tick()
            self.osoyoo_car_window.dispatch_events()
            self.osoyoo_car_window.on_draw()
            self.osoyoo_car_window.flip()

        # Update the Egocentric Memory Window
        self.controller.update_model()
        self.controller.enact_step = 0
        # pyglet.clock.tick()
        self.osoyoo_car_window.dispatch_events()
        self.osoyoo_car_window.on_draw()
        self.osoyoo_car_window.flip()

        # Return the outcome based on floor change
        outcome = 0
        json_outcome = json.loads(self.controller.outcome_string)
        if 'floor' in json_outcome:
            outcome = json_outcome['floor']

        return int(outcome)


# Testing the Osoyoo Car Enacter but controlling the robot from the console
if __name__ == "__main__":
    e = OsoyooCarEnacter()

    _outcome = 0
    for i in range(10):
        _action = input("Enter action: ")
        _outcome = e.outcome(int(_action))
        print("Action: " + _action + " Outcome: " + str(_outcome))
