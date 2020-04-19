from env_sim.envs.utils.agent import Agent
from env_sim.envs.utils.state import JointState
'''
he human 一样
'''

class Robot(Agent):
    def __init__(self, config, section):
        super().__init__(config, section)

    def act(self, ob):
        if self.policy is None:
            raise AttributeError('Policy attribute has to be set!')

        state = JointState(self.get_full_state(), ob)
        action = self.policy.predict(state)
        return action
