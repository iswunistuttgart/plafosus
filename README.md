# PLAFOSUS

#### A Process Planning Framework for Sustainable Manufacturing

---

This application enables a highly-automated selection process of manufacturing resources with regard to environmental 
aspects by matching and evaluating manufacturing processes of a part with available manufacturing resources. 
This is achieved by abstracting and generalizing manufacturing resources and part descriptions to dynamically calculate 
the resulting price, required time, and ecologically impacts for the manufacturing of a specific part.

## License
Published under GNU General Public License v3.0 by 
[Institute for Control Engineering of Machine Tools and Manufacturing Units (ISW)](https://www.isw.uni-stuttgart.de)
University of Stuttgart, 2021

## Authors

- [Colin Reiff](https://www.isw.uni-stuttgart.de/en/institute/team/Reiff-00001/) (ISW, University of Stuttgart)
- [Matthias Buser](https://www.ifsw.uni-stuttgart.de/en/institute/team/Buser/) (IFSW, University of Stuttgart)
- [Thomas Betten](https://www.iabp.uni-stuttgart.de/en/institute/persons/Betten/) (IABP, University of Stuttgart)

---

## Table of Contents

> * [Quick Start Guide](#quick-start-guide)
> * [General Usage](#general-usage)
> * [Development, Maintenance, and Deployment](#development-maintenance-and-deployment)

## Quick Start Guide

> You can use batch files located in `/bin` for the complete local or docker start-up. 
  Nevertheless, the manual steps to execute the application are described below.

### Docker

**Prerequisites:** Installed `docker` and `docker-compose`.
On Windows you can easily install [Docker Desktop](https://www.docker.com/get-started).

1.  Open a command line interface (e.g. cmd) and navigate to the root path of this application (`/plafosus`).
2.  Start the docker container. 
    ```
    docker-compose up -d
    ``` 
    **Note:**   `-d` starts the application in the background.

### Local

**Prerequisites:** Installed `python 3.9` and `pip` (should be included in the standard installation of python).
Make sure to select `Add to PATH` during [installation](https://www.python.org/downloads/release/python-390/).

1.  Open a command line interface (e.g. cmd) and navigate (`cd plafosus`) 
    to the root path of this application (`/plafosus`).
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
    **Note:** You should se `(venv)` on your command line.
4.  Go back to the root path (`cd ..`) and install the requirements. 
    ```
    pip install -r requirements.txt
    ```
5.  Start the application. 
    ```
    python manage.py runserver
    ```

## General Usage

As a **Service Provider**: Insert your resources into the table **resource**.

As a **Customer**: Insert your part into the table **part**.

After saving the part, the evaluation is executed automatically.
You can find the results in the table **solutions**.

### Architecture

The main models are described below:

**Part:** A part is the high-level object to be manufactured for a customer. 
A part itself is defined by part process steps grouped into single manufacturing possibilities.

**Resource:** A resource is the representation of a machine or similar object in a production environment. 
A resource is defined by its resource skills.

**Requirement:** A requirement is the base class for constraints, and abilities. 
Requirements define the name, unit, and data type. A requirement can be for example *material* of data type 
*string*, since we expect the material name as value.

**Constraint:** A constraint is the specific requirement of a part process step, 
which has to be fulfilled by the resource skill abilities. 
A constraint for the exemplary requirement *material* can be *metal*. 
An operator determines whether the value of the ability must be greater, less or equal to this condition. 
In the case of *material*, the values have to match (operator: *=*).

**Ability:** An ability is the capability of a resource skill to fulfill constraints. 
An ability can be for example *metal* for the requirement *material* and would fulfill the constraint mentioned above.

**Process Step:** A process step is the generic representation of a manufacturing process according to DIN 8580. 
Next to the name of the manufacturing process (e.g. separation), the unit of the process step is defined. 
For example: separation in mm² (e.g. cutting) or separation in mm³ (e.g. milling).

**Part Process Step:** The part process step contains the required quantity of a process step 
(e.g. 50 mm³ of milling) as well as the specified constraints to create a part. 
Each part process step belongs to a manufacturing possibility. 
Multiple possibilities to manufacture the part can be defined.

**Skill:** A skill is the abstract capability of a resource to perform a certain process step. 
For example *high-speed cutting*.

**Resource Skill:** The resource skill is a specific skill of a resource. 
Here, the actual costs, required time and produced co2-e for performing one unit of the skill are defined. 
The unit is defined by underlying process step. A resource skills can be for example *high-speed cutting* 
which is derived from the skill *cutting* with the process step *separation*.

**Consumable:** The consumable is the abstract representation of a medium and its unit consumed by a resource 
to perform a certain resource skill (e.g. water in , electricity, coolant etc.).
**Resource Skill Consumable:** Resource skill consumables are the representation of a medium consumed 
by a specific resource to perform a resource skill. 
E.g. *high-speed cutting* consumes a defined quantity of electricity and coolant per performed 
unit of the resource skill. The resource skill consumables define furthermore the costs (price and co2-e) 
for the usage of one unit of the underlying consumable.

![Models](docs/figures/models.png)

## Development, Maintenance and Deployment

The application is built using [Django](https://www.djangoproject.com/). 
Django is a high-level Python Web framework.

### Project Structure

The most important elements of the django project are described below.

```
.
+-- core:                   The app containing the logic for the main modelling.
|   +-- migrations:         The migrations of the core.
|   +-- admin.py:           The admin interface elements.
|   +-- models.py:          The database models.
|   +-- signals.py:         If a part is saved, here the signal is captured and the main logic for finding a solution is executed.
+-- plafosus:               The project app.
|   +-- settings.py:        Contains the django settings.
+-- solutions:              The app containing the logic for finding solutions.
|   +-- migrations:         The migrations of the solution.
|   +-- admin.py:           The admin interface elements.
|   +-- models.py:          The database models.
|   +-- critic.py:          Some helper functions of the CRITIC evaluation method.
|   +-- search_solution.py: The main workflow for finding solutions.
```

Below, some useful (django) workflows and commands are described.

### Resetting the Database

1. Stop the application.
2. Delete `db.sqlite3`, and all migrations (`core/migrations` and `solutions/migrations`). 
   **Caution:** Do NOT delete the `__init__.py` files in those folders!
3. Continue with [Applying Model Changes](#applying-model-changes)
   
### Applying Model Changes

1. Create new migrations by running `python manage.py makemigrations`.
2. Run `python manage.py migrate`.
3. If you have created a completely new database, 
   create new superuser by running `python manage.py createsuperuser` and insert your credentials.

### Saving Database Data

If you want to save database data, you can dump the information into a file.
[Further information](https://docs.djangoproject.com/en/3.1/ref/django-admin/)

```
python manage.py dumpdata core --indent 2 > fixtures/core.json
```

### Loading Database Data

If you want to insert data into the database, execute:

```
python manage.py loaddata fixtures/core.json
```
