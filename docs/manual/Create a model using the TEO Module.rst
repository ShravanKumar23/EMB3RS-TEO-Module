===================================
Create a model using the TEO Module
===================================

This section introduces the user to the basic components of any application of TEO and describes the steps for the creation of a model. To this end, a sample case study is used and examples from it are shown throughout the section. 
The sample case study for TEO, represents a case of industrial excess heat recovery and use. The simple use case consists of two excess heat producers Supermarket and Metal casting Industry and three sink points District Heating and Cooling grid (DHC), office buildings and residential buildings. The excess heat load profiles for the source and sink points are be used. The case study is better represented using the reference energy system (RES) shown in Figure below.


.. figure::  Documents/Images/RES.png
   :align:   center

   The Reference Energy System (RES) of the Simple case study.

The outflow temperatures of the metal casting industry are to be at 300, 90 and 70 degrees Celsius for its three outflows whereas the waste heat from the supermarket is at 50 degrees Celsius. On the sinks’ side, the DHC demand temperature was same as the average supply temperature of the DHN, which is at 90 degrees Celsius. The demand temperature profile of the office buildings was to be the same as that of the residential buildings at 90 degrees Celsius. The sources and the sinks are equipped with storages. This implied that the generation and supply technologies be connected to a storage technology, and also, the demand technologies be connected to storage systems. 

In the RES, The rectangles represent the technologies, the arrows represent the flow of energy and the vertical lines represent fuels. The RES is read from the left to the right, which means the primary side is on the left and the final side is on the right. The source nodes, metal casting industry and the supermarket, are modelled as technologies, whereas the sink nodes, being residential buildings, office buildings and DHC are modelled as fuels. The distribution grid has also been added as a technology as some components can either require or produce electricity. For the test case, the heat pumps in the system will require electricity to operate. The first set of vertical lines represent fuels at the primary level. These primary fuels consist of electricity, waste heat from the outflows of the metal casting industry at three different temperatures, and waste heat from supermarket. The waste heat from each source is supplied to a set of technologies. Here, as the platform is yet to be developed, we assume that the user has chosen a Heat Exchanger (HE), Waste Heat Recovery Boiler (WHRB) for the first waste heat outflow from the industry. Similarly, the second outflow makes use of a HE and a WHRB. The third outflow is provided to a Heat Pump (HP) and a HE. The supermarket waste heat is provided with a HP. 


It is to be noted that only one storage will be chosen for a set of technologies. Here, each technology is connected to a storage option. Based on the technology that is selected from the optimization process, the energy will be stored from the technology in the storage.


The technologies are assessed for feasibility and selected in the process. The converted useful heat at the suitable temperature (here, the network temperature) is stored and also supplied to the secondary fuel level. The secondary level fuel is the converted useful heat. The converted useful heat is then supplied to the District Heating Network, which is modelled as a technology. The network is similar to the distribution grid being modelled as a technology, and they both account for losses. The heat from the network is supplied to all demand points by first being transformed into a tertiary level fuel of district heating water. To further assess the feasibility of the demand side system, solar technologies have been added. Solar thermal technologies have been added to all sinks.

