=================================
Structure of the TEO Module
=================================
The TEO module will be able to optimize the matching between the different sources and the sinks, while taking into account various technical and economic constraints, such as demand profiles, technology cost, efficiencies and losses while also considering thermal energy storage.

•	The TEO optimizes investments and the operation for a case study of three heat sources, two heat sinks, and six thermal energy storages. 

•	The code for the TEO is written in PULP, python. The user needs to install python and then the python package PULP to run the TEO.

•	The code for the TEO us organised in three python files, ‘TEO_Model’, ‘TEO_functions’ and ‘TEO_running_file’. The ‘TEO_Model’ file contains the code of the TEO module and all the equations of the optimization model. ‘TEO_functions’ contains certain pre and post processing functions that are needed to run the module. ‘TEO_running_file’ is the executable file of the TEO. The user can specify the input file and desired format of outputs in the ‘TEO_running_file’.

•	The input file for the prototype is ‘Input_file_TEO’. To run the module, download the code and the input file. Create two folders, names ‘Input_data’ and ‘Output_data’. The python file with the code and the two folders mention above should be located in the same place on the computer. When the model is run, python will provide a series of logs, which describe the model simulation status as shown in the image below. Once the model is run, the output will be saved in a file name ‘Input_file_TEO_Results’ in the ‘Output_data’ folder.

•	The TEO module has been formulated as a linear (mixed-integer) optimisation problem.  

•	In the TEO module, the user will choose from a feasible list of technologies (which will be in knowledge base) based on the level of temperature, for example  Heat Exchanger (HE), Heat Pump (HP),  Waste Heat Recovery (WHR) Boiler and thermal energy storage. The model will then choose the least cost mix of  technologies needed to match the source and sink based on defined constraints of capacity, costs etc.   

•	A long-term optimization of the energy system over several years can be conducted using the TEO. 

The code of the TEO module is based on the long-term energy-planning tool OSeMOSYS (Apache License 2.0). The TEO is built using the python version of OSeMOSYS written in the PULP package of python, which can be accessed at ‘https://github.com/OSeMOSYS/OSeMOSYS_PuLP’. 
The model is structured into SETS, PARAMETERS and VARIABLES.  The model contains equations written based on a linear/mixed integer linear program. The SETS, PARAMETERS and VARIABLES are described below.

The TEO is built based on the Long term energy system optimization tool OSeMOSYS. Further information on the structure of OSeMOSYS can be found at https://osemosys.readthedocs.io/en/latest/manual/Introduction.html 
