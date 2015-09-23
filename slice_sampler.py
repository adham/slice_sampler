# -*- coding: utf-8 -*-
"""
slice_sampler.py

Adham Beyki, odinay@gmail.com
"""

# import necessary packages

import numpy as np

"""
TODO: different dimensions can have different ws and ps
pass an array instead of scalar for w and p
"""


def I_stepping_out(f, x0, w=1, m=1000, n_dim=1, all_dim=True):
    """
    stepping out procedure for finding an appropriate interval around
    the current point
    """
    y0 = f(x0)
    y = np.random.uniform(0, y0)
    U = np.random.uniform(0, 1, size=n_dim)
    L = x0 - U*w
    R = L + w

    # stepping out of dimensions all together
    if all_dim:
        V = np.random.uniform(0, 1)
        J = np.floor(m*V)
        K = (m-1) - J

        while J>0 and y<f(L):
            L -= w
            J -= 1
        while K>0 and y<f(R):
            R += w
            K -= 1

        return L, R, y

    # stepping out of dimensions one by one
    else:
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

def I_doubling(f, x0, w=1, p=20, n_dim=1, all_dim=True):
    """
    doubling procedure for finding an appropriate interval around
    the current point
    """

    y0 = f(x0)
    y = np.random.uniform(0, y0)
    U = np.random.uniform(0, 1, size=n_dim)
    L = x0 - w*U
    R = L + w
    K = p

    # doubling dimensions all together
    if all_dim:
        while K>0 and (y<f(L) or y<f(R)):
            V = np.random.uniform(0, 1)
            if V < 0.5:
                L -= R - L
            else:
                R += R - L
            K -= 1

        return L, R, y

    # doubling dimensions one by one
    else:
        for dim in xrange(n_dim):
            K = p
            while K>0 and (y<f(L) or y<f(R)):
                V = np.random.uniform(0, 1)
                if V < 0.5:
                    L[dim] -= R[dim] - L[dim]
                else:
                    R[dim] += R[dim] - L[dim]
                K -= 1
        return L, R, y

def accept_doubling(f, x0, x1, y, w, L, R, n_dim=1):
    """
    checks if the proposal in doubling procedure is acceptable or not
    """

    for dim in xrange(n_dim):
        D = False
        while (R[dim] - L[dim]) > 1.1*w:
            M = (R[dim] + L[dim]) / 2

            if (x0[dim]<M and x1[dim]>=M) or (x0[dim]>=M and x1[dim]<M):
                D = True
            if x1[dim] < M:
                R[dim] = M
            else:
                L[dim] = M

            if D and y>=f(L) and y>=f(R):
                return False
    return True

def slice_sampler_stepping_out(f, x0, n_samples, w, m, n_dim=1, all_dim=True):

    n_dim = len(x0)
    samples = np.zeros([n_samples, n_dim])

    for i in xrange(n_samples):
        while True:
            L, R, y = I_stepping_out(f, x0, w, m, n_dim, all_dim)
            x1 = np.random.uniform(L, R, [1, n_dim])[0]

            if f(x1) > y:
                break

            mask = x1<x0
            L[mask] = x1[mask]
            mask = x1>x0
            R[mask] = x1[mask]
        x0 = x1
        samples[i] = x0
    return samples


def slice_sampler_doubling(f, x0, n_samples, w, p, all_dim=True):

    n_dim = len(x0)
    samples = np.zeros([n_samples, n_dim])

    for i in xrange(n_samples):
        while True:
            L, R, y = I_doubling(f, x0, w, p, n_dim, all_dim)
            x1 = np.random.uniform(L, R, [1, n_dim])[0]


            if f(x1) > y and accept_doubling(f, x0, x1, y, w, L, R, n_dim):
                break

            mask = x1<x0
            L[mask] = x1[mask]
            mask = x1>x0
            R[mask] = x1[mask]

        x0 = x1
        samples[i] = x0
    return samples


def slice_sampler(f, x0, n_samples, w, doubling=True, m=50, p=20, all_dim=True):
    if doubling:
        return slice_sampler_doubling(f, x0, n_samples, w, p, all_dim)
    else:
        return slice_sampler_stepping_out(f, x0, n_samples, w, m, all_dim)