# Olivier Georgeon, 2022.
# This code is used to teach Developmental AI.
# Requires:
#   - A robot Osoyoo Car https://osoyoo.com/2019/11/08/omni-direction-mecanum-wheel-robotic-kit-v1/
from WifiInterface import WifiInterface
import sys
import json


class OsoyooCarEnacter:
    def __init__(self, ip):
        # Handling the wifi connection to the robot
        self.wifiInterface = WifiInterface(ip)

    def outcome(self, action):
        """ Enacting an action and returning the outcome """
        outcome = 0
        if action in [0, 1, 2]:
            # Convert the action to command and send it to the robot
            command = ['8', '1', '3'][action]
            print("sending:", command)

            outcome_string = self.wifiInterface.enact(command)

            print("Received:", outcome_string)
            json_outcome = json.loads(outcome_string)
            # Return the outcome based on floor change
            if 'floor' in json_outcome:
                # outcome = json_outcome['floor']
                if json_outcome['floor']:
                    outcome = 1
        else:
            print("Action", action, "is not accepted")

        return outcome


# Testing the Osoyoo Car Enacter but controlling the robot from the console
if __name__ == "__main__":
    ip = "192.168.4.1"
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        print("Please provide your robot's IP address")
    print("Robot IP: " + ip)
    e = OsoyooCarEnacter(ip)

    _outcome = 0
    for i in range(10):
        _action = input("Enter action: ")
        _outcome = e.outcome(int(_action))
        print("Action: " + _action + " Outcome: " + str(_outcome))
