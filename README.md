eigenvector-sparql.py instructions
=========================

1. Follow the instructions [here](https://wiki.duraspace.org/display/FF/Triplestore+Setup) to setup Sesame with Tomcat.
2. Navigate to the `bin` folder in your Tomcat directory and run `./startup.sh`
3. Go to http://localhost:8080/openrdf-workbench/repositories/NONE/create and create a new repository in the memory store. Give it the ID 'eigen' and a title of your choice.
4. Execute the python code by running `python eigenvector-sparql.py`. Ensure that edgefile.txt is in the same location as the python file.

==============================

eigenvector-sherlock.py instructions
=========================

1. Log on to https://sherlock.psc.edu/urika/gam/.
2. In the 'Manage Data' tab, click on 'Add Data' and choose eigen.nt as the data file.
3. In the 'Manage Databases' tab, create a new database and call it 'eigenvector2'. Click on 'Add Data' and select the artifact you just added.
4. Build and start the eigenvector database.
5. Ensure the current database status header reads **Current database:** eigenvector `Connected`.
6. Run `python eigenvector-sherlock.py [username] [password]`.
6. Wait for about 48 minutes for the code to run (sorry). Ensure that the network connection will not be unexpectedly disrupted during this period. 
7. Once the process is complete, the folder with the python script should have an eigenvector-sherlock.txt file containing the first eigenvector as a function of the number of iterations.