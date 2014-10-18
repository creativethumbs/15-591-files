How to get things working
=========================

1. Follow the instructions [here](https://wiki.duraspace.org/display/FF/Triplestore+Setup) to setup Sesame with Tomcat.
2. Navigate to the `bin` folder in your Tomcat directory and run `./startup.sh`
3. Go to http://localhost:8080/openrdf-workbench/repositories/NONE/create and create a new repository in the memory store. Give it the ID 'eigen' and a title of your choice.
4. Execute the python code by running `python eigenvector-sparql.py`. Ensure that edgefile.txt is in the same location as the python file.