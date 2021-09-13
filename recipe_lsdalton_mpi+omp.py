"""
HPCCM recipe for LSDALTON image (MPI+OpenMP)

Contents:
  Ubuntu 18.04
  GNU compilers (upstream)
  Intel MKL as linear algebra backend
  OpenMPI
  OFED/MOFED
  PMI2 (SLURM)
  UCX

Generating recipe (stdout):
  $ hpccm --recipe recipe_lsdalton_mpi+omp.py --format singularity --singularity-version=3.2
"""

os_version = "18.04"
cmake_version = "3.20.2"
openmpi_version = "4.0.5"

lsdalton_version = "@_VERSION_@"

# Ubuntu base image
Stage0 += baseimage(image=f"ubuntu:{os_version}", _as="build")

# GNU compilers
compiler = gnu()
Stage0 += compiler
Stage0 += packages(apt=["patch"])

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

# Python 3
Stage0 += python(python2=False, python3=True, devel=True)
Stage0 += pip(upgrade=True, packages=["cffi", "numpy", "scipy"], pip="pip3")

# LSDALTON
Stage0 += generic_cmake(
    cmake_opts=[
        "-D CMAKE_BUILD_TYPE=Release",
        "-D CMAKE_Fortran_COMPILER=mpifort",
        "-D CMAKE_C_COMPILER=mpicc",
        "-D CMAKE_CXX_COMPILER=mpicxx",
        "-D ENABLE_MPI=ON",
        "-D ENABLE_OMP=ON",
        "-D ENABLE_PYTHON_INTERFACE=ON",
    ],
    prefix="/usr/local/lsdalton",
    url=f"https://gitlab.com/dalton/lsdalton/-/archive/{lsdalton_version}/lsdalton-{lsdalton_version}.tar.gz",
    directory=f"lsdalton-{lsdalton_version}",
)

# Runtime distributable stage
Stage1 += baseimage(image=f"ubuntu:{os_version}")
Stage1 += Stage0.runtime()
Stage1 += environment(variables={"PATH": "$PATH:/usr/local/lsdalton/bin"})
Stage1 += runscript(commands=["lsdalton"])

Stage1 += label(
    metadata={
        "Author": '"Radovan Bast and Roberto Di Remigio"',
        "Version": f'"{lsdalton_version}"',
        "Description": '"LSDALTON program (MPI+OpenMP version)"',
        "Dependency": '"OpenMPI v4.0"',
    }
)

help_str = f"""
%help
    Hybrid parallel (MPI+OpenMP) build of LSDALTON using
    OpenMPI-{openmpi_version} on a Ubuntu-{os_version} base image. Requires
    compatible OpenMPI version on the host.
    The image includes Mellanox OFED, UCX and PMI2 for compatibility with common
    HPC environments with InfiniBand and SLURM.
    For a pure OpenMP run (n threads on one process) run the container just as
    the regular lsdalton executable, here with input files hf.dal and
    molecule.mol:

        $ export OMP_NUM_THREADS=n
        $ ./<image-name>.sif hf molecule

    To run in hybrid parallel (n threads on N processes) you should launch the
    singularity execution with mpirun/srun:

        $ export OMP_NUM_THREADS=n
        $ mpirun -np N singularity exec <image-name>.sif hf molecule
"""
Stage1 += raw(singularity=help_str)
