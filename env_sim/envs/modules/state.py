import torch


class FullState(object):
    def __init__(self, px, py, vx, vy, radius, gx, gy, v_pref):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.gx = gx
        self.gy = gy
        self.v_pref = v_pref

        self.position = (self.px, self.py)
        self.goal_position = (self.gx, self.gy)
        self.velocity = (self.vx, self.vy)

    # 添加
    def __add__(self, other):
        return other + (self.px, self.py, self.vx, self.vy, self.radius, self.gx, self.gy, self.v_pref)

    # toString
    def __str__(self):
        return ' '.join([str(x) for x in [self.px, self.py, self.vx, self.vy, self.radius, self.gx, self.gy,
                                          self.v_pref]])

    def to_tuple(self):
        return self.px, self.py, self.vx, self.vy, self.radius, self.gx, self.gy, self.v_pref

    # 获取可观测状态
    def get_observable_state(self):
        return ObservableState(self.px, self.py, self.vx, self.vy, self.radius)


# 可观测状态
class ObservableState(object):
    def __init__(self, px, py, vx, vy, radius):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.radius = radius

        self.position = (self.px, self.py)
        self.velocity = (self.vx, self.vy)

    def __add__(self, other):
        return other + (self.px, self.py, self.vx, self.vy, self.radius)

    def __str__(self):
        return ' '.join([str(x) for x in [self.px, self.py, self.vx, self.vy, self.radius]])

    def to_tuple(self):
        return self.px, self.py, self.vx, self.vy, self.radius


# 联合状态
class JointState(object):
    def __init__(self, self_state, agents_state):
        assert isinstance(self_state, FullState)  # 要保证是robot的全部状态
        for agent_state in agents_state:
            assert isinstance(agent_state, ObservableState)  # 断言 human的状态是可观测状态

        self.self_state = self_state
        self.agents_states = agents_state

    # to_tensor 返回 tensor 形式的状态 现在废弃了
    def to_tensor(self, add_batch_size=False, device=None):
        self_state_tensor = torch.Tensor([self.self_state.to_tuple()])
        agents_state_tensor = torch.Tensor([agent_state.to_tuple() for agent_state in self.agents_states])

        if add_batch_size:
            self_state_tensor = self_state_tensor.unsqueeze(0)
            agents_state_tensor = agents_state_tensor.unsqueeze(0)

        if device is not None:
            self_state_tensor.to(device)
            agents_state_tensor.to(device)

        return self_state_tensor, agents_state_tensor


# 将tensor形式的state 转换成joint state
def tensor_to_joint_state(state):
    robot_state, human_states = state

    robot_state = robot_state.squeeze().data.numpy()  # 变成numpy形式
    robot_state = FullState(robot_state[0], robot_state[1], robot_state[2], robot_state[3], robot_state[4],
                            robot_state[5], robot_state[6], robot_state[7], robot_state[8])
    human_states = human_states.squeeze(0).data.numpy()
    human_states = [ObservableState(human_state[0], human_state[1], human_state[2], human_state[3],
                                    human_state[4]) for human_state in human_states]

    return JointState(robot_state, human_states)
