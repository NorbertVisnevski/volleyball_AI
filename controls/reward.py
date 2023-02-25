
def calculate_reward_type1(step, actions, next_step, ai):
    for i in range(len(step[0])):
        state = step[0][i]
        next_state = next_step[0][i]
        action = actions[i]
        reward = None
        if state[4] < next_state[4]:
            reward = 10
        if i < 2 and step[1] > next_step[1]:
            reward = 100
        if i > 1 and step[2] > next_step[2]:
            reward = 100
        ai.store(state, action, reward or -1, next_state)

