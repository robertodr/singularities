# singularities

Singularity container recipes for LSDalton, based on Ubuntu 18.04 LTS.

## Available recipes

- [Singularity.lsdalton-omp](Singularity.lsdalton-omp): OpenMP-parallel binary on Ubuntu 18.04
- [Singularity.lsdalton-mpi+omp](Singularity.lsdalton-mpi+omp): MPI+OpenMP-parallel binary on Ubuntu 18.04

## Generate new recipes using HPC Container Maker (HPCCM)

The recipe files are auto-generated using [HPC Container Maker](https://github.com/NVIDIA/hpc-container-maker).

For Singularity:
```
$ hpccm --recipe <recipe_name>.py --format singularity --singularity-version=3.2 > recipes/Singularity.<version-tag>
```

For Docker:
```
$ hpccm --recipe <recipe_name>.py --format docker > recipes/Docker.<version-tag>
```

The images are automatically built in GitLab CI and uploaded to the registry on every commit.

## How to locally build the image from a recipe file

You need `sudo` for building images but you don't need `sudo` for anything else.
```
$ sudo singularity build lsdalton-v2020.0-omp.sif Singularity.lsdalton-v2020.0-omp
```

## How to pull these images from the GitLab registry

For Singularity:
```
singularity pull https://gitlab.com/api/v4/projects/dalton%2Fcontainers/packages/generic/lsdalton/v2020.0/lsdalton-v2020.0-omp_latest.sif
```

## How to use the image

### Singularity

First try this:
```
$ cat /etc/os-release
$ singularity exec lsdalton-v2020.0-omp.sif cat /etc/os-release
```

Now try to run LSDalton:
```
$ singularity run lsdalton-v2020.0-omp.sif myinput.dal somemolecule.mol
```

Since `lsdalton-v2020.0-omp.sif` is executable, you can also rename it to _e.g._ `lsdalton` and do this instead:
```
$ mv lsdalton-v2020.0-omp.sif lsdalton
$ ./lsdalton myinput.dal somemolecule.mol
```
