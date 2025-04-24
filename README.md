# Metasurface-design

## Introduction

Fundamental metasurface design workflows realized with Python (notebook) based on Lumerical FDTD API. 
Code for paper [Fundamentals to emerging concepts and applications of metasurface for flat optics: a multifaceted tutorial]().  <!-- NOTE -->
This repository will be continuously maintained and updated. 
Welcome for your star!

**Important notes** <!-- NOTE -->

*The paper is still not published.*

A major advantage of the design demos we provide is that 
the entire metasurface design and analysis process can be carried out within the Python environment, 
offering a highly efficient, flexible, convenient, and automated workflow. 

Here we use [Lumerical FDTD](https://www.ansys.com/products/optics/fdtd) for electromagnetic simulation. 
However, Lumerical FDTD is not the only option available. 
You can also consider alternatives like [Meep](https://meep.readthedocs.io/en/master/), 
[Lumerical RCWA](https://optics.ansys.com/hc/en-us/articles/4414567728787-RCWA-Product-Reference-Manual), 
or [S4](https://web.stanford.edu/group/fan/S4/). 

In the following, 
we will introduce demos for various metasurface designs, 
each accompanied by a corresponding notebook file located in the [notebook](notebook/) directory.

### Propagation phase metasurface design

In this demo, we realize the propagation phase metasurface design workflow, 
from building the meta-atom library to the arrangement of meta-atoms on the substrate. 
We note that resonant phase metasurfaces share the similar workflow with propagation phase metasurfaces. 
The GDS file export method for propagation phase metasurfaces is also provided. 

### Geometric phase metasurface design

In this demo, we realize the geometric phase metasurface design workflow, 
from finding the meta-atom with the highest transmittance and polarization conversion efficiency 
to the arrangement of meta-atoms on the substrate. 
The GDS file export method for geometric phase metasurfaces is also provided. 

### Metagrating design and analysis

In this demo, we design a polarization-insensitive metagrating based on propagation phase modulation mechanism. 
The meta-atom library is built using the propagation phase metasurface design workflow above. 
The performance of the metagrating is also analyzed. 

### Metalens design and analysis

In this demo, we design a polarization-insensitive metalens based on propagation phase modulation mechanism. 
The meta-atom library is built using the propagation phase metasurface design workflow above. 
The performance of the metalens is also analyzed. 

### Metasurface hologram design and analysis

In this demo, we design a polarization-insensitive metasurface hologram based on propagation phase modulation mechanism. 
The meta-atom library is built using the propagation phase metasurface design workflow above. 
The performance of the metasurface hologram is also analyzed. 

### Design and analysis of the metasurface for vortex generation

In this demo, we design a polarization-insensitive metasurface for vortex generation 
based on propagation phase modulation mechanism. 
The meta-atom library is built using the propagation phase metasurface design workflow above. 
The performance of the metasurface is also analyzed. 

### Quasi-symmetry-protected BIC metasurface design

In this demo, we design a quasi-symmetry-protected BIC metasurface using two tilted ellipse meta-atoms. 
The Fano fitting for solving the quality factor is also demonstrated. 

### Computer generated hologram 

In this demo, we realize the Gerchberg–Saxton algorithm (GS algorithm), 
which is usually used for solving the phase distribution of the phase-only metasurface hologram. 
Furthermore, we also realize the distortion and intensity correction algorithms for wide-FOV holography, 
which are proposed in the Subsection 5.1.2 of the [paper]().  <!-- NOTE -->

## File structure

The main directories we use are explained as follows. 

### [data](data/)

The `data` directory contains the input and output data in metasurface design, 
including the meta-atom library, the target holographic image, 
the phase distribution of the hologram solved by the GS algorithm, etc. 

### [fsp](fsp/)

The `fsp` directory contains the simulation files of Lumerical FDTD. 

### [layout](layout/)

The `layout` directory contains the GDS (Graphic Data System) files of metasurfaces. 

### [material](material/)

The `material` directory contains the material data (wavelength, refractive index, and extinction coefficient), 
which will be imported into Lumerical FDTD in the design. 

*The TiO2 data in the directory is obtained from [RefractiveIndex.INFO website](https://refractiveindex.info/).*

### [module](module/)

The `module` directory contains two python modules, which are used over and over again in the metasurface design. 
The files in this directory are as follows.

1. [FieldPropagation.py](module/FieldPropagation.py): Field propagation function based on Lumerical FDTD API
2. [MetaTool.py](module/MetaTool.py): Several useful functions in metasurface design.

### [notebook](notebook/)

The `notebook` directory contains our workflows for metasurface design. 
The files in this directory are as follows.

1. [GeometricPhaseMetasurface.ipynb](notebook/GeometricPhaseMetasurface.ipynb): Workflow for geometric phase metasurface design.
2. [PropagationPhaseMetasurface.ipynb](notebook/PropagationPhaseMetasurface.ipynb): Workflow for propagation phase metasurface design.
3. [Metagrating.ipynb](notebook/MetagratingDesign.ipynb): Workflow for the design and analysis of the metagrating.
4. [MetalensDesign.ipynb](notebook/MetalensDesign.ipynb): Workflow for the design and analysis of the metalens.
5. [MetasurfaceHologramDesign.ipynb](notebook/MetasurfaceHologramDesign.ipynb): Workflow for the design and analysis of the metasurface hologram.
6. [MetasurfaceVortexDesign.ipynb](notebook/MetasurfaceVortexDesign.ipynb): Workflow for the design and analysis of the metasurface for vortex generation.
7. [SymmetryProtectedBICMetasurface.ipynb](notebook/SymmetryProtectedBICMetasurface.ipynb): Workflow for the design and analysis of the quasi-symmetry-protected metasurface.
8. [ComputerGeneratedHologram.ipynb](notebook/ComputerGeneratedHologram.ipynb): Realization of computer generated hologram algorithms. 

## How to use it?

All the code is written in Python and organized within Jupyter notebooks. 
To get started, you need to have both Python and Jupyter Notebook installed on your system.

**Important notes**

In our tests, 
for some old versions of Lumerical FDTD, 
in order to use the python API, 
the python version of the environment should not be higher than 3.9.0. 

We use the following codes to import `lumapi` of Lumerical FDTD. 

```python
import importlib.util
# import lumapi
spec = importlib.util.spec_from_file_location('lumapi', 'D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py')
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)
```

Please ensure that the path to the `lumapi.py` file is adjusted to match your specific directory. 

**References and Additional Resources**

- Official Jupyter Documentation: [Jupyter.org](https://jupyter.org/documentation)
- Python Documentation: [Python.org](https://docs.python.org/3/)

These resources will provide you with more detailed instructions and guidance on using Python and Jupyter Notebook effectively. 

## Credits
If you use any of these codes in your research or work, please cite our paper:

> Gao Y., Ma Y. Fundamentals to frontiers of metasurface for flat optics: a multifaceted tutorial. 
> [[bibtex](article.bib)] <!-- NOTE -->

## Author information

The personal page of the code author (Yubin Gao) can be found [here](https://hzzg0727.github.io/).

The website of our group (NanoOptics Group in Zhejiang University) can be found [here](http://10.12.15.222/index).

## Questions and feedback

If you have any questions or bug reports, 
please use the [Issues](https://github.com/hzzg0727/Metasurface-Design/issues) section to report them. 
