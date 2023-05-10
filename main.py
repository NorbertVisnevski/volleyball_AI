from threading import Thread

from configurations.normal import normal_game
from configurations.q_learning_1 import q_learning_self_play
from configurations.q_learning_1side import q_learning_1side, q_learning_1side_2, q_learning_1side_3, \
    q_learning_1side_4, q_learning_1side_5, q_learning_1side_r1, q_learning_1side_r2, q_learning_1side_r3, \
    q_learning_1side_7, q_learning_1side_8, q_learning_1side_r4, q_learning_1side_random, q_learning_1side_discount, \
    q_learning_1side_learning_rate, q_learning_1side_deep, q_learning_1side_after_self_play, q_learning_1side_test

if __name__ == '__main__':
    # q_learning_1side_discount(0.1)
    # q_learning_1side_discount(0.3)
    # q_learning_1side_discount(0.5)
    # q_learning_1side_discount(0.7)
    # q_learning_1side_discount(0.9)

    # q_learning_1side_learning_rate(0.2)
    # q_learning_1side_learning_rate(0.02)
    # q_learning_1side_learning_rate(0.002)
    # q_learning_1side_learning_rate(0.0002)
    # q_learning_1side_learning_rate(0.00002)
    # q_learning_self_play()
    # q_learning_1side_deep()
    # q_learning_1side_after_self_play()
    # q_learning_1side_test()
    normal_game()
