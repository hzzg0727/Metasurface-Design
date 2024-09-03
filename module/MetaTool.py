"""
Module: Usually used functions in metasurface design.
"""

import numpy as np


def permittivity2nk(permittivity):
    """ 
    Convert from complex permittivity to (n, k)
    @param permittivity: complex value
    @return: a tuple with n and k
    """
    temp = np.sqrt(permittivity)
    return (temp.real, temp.imag)


def nk2permittivity(n, k):
    """ 
    Convert from (n, k) to complex permittivity
    @param n: the real part of complex refractive index
    @param k: the imaginary part of complex refractive index
    @return: complex permittivity
    """
    return (n + 1j * k) ** 2


def setResources(fdtd, parallel_job_number, processes, threads, capacity, job_launching_preset, clear=True, prefix=""):
    """ 
    Set resources in FDTD
    @param fdtd: fdtd object
    @param parallel_job_number: the number of the paralleled jobs
    @param processes: the processes value for each resouce
    @param threads: the threads value for each resouce
    @param capacity: the capacity value for each resouce
    @param job_launching_preset: the job launching preset for each resouce
    @param clear: whether to clear the resources defined before or not. Default: True
    @param prefix: specify the prefix label for the resource names. Default: True
    """
    if clear:
        # clear all the resources except the first one
        try:
            while True:
                fdtd.deleteresource("FDTD", 2)
        except:
            pass

    # add new resources
    for i in range(parallel_job_number):
        fdtd.addresource("FDTD")
        fdtd.setresource("FDTD", i + 2, "name", prefix + "-Resource-{}".format(i + 1))
        fdtd.setresource("FDTD", i + 2, "processes", processes)
        fdtd.setresource("FDTD", i + 2, "threads", threads)
        fdtd.setresource("FDTD", i + 2, "capacity", capacity)
        fdtd.setresource("FDTD", i + 2, "Job launching preset", job_launching_preset)

    if clear:
        # clear the first resource
        fdtd.deleteresource("FDTD", 1)


def getMatrixCenter(mat):
    """ 
    Return the center value of the matrix
    @param mat: the matrix defined with numpy 2D array
    @return: center value
    """
    w = mat.shape[0]
    l = mat.shape[1]
    if (w % 2 == 0 and l % 2 == 0):
        return (mat[round(w / 2) - 1, round(l / 2) - 1] + mat[round(w / 2) - 1, round(l / 2)] 
            + mat[round(w / 2), round(l / 2) - 1] + mat[round(w / 2), round(l / 2)]) / 4
    elif (w % 2 == 0 and l % 2 != 0):
        return (mat[round(w / 2) - 1, int(np.floor(l / 2))] + mat[round(w / 2), int(np.floor(l / 2))]) / 2
    elif (l % 2 == 0):
        return (mat[int(np.floor(w / 2)), round(l / 2) - 1] + mat[int(np.floor(w / 2)), round(l / 2)]) / 2
    else:
        return (mat[int(np.floor(w / 2)), int(np.floor(l / 2))])
    

def norm(matrix):
    """ 
    Return the MinMaxScaler normalized matrix
    @param matrix: matrix to be normalized
    @return: normalized matrix
    """
    min = np.min(matrix)
    max = np.max(matrix)
    return (matrix - min) / (max - min)

