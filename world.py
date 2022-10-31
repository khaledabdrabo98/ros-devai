#!/usr/bin/env python
# Olivier Georgeon, 2021.
# This code is used to teach Developmental AI.
# from turtlesim_enacter import TurtleSimEnacter # requires ROS
from turtlepy_enacter import TurtlePyEnacter
# from Agent5 import Agent5
from OsoyooCarEnacter import OsoyooCarEnacter
ROBOT_IP = "192.168.4.1"


class Agent:
    def __init__(self, valence_table):
        """ Creating our agent """
        self.valence_table = valence_table
        self.memory = {}
        self._action = None
        self.anticipated_outcome = None
        self.right_prediction = 0

    def action(self, outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print(" Action: " + str(self._action) +
                  ", Anticipation: " + str(self.anticipated_outcome) +
                  ", Outcome: " + str(outcome) +
                  ", Satisfaction: (anticipation: " + str(self.anticipated_outcome == outcome) +
                  ", valence: " + str(self.valence_table[self._action][outcome]) + 
                  ", ennui: " + str("??") + ")")

        """ Computing the next action to enact """
        # TODO: Implement the agent's decision mechanism
        self._action = 0
        # TODO: Implement the agent's anticipation mechanism
        self.anticipated_outcome = 0
        return self._action

    def remember(self, action, outcome):
        pass

class Agent1(Agent):
    def action(self, outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            # TRACE
            print(" Action: " + str(self._action) +
                  ", Anticipation: " + str(self.anticipated_outcome) +
                  ", Outcome: " + str(outcome) +
                  ", Satisfaction: (anticipation: " + str(self.anticipated_outcome == outcome) +
                  ", valence: " + str(self.valence_table[self._action][outcome]) + 
                  ", ennui: " + str("??") + ")")

        """ Computing the next action to enact """
        # TODO: Implement the agent's decision mechanism
        self._action = 0

        if self.anticipated_outcome == outcome:
            self.right_prediction += 1
        else:
            self.right_prediction = 0

        if self.right_prediction >= 4:
            # self._action = not self._action
            if self._action == 1:
                self._action = 0
            else:
                self._action = 1

        # TODO: Implement the agent's anticipation mechanism
        self.anticipated_outcome = 0

        if self._action in self.memory :
            self.anticipated_outcome = self.memory[self._action]

        return self._action

    def remember(self, action, outcome):
        self.memory[action] = outcome


class Environment1:
    """ In Environment 1, action 0 yields outcome 0, action 1 yields outcome 1 """
    def outcome(self, action):
        # return int(input("entre 0 1 ou 2"))
        if action == 0:
            return 0
        else:
            return 1


class Environment2:
    """ In Environment 2, action 0 yields outcome 1, action 1 yields outcome 0 """
    def outcome(self, action):
        if action == 0:
            return 1
        else:
            return 0


class Environment3:
    """ Environment 3 yields outcome 1 only when the agent alternates actions 0 and 1 """
    def __init__(self):
        """ Initializing Environment3 """
        self.previous_action = 0

    def outcome(self, action):
        _outcome = 1
        if action == self.previous_action:
            _outcome = 0
        self.previous_action = action
        return _outcome


# TODO Define the valance of interactions (action, outcome)
valences = [[-1, 1], [-1, 1]]
# valences = [[1, -1], [1, -1]]
# TODO Choose an agent
# a = Agent(valences)
a = Agent1(valences)
# a = Agent2(valences)
# a = Agent3(valences)
# a = Agent4(valences)
# a = Agent5(valences)
# TODO Choose an environment
e = Environment1()
# e = Environment2()
# e = Environment3()
# e = TurtleSimEnacter()
# e = TurtlePyEnacter()
# e = OsoyooCarEnacter(ROBOT_IP)

if __name__ == '__main__':
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    for i in range(20):
        action = a.action(outcome)
        a.remember(action, outcome)
        outcome = e.outcome(action)
