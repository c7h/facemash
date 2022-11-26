![image](https://user-images.githubusercontent.com/2639206/204101320-b13b6441-9e15-44e3-be88-06e8149d3c9a.png)

Blog article with more description here: https://www.gerneth.info/2016/12/11/project-3-facemash-clone/

## Setup the environment:

    python setup.py
    source venv/bin/activate


## fill it with data!

1) add some pictures to the folder `static/face` in format `name1_name2.jpg` and run

2) use the migration tool to add these images to the database:

    python server.py runserver
    python Tools/db_create_helper.py

## run the server

    python server.py runserver


