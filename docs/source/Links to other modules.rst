===================================
Links to other modules
===================================
This section describes the links between the TEo and the other modules in the EMB3RS platform. 

The TEO module is linked to the GIS and CF module to design the capacities of the heat generation technologies and the heating network. The outputs from TEO are given to GIS module for the iterative process. Other than this, the output from TEO module supplies some inputs to market and business module. 

The iteration between the TEO, the CF and the GIS modules will take place in two steps. In the first step, the GIS module will provide values for DHC costs and average network losses considering all possible connection in the network. The losses in the network consists both of energy and exergy losses. The CF module will account for the exergy losses and calculate the correct conversion capacities for all the sources and sink side technologies. To compensate for the exergy losses, the technologies on the sink and source side must produce heat at higher temperatures. In some cases, additional temperature boosting technologies such as heat pump would be needed to the overcome the exergy losses. The CF will provided the corrected maximum capacities of the technologies to the TEO.  TEO will determine the least cost matching of sources and sinks considering the energy losses in the network. Since the loss values from the GIS are as power losses (in terms of kW), these losses are added to the sink demand in each hour. The TEO then determines the optimal matching of sources and sinks. Based on this, the exchange capacities between the sources and the sinks i.e. the maximum exchange between each source and sinks are calculated. The sources and the sinks in the network and maximum capacities of the sources and the sinks will be fed back to the GIS. In Some cases, the TEO might discard certain sources due to the lack of profitability. This information is also passed on t the GIS module.  In the second step, the GIS will use the calculated maximum exchange capacities to determine the accurate losses and the investments costs of the DHC. These losses are once again fed into the CF to determine the corrected maximum capacities accounting for the exergy losses and forward this information to the TEO. These results are then fed into the TEO to obtain the accurate least cost mix of technologies. A schematic of the iteration is shown in the  Figure below.

.. figure::  Documents/Images/TEO_GIS_CF.png
   :align:   center


TEO-CF-GIS iterations.

In every iteration, the loss value from the GIS is monitored and used as a critical value of stopping the iteration. When the difference in the loss values in two consecutive iterations is below 0.0001, the iterations are stopped. 

Furthermore, the market and business module use the TEO results in a direct manner. The market module uses the installed capacities of the different technologies to calculate the dispatch from each technology. The business module uses the capital investment and operation and maintenance costs of the different technologies and storages, and the salvage values to analyse the financial feasibility of the project. 
