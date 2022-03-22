=================================
EMB3RS project
=================================

EMB3Rs (“User-driven Energy-Matching & Business Prospection Tool for Industrial Excess Heat/Cold Reduction, Recovery and Redistribution) is a European project funded under the H2020 Programme (Grant Agreement No.847121) to develop an open-sourced tool to match potential sources of excess thermal energy with compatible users of heat and cold. More information about the EMB3RS project can be found on the `EMB3RS website <https://www.emb3rs.eu/>`_ .

Users, like industries and other sources that produce excess heat, will provide the essential parameters, such as their location and the available excess thermal energy. The EMB3Rs platform will then autonomously and intuitively assess the feasibility of new business scenarios and identify the technical solutions to match these sources with compatible sinks. End users such as building managers, energy communities or individual consumers will be able to determine the costs and benefits of industrial excess heat and cold utilisation routes and define the requirements for implementing the most promising solutions. The EMB3Rs platform will integrate several analysis modules that will allow a full exploration of the feasible technical routes to the recovery and use of the available excess thermal energy. Several other modules are a part of the EMB3RS platform. Each module will be used to conduct a special purpose task or analysing excess heat and cold recovery. The models and their primary functionalities are specified below

Core functionalities (CF) module
##############################
The purpose of the CF module is to provide a comprehensive quantification of the energy flows of the EMB3RS platform objects (sinks, sources, and links) and costs associated with different options for excess H/C recovery and use. This information is used by the other analysis modules (GIS, TEO, MM and BM) to perform simulations according to user specifications. The CF module has two main functionalities: 

  1.	Full characterization of objects – e.g., in terms of processes, equipment, building characteristics
  2.	To carry out a preliminary analysis of available supply and demand - described as a simulation feature within the CF.
  
GIS module
##########
The purpose of the GIS model within EMB3Rs is to analyse possible network solutions for a given set of sources and sinks as well as an assumption of related network heat/cold losses and costs. The GIS thereby finds such a network solution along the existing Open Street Map (OSM) Road Network connecting all sources and sinks. It currently outputs a graph/map that lets the user check the specifications of every single pipe element from the network found and a table that illustrates all source/sink specific losses, costs, network length and installed pipe capacity. 

TEO Module
###########
The TEO module identifies least-cost combinations of technologies for using and conveying excess heating or cooling (HC) from defined sources to defined sinks. The user (representing the excess heat producer - i.e., source – or a demand point – i.e., sink) wants to evaluate the least-cost options of utilising excess HC generated to meet the heating/cooling demand for one or more known/assumed sinks. The objective of the optimisation is to find the least-cost mix of technologies (in terms of installed capacities – typically, in power units) and match between sources and sinks (in terms of energy flows) that satisfies the demands under constraints dictated by regulation, availability of heat, load profiles, techno-economic characteristics of technologies, investment plans.

Market Module
##############
The Market Module (MM) will provide the user with economic and fairness indicators like energy transaction, market price, social welfare, fairness among prices. This will be done by short-term and long-term market analyses that simulate various market structures and incorporate business conditions and network models. The MM will consider the existing Pool market as well as new forms of a decentralized market based on peer-to-peer and community systems. The modelling of heat/cold sources and sinks will include flexibility, offering price and business preferences.

Business Module
###############
Business Model Module evaluates various business models for DHC which incorporates excess heat. This is done by calculating matrices like Net Present Value (NPV), Levelized Cost of Heat (LCOH) and Internal Rate of Return (IRR) under different ownership structures and market frameworks. 


