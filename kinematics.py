import numpy as np

class Joint:
    def __init__(self, d, theta, alpha, r, parent=None):
        self.d = d
        self.theta = theta
        self.alpha = alpha
        self.r = r

        if parent is not None:
            self.parent = parent
        else:
            self.parent = None

    def matrix(self):
        m = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 1]], dtype=float)

        m[0:3, 0:3] = self.rot()
        m[0:3, 3] = self.trans().T

        return m

    def matrix2(self):
        m = np.array([[np.cos(self.theta), -np.sin(self.theta)*np.cos(self.alpha), np.sin(self.theta)*np.sin(self.alpha), self.r*np.cos(self.theta)],
                      [np.sin(self.theta), np.cos(self.theta)*np.cos(self.alpha), -np.cos(self.theta)*np.sin(self.alpha), self.r*np.sin(self.theta)],
                      [0, np.sin(self.alpha), np.cos(self.alpha), self.d],
                      [0, 0, 0, 1]])

        return m

    def trans(self):
        translation = np.array([[self.r*np.cos(self.theta)],
                                [self.r*np.sin(self.theta)],
                                [self.d]])

        return translation

    def rot(self):
        rotation = np.array([[np.cos(self.theta), -np.sin(self.theta)*np.cos(self.alpha), np.sin(self.theta)*np.sin(self.alpha)],
                             [np.sin(self.theta), np.cos(self.theta)*np.cos(self.alpha), -np.cos(self.theta)*np.sin(self.alpha)],
                             [0, np.sin(self.alpha), np.cos(self.alpha)]])

        return rotation

    # recursively move up chain to calculate transform
    def get_transform_by_chain(self):
        if self.parent:
            return self.parent.matrix() @ self.matrix()
        else:
            return self.matrix()


class Link:
    def __init__(self, alpha, r):
        self.alpha = alpha
        self.r = r

    def matrix(self):
        m = np.array([[0, 0, 0, self.r],
                     [0, np.cos(self.alpha), -np.sin(self.alpha), 0],
                     [0, np.sin(self.alpha), np.cos(self.alpha), 0],
                     [0, 0, 0, 1]])

        return m