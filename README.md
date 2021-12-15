# singularities

Singularity container recipes for Dalton and LSDalton, based on Ubuntu 18.04 LTS.

## Available recipes

- [Singularity.lsdalton-omp](Singularity.lsdalton-omp): OpenMP-parallel binary on Ubuntu 18.04
- [Singularity.lsdalton-mpi-omp](Singularity.lsdalton-mpi-omp): MPI+OpenMP-parallel binary on Ubuntu 18.04
- [Singularity.dalton-mpi](Singularity.dalton-mpi): MPI-parallel binary on Ubuntu 18.04

## Generate new recipes using HPC Container Maker (HPCCM)

The recipe files are auto-generated using [HPC Container Maker](https://github.com/NVIDIA/hpc-container-maker).

For Singularity:

```
$ hpccm --recipe <recipe_name>.py --format singularity --singularity-version=3.2 > recipes/Singularity.<version-tag>
```

The images are automatically built in GitHub Actions and uploaded to the GitHub
Container Registry.  **Only containers whose recipe changed on a given commit
are rebuilt.**

## How to locally build the image from a recipe file

The version to build is a configurable parameter in the recipes:

- To generate a definition file for v2020.0 of LSDalton:

  ```
  $ cat Singularity.lsdalton-omp | sed "s/@_VERSION_@/v2020.0/g" > Singularity.lsdalton-v2020.0-omp
  ```
- To generate a definition file for the `master` branch of Dalton:

  ```
  $ cat Singularity.lsdalton-omp | sed "s/@_VERSION_@/master/g" > Singularity.lsdalton-master-omp
  ```

You need `sudo` for building images, but you don't need `sudo` for anything else.

```
$ sudo -E singularity build lsdalton-v2020.0-omp.sif Singularity.lsdalton-v2020.0-omp
```

## How to pull these images from GitHub Container Registry

For LSDalton:

- v2020.0 OpenMP parallelization only:
  ```
  singularity pull oras://ghcr.io/robertodr/singularities/lsdalton-v2020.0-omp:latest
  ```

- master branch MPI+OpenMP parallelization:
  ```
  singularity pull oras://ghcr.io/robertodr/singularities/lsdalton-master-mpi-omp:latest
  ```

For Dalton:

- v2020.0 MPI parallelization only:
  ```
  singularity pull oras://ghcr.io/robertodr/singularities/dalton-v2020.0-mpi:latest
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
