# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      temporal_transformation.py                         ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: Branly, Tran Quoc <->                          ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://github.com/StephaneBranly              +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2022/05/31 18:39:05 by Branly, Tran Quoc   ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import math


def linear_to_cyclic_cos(value, range):
    return math.cos(value / range * math.pi * 2)


def linear_to_cyclic_sin(value, range):
    return math.sin(value / range * math.pi * 2)


def cyclic_to_theta(x, y):
    tmp = math.atan2(y, x)
    return tmp if tmp >= 0 else tmp + 2 * math.pi


def cyclic_to_radius(x, y):
    return math.sqrt(y * y + x * x)
