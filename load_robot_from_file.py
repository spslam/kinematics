from kinematics import Joint


def load_robot():
    robot = []

    with open('joint_params.txt') as file:
        for row in file.readlines():
            v = row.split()
            v = [float(x) for x in v]
            d = {'theta': v[0], 'r': v[1], 'd': v[2], 'alpha': v[3]}

            # check if it's the first joint (empty list) -- otherwise make parent the previous joint
            if robot:
                parent = robot[-1]
            else:
                parent = None

            j = Joint(d['d'], d['theta'], d['alpha'], d['r'], parent=parent)
            robot.append(j)

    return robot
