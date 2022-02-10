=================================
Running the TEO for the test case
=================================

Solvers
----------------------------------

Two solvers, GLPK (GNU linear programming kit) and CBC (Coin-or branch and cut) are inbuilt in the PULP. In order to use other solvers, they should be downloaded and installed. Instruction for this can be found at ‘https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html’. After the installation of the solver, the solver path needs to be added as an environment variable and then should be called into python using solver commands.  The user can analyse the data based on the results saved in the output file. The user can also use other solvers such as CPLEX and Gurobi to run the TEO. The solver name and path must be specified in the TEO_running_file.
