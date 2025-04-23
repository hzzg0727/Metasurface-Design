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


def addMaterialNK(fdtd, name, n, k, color=np.array([255 / 255, 69 / 255, 0 / 255, 1])):
    """ 
    Add material to FDTD with specified n and k
    @param fdtd: active FDTD object
    @param name: material name (string)
    @param n: refractive index (number)
    @param k: imaginary refractive index (number)
    @param color: display color for the material. Numpy array [R, G, B, alpha]. Default: np.array([255 / 255, 69 / 255, 0 / 255, 1])
    """
    temp = fdtd.addmaterial("(n,k) Material")
    fdtd.setmaterial(temp, "name", name)
    fdtd.setmaterial(name, "Refractive Index", n)
    fdtd.setmaterial(name, "Imaginary Refractive Index", k)
    fdtd.setmaterial(name, "color", color)

    
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


def getPolarizedField(e_x, e_y, polarization_angle=0):
    """ 
    Return the filed with specified polarization angle
    @param e_x: the x component of field, a ND(spacial dimension + wavelength dimension, ...) numpy array
    @param e_y: the y component of field, a ND numpy array
    @param polarization angle: polarization angle [rad]
    @return: the filed with specified polarization angle, a ND numpy array
    """
    return e_x * np.cos(polarization_angle) + e_y * np.sin(polarization_angle)


def extendField(x_vec, y_vec, e_mat, h_mat, period_x, period_y, extend_x, extend_y):
    """ 
    Return the extended filed (E and H matrix) for the period field
    @param x_vec: x vector for the period field [m]
    @param y_vec: y vector for the period field [m]
    @param e_mat: E matrix for the period field
    @param h_mat: H matrix for the period field
    @param period_x: the period along the x direction of the field [m]
    @param period_y: the period along the y direction of the field [m]
    @param extend_x: the extended number along the x direction
    @param extend_y: the extended number along the y direction
    @return: extended x_vec, y_vec, e_mat, and h_mat
    """
    len_x = len(x_vec)
    len_y = len(y_vec)
    x_extend_vec = np.zeros(len_x * extend_x, dtype=np.float_)
    y_extend_vec = np.zeros(len_y * extend_y, dtype=np.float_)
    e_extend_mat = np.zeros((len_x * extend_x, len_y * extend_y, *e_mat.shape[2:]), dtype=np.complex_)
    h_extend_mat = np.zeros((len_x * extend_x, len_y * extend_y, *h_mat.shape[2:]), dtype=np.complex_)
    for i in range(extend_x):
        x_extend_vec[i * len_x:(i + 1) * len_x] = x_vec + period_x * i
    center_x = (x_extend_vec[0] + x_extend_vec[-1]) / 2
    x_extend_vec = x_extend_vec - center_x
    for j in range(extend_y):
        y_extend_vec[j * len_y:(j + 1) * len_y] = y_vec + period_y * j
    center_y = (y_extend_vec[0] + y_extend_vec[-1]) / 2
    y_extend_vec = y_extend_vec - center_y
    for i in range(extend_x):
        for j in range(extend_y):
            e_extend_mat[i * len_x:(i + 1) * len_x, j * len_y:(j + 1) * len_y] = e_mat
            h_extend_mat[i * len_x:(i + 1) * len_x, j * len_y:(j + 1) * len_y] = h_mat
    return x_extend_vec, y_extend_vec, e_extend_mat, h_extend_mat


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


def distanceCycle(x, y, cycle_min, cycle_max, start_end=0):
    """ 
    Return the distance of two numbers with cycle rule
    @param x: number 1. `x`\in [`cycle_min`, `cycle_max`]
    @param y: number 2. `y`\in [`cycle_min`, `cycle_max`]
    @param cycle_min: min value in the cycle range
    @param cycle_max: max value in the cycle range
    @param start_end: the distance between `cycle_min` and `cycle_max`. Default: 0
    @return: distance between the numbers
    """
    assert cycle_min <= x <= cycle_max and cycle_min <= y <= cycle_max, "x, y must be in the cycle range."
    x, y = min(x, y), max(x, y)
    return min(y - x, x + cycle_max - cycle_min - y + start_end)


def phaseDis(phase1, phase2):
    """ 
    Return the absolute difference between two phases valued in (-\pi, \pi]
    @param phase1: phase 1 [rad]
    @param phase2: phase 2 [rad]
    @return: distance between the phases
    @note: make sure the value of phase is in (-\pi, \pi] in advance
    """
    return distanceCycle(phase1, phase2, -np.pi, np.pi)


def phaseNorm(phase):
    """ 
    Normalize phase number / numpy array (any dimension) to [-\pi, \pi).
    @param phase: number / Nd numpy array of phase
    @return: normalized phase number / Nd numpy array 
    """
    return np.angle(np.exp(1j * phase))


def integrate(mat, x_vec, y_vec, radius=np.inf):
    """ 
    Return the integrate of `mat` over `x_vec` and `y_vec`
    @param mat: 2D numpy array
    @param x_vec: 1D numpy array
    @param y_vec: 1D numpy array
    @param radius: only the region in the circle (centered at origin) withe the radius of `radius` will be integrated (default: np.inf)
    @return: the integrate
    """
    assert mat.shape[0] == len(x_vec) and mat.shape[1] == len(y_vec), "The dimension of the matrix and vectors don't match."

    if radius == np.inf:
        return np.sum([mat[i, j] * (x_vec[i + 1] - x_vec[i]) * (y_vec[j + 1] - y_vec[j]) \
            for i in range(len(x_vec) - 1) for j in range(len(y_vec) - 1)])
    else:
        return np.sum([mat[i, j] * (x_vec[i + 1] - x_vec[i]) * (y_vec[j + 1] - y_vec[j]) \
            for i in range(len(x_vec) - 1) for j in range(len(y_vec) - 1) if x_vec[i] ** 2 + y_vec[j] ** 2 <= radius ** 2])
    