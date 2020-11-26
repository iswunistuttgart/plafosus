# EOPP

Ecologically Optimized Production Planning

# TODO

- makemigrations, migrate, createsuperuser, install fixtures when installing
- dockerize everything

# Dump data

```
python manage.py dumpdata core.processstep --indent 2 > fixtures/processstep.json
```

# Load data

```
python manage.py loaddata fixtures/processstep.json
```
