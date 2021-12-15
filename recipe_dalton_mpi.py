"""
HPCCM recipe for DALTON image (MPI)

Contents:
  Ubuntu 18.04
  GNU compilers (upstream)
  Intel MKL as linear algebra backend
  HDF5
  OpenMPI
  OFED/MOFED
  PMI2 (SLURM)
  UCX

Generating recipe (stdout):
  $ hpccm --recipe recipe_dalton_mpi.py --format singularity --singularity-version=3.2
"""

import re

os_version = "18.04"
cmake_version = "3.20.2"
openmpi_version = "4.0.5"

dalton_version = "@_VERSION_@"

# Ubuntu base image
Stage0 += baseimage(image=f"ubuntu:{os_version}", _as="build")

# copy patches to apply
patches = ["dalton-py3.patch", "dalton-install.patch"]
Stage0 += copy(src=[f"patches/{p}" for p in patches], dest="/")

# GNU compilers
compiler = gnu()
Stage0 += compiler
Stage0 += packages(apt=["git", "ca-certificates"])

# (M)OFED
Stage0 += mlnx_ofed()

# UCX
Stage0 += ucx(cuda=False, ofed=True)

# PMI2
Stage0 += slurm_pmi2(version="20.11.7")

# OpenMPI (use UCX instead of IB directly)
Stage0 += openmpi(
    cuda=False,
    infiniband=False,
    pmi="/usr/local/slurm-pmi2",
    ucx="/usr/local/ucx",
    toolchain=compiler.toolchain,
    version=openmpi_version,
)

# CMake
Stage0 += cmake(eula=True, version=cmake_version)

# MKL
Stage0 += mkl(eula=True, mklvars=False)

# HDF5
Stage0 += hdf5(version="1.10.5", configure_opts=["--enable-fortran"])

# Python 3
Stage0 += python(python2=False, python3=True)

# DALTON
Stage0 += generic_cmake(
    repository="https://gitlab.com/dalton/dalton",
    branch=dalton_version,
    recursive=True,
    preconfigure=[f"git apply --reject /{p}" for p in patches],
    cmake_opts=[
        "-D CMAKE_BUILD_TYPE=Release",
        "-D CMAKE_Fortran_COMPILER=mpifort",
        "-D CMAKE_C_COMPILER=mpicc",
        "-D CMAKE_CXX_COMPILER=mpicxx",
        "-D ENABLE_MPI=ON",
        "-D ENABLE_PELIB=ON",
        "-D ENABLE_PDE=ON",
        "-D ENABLE_SRDFT=ON",
    ],
    prefix="/usr/local/dalton",
)

# Runtime distributable stage
Stage1 += baseimage(image=f"ubuntu:{os_version}")
Stage1 += Stage0.runtime()
Stage1 += environment(variables={"PATH": "$PATH:/usr/local/dalton/bin"})
Stage1 += runscript(commands=["dalton"])

Stage1 += label(
    metadata={
        "Author": '"Radovan Bast and Roberto Di Remigio"',
        "Version": f'"{dalton_version}"',
        "Description": '"DALTON program (MPI version)"',
        "Dependency": '"OpenMPI v4.0"',
    }
)

help_str = f"""
%help
    MPI-parallel build of DALTON using OpenMPI-{openmpi_version} on a
    Ubuntu-{os_version} base image. Requires compatible OpenMPI version on the
    host.
    The image includes Mellanox OFED, UCX and PMI2 for compatibility with common
    HPC environments with InfiniBand and SLURM.
    To run with N processes you should launch the singularity execution with
    mpirun/srun:

        $ mpirun -np N singularity exec <image-name>.sif hf molecule
"""
Stage1 += raw(singularity=help_str)
