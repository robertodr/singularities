"""
HPCCM recipe for LSDALTON image (OpenMP)

Contents:
  Ubuntu 20.04
  GNU compilers (upstream)
  Intel MKL as linear algebra backend

Generating recipe (stdout):
  $ hpccm --recipe recipe_lsdalton_omp.py --format singularity --singularity-version=3.2
"""

os_version = "20.04"
lsdalton_version = "@_VERSION_@"
cmake_version = "3.20.2"

# Ubuntu base image
Stage0 += baseimage(image=f"ubuntu:{os_version}", _as="build")

# GNU compilers
Stage0 += gnu()
Stage0 += packages(apt=["patch"])

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
        "-D ENABLE_MPI=OFF",
        "-D ENABLE_OMP=ON",
        "-D ENABLE_PYTHON_INTERFACE=ON",
    ],
    prefix="/usr/local/lsdalton",
    url=f"https://gitlab.com/dalton/lsdalton/-/archive/{lsdalton_version}/lsdalton-{lsdalton_version}.tar.gz",
    directory=f"lsdalton-{lsdalton_version}",
)

# Runtime distributable stage
Stage1 += baseimage(image=f"ubuntu:{os_version}")
Stage1 += Stage0.runtime(_from="build")
Stage1 += environment(variables={"PATH": "$PATH:/usr/local/lsdalton/bin"})
Stage1 += runscript(commands=["lsdalton"])

Stage1 += label(
    metadata={
        "Author": '"Radovan Bast and Roberto Di Remigio"',
        "Version": f'"{lsdalton_version}"',
        "Description": '"LSDALTON program (OpenMP version)"',
    }
)

help_str = f"""
%help
    Shared memory parallel (OpenMP) build of LSDALTON on a Ubuntu-{os_version}
    base image.

    For a pure OpenMP run (n threads on one process) you can run the container
    just as the regular lsdalton executable, here with input files hf.dal and
    molecule.mol:

        $ export OMP_NUM_THREADS=n
        $ ./<image-name>.sif hf molecule
"""
Stage1 += raw(singularity=help_str)
