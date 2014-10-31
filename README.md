# How to Use

## Setup the environment:

    python setup.py
    source venv/bin/activate


## fill it with data!

1) add some pictures to the folder `static/face` in format `name1_name2.jpg` and run

2) use the migration tool to add these images to the database:

    python server.py runserver
    python Tools/db_create_helper.py

3) run the server

    python server.py runserver
