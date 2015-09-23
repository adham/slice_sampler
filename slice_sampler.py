# import necesarry packages

import numpy as np

def I_doubling(f, x0, w=1, p=20):
    """
    doubling procedure for finding an appropriate interval around
    the current point

    TODO: different dimensions can have differnt ws and ps
    pass an array instead os scalar for w and p

    """

    y0 = f(x0)
    y = np.random.uniform(0, y0)
    U = np.random.uniform(0, 1, size=len(x0))
    L = x0 - w*U
    R = L + w
    K = p

    """
    TODO: it might be possible to increase dimensions separately to cover
    as much as possible
    """
    while K>0 and (y<f(L) or y<f(R)):
        V = np.random.uniform(0, 1)
        if V<0.5:
            L = L - (R - L)
        else:
            R = R + (R - L)
        K = K - 1

    return L, R, y

#%%

def I_stepping_out1(f, x0, w=1, m=1000):
    """
    stepping out procedure for finding an appropriate interval around
    the current point
    """
    y0 = f(x0)
    y = np.random.uniform(0, y0)
    U = np.random.uniform(0, 1, size=len(x0))
    L = x0 - U*w
    R = L + w

    V = np.random.uniform(0, 1)
    J = np.floor(m*V)
    K = (m-1) - J

    while J>0 and y<f(L):
        L = L - w
        J = J - 1
    while K>0 and y<f(R):
        R = R + w
        K = K - 1

    return L, R, y

def I_stepping_out2(f, x0, w=1, m=100):

    n_dim = len(x0)
    y0 = f(x0)
    y = np.random.uniform(0, y0)
    U = np.random.uniform(0, 1, size=len(x0))
    L = x0 - U*w
    R = L + w

    V = np.random.uniform(0, 1, size=n_dim)
    J = np.floor(m*V)
    K = (m-1) - J

    for dim in xrange(n_dim):
        while J[dim]>0 and y<f(L):
            L[dim] -= w
            J[dim] -= 1
        while K[dim]>0 and y<f(R):
            R[dim] += w
            K[dim] -= 1

    return L, R, y