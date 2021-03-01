# A Process Planning Framework for Sustainable Manufacturing

This application enables a highly-automated selection process of manufacturing resources with regard to environmental 
aspects by matching and evaluating manufacturing processes of a part with available manufacturing resources. 
This is achieved by abstracting and generalizing manufacturing resources and part descriptions to dynamically calculate 
the resulting price, required time, and ecologically impacts for the manufacturing of a specific part.

## License
Published under GNU General Public License v3.0 by 
[Institute for Control Engineering of Machine Tools and Manufacturing Units (ISW)](https://www.isw.uni-stuttgart.de)
University of Stuttgart, 2021

## Authors

- [Colin Reiff](https://www.isw.uni-stuttgart.de/institut/team/Reiff-00001/) (ISW, University of Stuttgart)
- [Matthias Buser](https://www.ifsw.uni-stuttgart.de/en/institute/team/Buser/) (IFSW, University of Stuttgart)
- [Thomas Betten](https://www.iabp.uni-stuttgart.de/institut/team/Betten/) (IABP, University of Stuttgart)

---

## Table of Contents

> * [Quick Start Guide](#quick-start-guide)
>   * [Docker](#docker)    
>   * [Local](#local)    
> * [General Usage](#general-usage)
> * [Development and Maintenance](#development-and-maintenance)

## Quick Start Guide

> You can use batch files located in `/bin` for the complete local or docker start-up. 
  Nevertheless, the manual steps to execute the application are described below.

### Docker

**Prerequisites:** Installed `docker` and `docker-compose`.
On Windows you can easily install [Docker Desktop](https://www.docker.com/get-started).

1.  Open a command line interface (e.g. cmd) and navigate to the root path of this application (`/eopp`).
2.  Start the docker container. 
    ```
    docker-compose up -d
    ``` 
    **Note:**   `-d` starts the application in the background.

### Local

**Prerequisites:** Installed `python 3.9` and `pip` (should be included in the standard installation of python).
Make sure to select `Add to PATH` during [installation](https://www.python.org/downloads/release/python-390/).

1.  Open a command line interface (e.g. cmd) and navigate (`cd eopp`) 
    to the root path of this application (`/eopp`).
2.  Create a virtual environment. 
    ```
    python -m venv venv
    ```
3.  Activate the virtual environment.

    For Windows:
    ```
    venv/scripts activate
    ```
    For Linux:
    ```
    cd venv/bin
    ```
    and then 
    ```
    source activate
    ```
4.  Go back to the root path and install the requirements. 
    ```
    pip install -r src/requirements.txt
    ```

TODO: Makemigrations, migrate, createsuperuser

5.  Start the application. 
    ```
    python manage.py runserver
    ```

## General Usage

![Models](docs/figures/models.png)

### Create Parts

### Create Resources

### Execute an Evaluation

## Development and Maintenance

### Dump data

```
python manage.py dumpdata core.processstep --indent 2 > fixtures/processstep.json
```

### Load data

```
python manage.py loaddata fixtures/fixture.json
```
