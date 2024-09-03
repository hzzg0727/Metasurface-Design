"""
Module: field propagation realization based on Lumerical FDTD API.
"""

import numpy as np
import scipy.constants as sc


class fdtd_em_dataset:
    """ 
    Lumerical FDTD rectlinear dataset for EM filed
    """
    def __init__(self):
        self.dataset = {}
        self.dataset['Lumerical_dataset'] = {
            'parameters': [[]],
            'attributes': [],
            'geometry': 'rectilinear'
        }

    
    def setWavelength(self, wavelength_vec):
        """ 
        Add parameters `lambda` and `f` to dataset
        @param wavelength_vec: 1D wavelength array [m]
        """
        self.wavelength_vec = np.array(wavelength_vec)
        self.f_vec = sc.c / self.wavelength_vec
        self.dataset['lambda'] = np.reshape(self.wavelength_vec, (len(wavelength_vec), 1))
        # allow modify
        if not 'lambda' in self.dataset['Lumerical_dataset']['parameters']:
            self.dataset['Lumerical_dataset']['parameters'][0].append('lambda')
        self.dataset['f'] = sc.c / self.dataset['lambda']
        if not 'f' in self.dataset['Lumerical_dataset']['parameters']:
            self.dataset['Lumerical_dataset']['parameters'][0].append('f')


    def setRegion(self, x_vec, y_vec, z_vec):
        """
        Add `x`, `y` and `z` to dataset
        @param x_vec: 1D X array [m]
        @param y_vec: 1D Y array [m]
        @param z_vec: 1D Z array [m]
        """
        self.x_vec = np.array(x_vec)
        self.y_vec = np.array(y_vec)
        self.z_vec = np.array(z_vec)
        self.dataset['x'] = np.reshape(self.x_vec, (len(x_vec), 1))
        self.dataset['y'] = np.reshape(self.y_vec, (len(y_vec), 1))
        self.dataset['z'] = np.reshape(self.z_vec, (len(z_vec), 1))


    def setX(self, x_vec):
        """
        Add `x` to dataset
        @param x_vec: 1D X array [m]
        """
        self.x_vec = np.array(x_vec)
        self.dataset['x'] = np.reshape(self.x_vec, (len(x_vec), 1))


    def setY(self, y_vec):
        """
        Add `y` to dataset
        @param y_vec: 1D Y array [m]
        """
        self.y_vec = np.array(y_vec)
        self.dataset['y'] = np.reshape(self.y_vec, (len(y_vec), 1))


    def setZ(self, z_vec):
        """
        Add `z` to dataset
        @param z_vec: 1D Z array [m]
        """
        self.z_vec = np.array(z_vec)
        self.dataset['z'] = np.reshape(self.z_vec, (len(z_vec), 1))

    
    def setE(self, e_mat):
        """ 
        Add attribute `E` to dataset
        @param e_mat: E matrix
        """
        assert e_mat.shape == (len(self.x_vec), len(self.y_vec), len(self.z_vec), len(self.wavelength_vec), 3), \
            "Unmatched data shape: {} and {}".format(e_mat.shape, (len(self.x_vec), \
                len(self.y_vec), len(self.z_vec), len(self.wavelength_vec), 3))
        self.e_mat = np.array(e_mat)
        self.dataset['E'] = self.e_mat
        # allow modify
        if not 'E' in self.dataset['Lumerical_dataset']['attributes']:
            self.dataset['Lumerical_dataset']['attributes'].append('E')
    

    def setH(self, h_mat):
        """ 
        Add attribute `H` to dataset
        @param e_mat: H matrix
        """
        assert h_mat.shape == (len(self.x_vec), len(self.y_vec), len(self.z_vec), len(self.wavelength_vec), 3), \
            "Unmatched data shape: {} and {}".format(h_mat.shape, (len(self.x_vec), \
                len(self.y_vec), len(self.z_vec), len(self.wavelength_vec), 3))
        self.h_mat = np.array(h_mat)
        self.dataset['H'] = self.h_mat
        # allow modify
        if not 'H' in self.dataset['Lumerical_dataset']['attributes']:
            self.dataset['Lumerical_dataset']['attributes'].append('H')


    def getDataset(self):
        """ 
        Return the dataset
        """
        return self.dataset


class em_field:
    """
    EM filed dataset
    """
    def __init__(self, wavelength_vec=None, x_vec=None, y_vec=None, z_vec=None, e_mat=None, h_mat=None):
        self.field = {
            'wavelength_vec': np.array(wavelength_vec),
            'x_vec': np.array(x_vec),
            'y_vec': np.array(y_vec),
            'z_vec': np.array(z_vec),
            'e_mat': np.array(e_mat),
            'h_mat': np.array(h_mat)
        }


    def setWavelength(self, wavelength_vec):
        self.field['wavelength_vec'] = wavelength_vec


    def getWavelength(self):
        return self.field['wavelength_vec']


    def setX(self, x_vec):
        self.field['x_vec'] = x_vec


    def getX(self):
        return self.field['x_vec']


    def setY(self, y_vec):
        self.field['y_vec'] = y_vec


    def getY(self):
        return self.field['y_vec']


    def setZ(self, z_vec):
        self.field['z_vec'] = z_vec


    def getZ(self):
        return self.field['z_vec']
    

    def setRegion(self, x_vec, y_vec, z_vec):
        self.setX(x_vec)
        self.setX(y_vec)
        self.setX(z_vec)


    def setE(self, e_mat):
        self.field['e_mat'] = e_mat


    def getE(self):
        """ 
        E [X, Y, Z, Wavelengths, 3]
        """
        return self.field['e_mat']

    
    def setH(self, h_mat):
        self.field['h_mat'] = h_mat


    def getH(self):
        """ 
        H [X, Y, Z, Wavelengths, 3]
        """
        return self.field['h_mat']


    def toFdtdDataset(self):
        ds = fdtd_em_dataset()
        ds.setWavelength(self.field['wavelength_vec'])
        ds.setRegion(self.field['x_vec'], self.field['y_vec'], self.field['z_vec'])
        ds.setE(self.field['e_mat'])
        ds.setH(self.field['h_mat'])
        return ds.dataset


def fieldPropagationLumapi(field: em_field, dest_x_vec, dest_y_vec, dest_z_vec, wavelength_index_vec=None, index=1, fdtd=None):
    """ 
    Field propagation realized with Lumerical FDTD script
    @param field: source field (class: `em_field`)
    @param dest_x_vec: x destination region [m]
    @param dest_y_vec: y destination region [m]
    @param dest_z_vec: z destination region [m]
    @param wavelength_index_vec: the wavelength index vector for the wavelengths to be propagated. \
        Default: None, and it means choose all
    @param index: refractive index of the background material. Default: 1
    @param fdtd: FDTD object used by method #0.
    @return: E field matrix in destination region [X, Y, Z, 3, Wavelengths]
    """
    if wavelength_index_vec is None:
        wavelength_index_vec = np.arange(0, len(field.getWavelength()))
    elif len(wavelength_index_vec) == 0:
        return em_field()
    else:
        wavelength_index_vec = np.array(wavelength_index_vec)
    fld = em_field(
        field.getWavelength(),
        field.getX(),
        field.getY(),
        field.getZ(),
        field.getE()[:, :, :, :, :],
        field.getH()[:, :, :, :, :]
    )
    # FDTD farfieldexact3d
    assert fdtd != None, "FDTD must be given"
    far_field = fdtd.farfieldexact3d(fld.toFdtdDataset(), \
        np.array(dest_x_vec), np.array(dest_y_vec), np.array(dest_z_vec), wavelength_index_vec + 1, index)
    return far_field if len(wavelength_index_vec) > 1 else np.reshape(far_field, (*far_field.shape, 1))
