import os
import datetime as dt
import logging
import numpy as np
import pandas as pd
import pulp 
import itertools
from TEO_functions import *



def buildmodel(sets_df, df, defaults_df, mcs_df, n):
        # ----------------------------------------------------------------------------------------------------------------------
    #    SETS
    # ----------------------------------------------------------------------------------------------------------------------

    YEAR = createTuple(sets_df, 'YEAR')
    TECHNOLOGY = createTuple(sets_df, 'TECHNOLOGY')
    TIMESLICE = createTuple(sets_df, 'TIMESLICE')
    FUEL = createTuple(sets_df, 'FUEL')
    EMISSION = createTuple(sets_df, 'EMISSION')
    MODE_OF_OPERATION = createTuple(sets_df, 'MODE_OF_OPERATION')
    REGION = createTuple(sets_df, 'REGION')
    REGION2 = createTuple(sets_df, 'REGION2')
    SEASON = createTuple(sets_df, 'SEASON')
    DAYTYPE = createTuple(sets_df, 'DAYTYPE')
    DAILYTIMEBRACKET = createTuple(sets_df, 'DAILYTIMEBRACKET')
    FLEXIBLEDEMANDTYPE = createTuple(sets_df, 'FLEXIBLEDEMANDTYPE')
    STORAGE = createTuple(sets_df, 'STORAGE')

    logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                 f"Sets are created.")

    # ----------------------------------------------------------------------------------------------------------------------
    #    PARAMETERS AND DATA
    # ----------------------------------------------------------------------------------------------------------------------

    df['INDEX'] = [ci([str(r), str(rr), str(ld), str(e), str(f), str(lh), str(ls), str(l), str(s), str(m), str(t), str(y)])\
                       .replace('nan-', '').replace('<NA>-', '').replace('-nan', '').replace('-<NA>', '')
                   for r, rr, ld, e, f, lh, ls, l, s, m, t, y in
                     zip(df.REGION, df.REGION2, df.DAYTYPE, df.EMISSION, df.FUEL, df.DAILYTIMEBRACKET, df.SEASON,\
                         df.TIMESLICE, df.STORAGE, df.MODE_OF_OPERATION, df.TECHNOLOGY, df.YEAR)]

    # Dictionaries for parameters
    AccumulatedAnnualDemand = createParameter(df, 'AccumulatedAnnualDemand')
    AnnualEmissionLimit = createParameter(df, 'AnnualEmissionLimit')
    AnnualExogenousEmission = createParameter(df, 'AnnualExogenousEmission')
    AvailabilityFactor = createParameter(df, 'AvailabilityFactor')
    CapacityFactor = createParameter(df, 'CapacityFactor')
    CapacityOfOneTechnologyUnit = createParameter(df, 'CapacityOfOneTechnologyUnit')
    CapacityToActivityUnit = createParameter(df, 'CapacityToActivityUnit')
    CapitalCost = createParameter(df, 'CapitalCost')
    CapitalCostStorage = createParameter(df, 'CapitalCostStorage')
    Conversionld = createParameter(df, 'Conversionld')
    Conversionlh = createParameter(df, 'Conversionlh')
    Conversionls = createParameter(df, 'Conversionls')
    DaySplit = createParameter(df, 'DaySplit')
    DaysInDayType = createParameter(df, 'DaysInDayType')
    DepreciationMethod = createParameter(df, 'DepreciationMethod')
    DiscountRateTech = createParameter(df, 'DiscountRateTech')
    DiscountRateSto = createParameter(df, 'DiscountRateSto')
    EmissionActivityRatio = createParameter(df, 'EmissionActivityRatio')
    EmissionsPenalty = createParameter(df, 'EmissionsPenalty')
    FixedCost = createParameter(df, 'FixedCost')
    InputActivityRatio = createParameter(df, 'InputActivityRatio')
    MinStorageCharge = createParameter(df, 'MinStorageCharge')
    ModelPeriodEmissionLimit = createParameter(df, 'ModelPeriodEmissionLimit')
    ModelPeriodExogenousEmission = createParameter(df, 'ModelPeriodExogenousEmission')
    OperationalLife = createParameter(df, 'OperationalLife')
    OperationalLifeStorage = createParameter(df, 'OperationalLifeStorage')
    OutputActivityRatio = createParameter(df, 'OutputActivityRatio')
    OutputModeofoperation = createParameter(df, 'OutputModeofoperation')
    REMinProductionTarget = createParameter(df, 'REMinProductionTarget')
    RETagFuel = createParameter(df, 'RETagFuel')
    RETagTechnology = createParameter(df, 'RETagTechnology')
    ReserveMargin = createParameter(df, 'ReserveMargin')
    ReserveMarginTagFuel = createParameter(df, 'ReserveMarginTagFuel')
    ReserveMarginTagTechnology = createParameter(df, 'ReserveMarginTagTechnology')
    ResidualCapacity = createParameter(df, 'ResidualCapacity')
    ResidualStorageCapacity = createParameter(df, 'ResidualStorageCapacity')
    SpecifiedAnnualDemand = createParameter(df, 'SpecifiedAnnualDemand')
    SpecifiedDemandProfile = createParameter(df, 'SpecifiedDemandProfile')
    StorageMaxChargeRate = createParameter(df, 'StorageMaxChargeRate')
    StorageMaxDischargeRate= createParameter(df, 'StorageMaxDischargeRate')
    StorageMaxCapacity = createParameter(df, 'StorageMaxCapacity')
    StorageLevelStart = createParameter(df, 'StorageLevelStart')
    StorageL2D = createParameter(df, 'StorageL2D')
    StorageUvalue = createParameter(df, 'StorageUvalue')
    StorageFlowTemperature = createParameter(df, 'StorageFlowTemperature')
    StorageReturnTemperature = createParameter(df, 'StorageReturnTemperature')
    StorageAmbientTemperature = createParameter(df, 'StorageAmbientTemperature')
    TechWithCapacityNeededToMeetPeakTS = createParameter(df, 'TechWithCapacityNeededToMeetPeakTS')
    TechnologyFromStorage = createParameter(df, 'TechnologyFromStorage')
    TechnologyToStorage = createParameter(df, 'TechnologyToStorage')
    TotalAnnualMaxCapacity = createParameter(df, 'TotalAnnualMaxCapacity')
    TotalAnnualMaxCapacityInvestment = createParameter(df, 'TotalAnnualMaxCapacityInvestment')
    TotalAnnualMinCapacity = createParameter(df, 'TotalAnnualMinCapacity')
    TotalAnnualMinCapacityInvestment = createParameter(df, 'TotalAnnualMinCapacityInvestment')
    TotalTechnologyAnnualActivityLowerLimit = createParameter(df, 'TotalTechnologyAnnualActivityLowerLimit')
    TotalTechnologyAnnualActivityUpperLimit = createParameter(df, 'TotalTechnologyAnnualActivityUpperLimit')
    TotalTechnologyModelPeriodActivityLowerLimit = createParameter(df, 'TotalTechnologyModelPeriodActivityLowerLimit')
    TotalTechnologyModelPeriodActivityUpperLimit = createParameter(df, 'TotalTechnologyModelPeriodActivityUpperLimit')
    TradeRoute = createParameter(df, 'TradeRoute')
    VariableCost = createParameter(df, 'VariableCost')
    YearSplit = createParameter(df, 'YearSplit')

    # Default values for parameters
    dflt = defaults_df.set_index('PARAM').to_dict()['VALUE']

    logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                 f"Parameters are created.")

    # ----------------------------------------------------------------------------------------------------------------------
    #    PERMUTATION OF SETS
    # ----------------------------------------------------------------------------------------------------------------------

    # Global sets
    # REGION (no permutation needed for REGION)
    REGION_FUEL_TIMESLICE_YEAR = permutateSets([REGION, FUEL, TIMESLICE, YEAR])
    REGION_TECHNOLOGY_YEAR = permutateSets([REGION, TECHNOLOGY, YEAR])
    REGION_TIMESLICE_TECHNOLOGY_YEAR = permutateSets([REGION, TIMESLICE, TECHNOLOGY, YEAR])
    REGION_FUEL_TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY_YEAR = permutateSets([REGION, FUEL, TIMESLICE, MODE_OF_OPERATION, TECHNOLOGY, YEAR])
    REGION_FUEL_TIMESLICE_TECHNOLOGY_YEAR = permutateSets([REGION, FUEL, TIMESLICE, TECHNOLOGY, YEAR])
    REGION_REGION2_FUEL_TIMESLICE_YEAR = permutateSets([REGION, REGION2, FUEL, TIMESLICE, YEAR])
    REGION_FUEL_YEAR = permutateSets([REGION, FUEL, YEAR])
    REGION_REGION2_FUEL_YEAR = permutateSets([REGION, REGION2, FUEL, YEAR])
    REGION_MODE_OF_OPERATION_TECHNOLOGY_YEAR = permutateSets([REGION, MODE_OF_OPERATION, TECHNOLOGY, YEAR])
    REGION_DAYTYPE_DAILYTIMEBRACKET_SEASON_STORAGE_YEAR = permutateSets([REGION, DAYTYPE, DAILYTIMEBRACKET, SEASON, STORAGE, YEAR])
    REGION_STORAGE = permutateSets([REGION, STORAGE])
    REGION_STORAGE_YEAR = permutateSets([REGION, STORAGE, YEAR])
    REGION_STORAGE_TIMESLICE_YEAR = permutateSets([REGION, STORAGE, TIMESLICE, YEAR])
    REGION_SEASON_STORAGE_YEAR = permutateSets([REGION, SEASON, STORAGE, YEAR])
    REGION_DAYTYPE_SEASON_STORAGE_YEAR = permutateSets([REGION, DAYTYPE, SEASON, STORAGE, YEAR])
    REGION_YEAR = permutateSets([REGION, YEAR])
    REGION_TECHNOLOGY = permutateSets([REGION, TECHNOLOGY])
    REGION_TIMESLICE_YEAR = permutateSets([REGION, TIMESLICE, YEAR])
    REGION_FUEL_TECHNOLOGY_YEAR = permutateSets([REGION, FUEL, TECHNOLOGY, YEAR])
    REGION_EMISSION_MODE_OF_OPERATION_TECHNOLOGY_YEAR = permutateSets([REGION, EMISSION, MODE_OF_OPERATION, TECHNOLOGY, YEAR])
    REGION_EMISSION_TECHNOLOGY_YEAR = permutateSets([REGION, EMISSION, TECHNOLOGY, YEAR])
    REGION_EMISSION_YEAR = permutateSets([REGION, EMISSION, YEAR])
    REGION_EMISSION = permutateSets([REGION, EMISSION])
    # Local sets within equations
    MODE_OF_OPERATION_YEAR = permutateSets([MODE_OF_OPERATION, YEAR])
    TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY = permutateSets([TIMESLICE, MODE_OF_OPERATION, TECHNOLOGY])
    TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY_YEAR = permutateSets([TIMESLICE, MODE_OF_OPERATION, TECHNOLOGY, YEAR])
    DAYTYPE_DAILYTIMEBRACKET_SEASON = permutateSets([DAYTYPE, DAILYTIMEBRACKET, SEASON])
    DAYTYPE_DAILYTIMEBRACKET = permutateSets([DAYTYPE, DAILYTIMEBRACKET])
    FUEL_TECHNOLOGY = permutateSets([FUEL, TECHNOLOGY])
    FUEL_TIMESLICE = permutateSets([FUEL, TIMESLICE])
    MODE_OF_OPERATION_TECHNOLOGY = permutateSets([ MODE_OF_OPERATION, TECHNOLOGY])
    TIMESLICE_YEAR = permutateSets([ TIMESLICE, YEAR])

    # ----------------------------------------------------------------------------------------------------------------------
    #    MODEL CONSTRUCTION
    # ----------------------------------------------------------------------------------------------------------------------

    i = 0
    while i <= n:

        # ====  Simulation loops  ====

        logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                     f"Model run: {i}")

        # ------------------------------------------------------------------------------------------------------------------
        #    MODEL INITIALIZATION
        # ------------------------------------------------------------------------------------------------------------------

        model = pulp.LpProblem(modelName, pulp.LpMinimize)

        # ------------------------------------------------------------------------------------------------------------------
        #    MODEL VARIABLES
        # ------------------------------------------------------------------------------------------------------------------

        variables = {

            # ====  Net Present Cost  ====

            # 'Cost'

            # ====  Demands  ====

           'RateOfDemand': {'sets': [REGION, FUEL, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'y']},
           'Demand': {'sets': [REGION, FUEL, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'y']},

            # ====  Storage  ====

           'RateOfStorageCharge': {'sets': [REGION, STORAGE, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'l', 'y']},
           'RateOfStorageDischarge': {'sets': [REGION, STORAGE, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'l', 'y']},
           'NetChargeWithinYear': {'sets': [REGION, DAYTYPE, DAILYTIMEBRACKET, SEASON, STORAGE, YEAR], 'lb': None, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'ld', 'lh', 'ls', 's', 'y']},
           'NetChargeWithinDay': {'sets': [REGION, DAYTYPE, DAILYTIMEBRACKET, SEASON, STORAGE, YEAR], 'lb': None, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'ld', 'lh', 'ls', 's', 'y']},
           'StorageLevelYearStart': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'StorageLevelYearFinish': {       'StorageLevelYearFinish': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'StorageLevelSeasonStart': {'sets': [REGION, SEASON, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'ls', 's', 'y']},
           'StorageLevelTimesliceStart': {'sets': [REGION, STORAGE, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'l', 'y']},
           'StorageLosses': {'sets': [REGION, STORAGE, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'l', 'y']},
           'StorageLevelDayTypeStart': {'sets': [REGION, DAYTYPE, SEASON, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'ld', 'ls', 's', 'y']},
           'StorageLevelDayTypeFinish': {'sets': [REGION, DAYTYPE, SEASON, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'ld', 'ls', 's', 'y']},
           'StorageLowerLimit': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'StorageUpperLimit': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'AccumulatedNewStorageCapacity': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'StorageSurfaceArea': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'NewStorageCapacity': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'CapitalInvestmentStorage': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'DiscountedCapitalInvestmentStorage': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'SalvageValueStorage': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'DiscountedSalvageValueStorage': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},
           'TotalDiscountedStorageCost': {'sets': [REGION, STORAGE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 's', 'y']},

            # ====  Capacity Variables  ====

           'NumberOfNewTechnologyUnits': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Integer', 'indices': ['r', 't', 'y']},
           'NewCapacity': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'AccumulatedNewCapacity': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'TotalCapacityAnnual': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},

            # ====  Activity Variables  ====

           'RateOfActivity': {'sets': [REGION, TIMESLICE, MODE_OF_OPERATION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'l', 'm', 't', 'y']},
           'RateOfTotalActivity': {'sets': [REGION, TIMESLICE, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'l', 't', 'y']},
           'TotalTechnologyAnnualActivity': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'TotalAnnualTechnologyActivityByMode': {'sets': [REGION, MODE_OF_OPERATION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'm', 't', 'y']},
           'TotalTechnologyModelPeriodActivity': {'sets': [REGION, TECHNOLOGY], 'lb': None, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't']},
           'RateOfProductionByTechnologyByMode': {'sets': [REGION, FUEL, TIMESLICE, MODE_OF_OPERATION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'm', 't', 'y']},
           'RateOfProductionByTechnology': {'sets': [REGION, FUEL, TIMESLICE, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 't', 'y']},
           'ProductionByTechnology': {'sets': [REGION, FUEL, TIMESLICE, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 't', 'y']},
           'ProductionByTechnologyAnnual': {'sets': [REGION, FUEL, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 't', 'y']},
           'RateOfProduction': {'sets': [REGION, FUEL, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'y']},
           'Production': {'sets': [REGION, FUEL, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'y']},
           'RateOfUseByTechnologyByMode': {'sets': [REGION, FUEL, TIMESLICE, MODE_OF_OPERATION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'm ', 't', 'y']},
           'RateOfUseByTechnology': {'sets': [REGION, FUEL, TIMESLICE, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 't', 'y']},
           # 'UseByTechnologyAnnual': {'sets': [REGION, FUEL, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 't', 'y']},
           # 'RateOfUse': {'sets': [REGION, FUEL, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'y']},
           # 'UseByTechnology': {'sets': [REGION, FUEL, TIMESLICE, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 't', 'y']},
           'Use': {'sets': [REGION, FUEL, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'l', 'y']},
           'Trade': {'sets': [REGION, REGION2, FUEL, TIMESLICE, YEAR], 'lb': None, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'rr', 'f', 'l', 'y']},
           # 'TradeAnnual': {'sets': [REGION, REGION2, FUEL, YEAR], 'lb': None, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'rr', 'f', 'y']},
           'ProductionAnnual': {'sets': [REGION, FUEL, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'y']},
           # 'UseAnnual': {'sets': [REGION, FUEL, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'f', 'y']},

            # ====  Costing Variables  ====

           'CapitalInvestment': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'DiscountedCapitalInvestment': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'SalvageValue': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'DiscountedSalvageValue': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'OperatingCost': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'DiscountedOperatingCost': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'AnnualVariableOperatingCost': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'AnnualFixedOperatingCost': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'TotalDiscountedCostByTechnology': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'TotalDiscountedCost': {'sets': [REGION, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'y']},
           'ModelPeriodCostByRegion': {'sets': [REGION], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r']},

            # ====  Reserve Margin  ====

           'TotalCapacityInReserveMargin': {'sets': [REGION, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'y']},
           'DemandNeedingReserveMargin': {'sets': [REGION, TIMESLICE, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'l', 'y']},

            # ====  RE Gen Target  ====

           # 'TotalREProductionAnnual': {'sets': [REGION, YEAR], 'lb': None, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'y']},
           'RETotalProductionOfTargetFuelAnnual': {'sets': [REGION, YEAR], 'lb': None, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'y']},

            # ====  Emissions  ====

           'AnnualTechnologyEmissionByMode': {'sets': [REGION, EMISSION, MODE_OF_OPERATION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'e', 'm', 't', 'y']},
           'AnnualTechnologyEmission': {'sets': [REGION, EMISSION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'e', 't', 'y']},
           'AnnualTechnologyEmissionPenaltyByEmission': {'sets': [REGION, EMISSION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'e', 't', 'y']},
           'AnnualTechnologyEmissionsPenalty': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'DiscountedTechnologyEmissionsPenalty': {'sets': [REGION, TECHNOLOGY, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 't', 'y']},
           'AnnualEmissions': {'sets': [REGION, EMISSION, YEAR], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'e', 'y']},
           'ModelPeriodEmissions': {'sets': [REGION, EMISSION], 'lb': 0, 'ub': None, 'cat': 'Continuous', 'indices': ['r', 'e']}
        }

        # Dictionaries for variables

        # ====  Net Present Cost  ====

        # 'Cost'

        # ====  Demands  ====

        RateOfDemand = createVariable('RateOfDemand', variables)
        Demand = createVariable('Demand', variables)

        # ====  Storage  ====

        RateOfStorageCharge = createVariable('RateOfStorageCharge', variables)
        RateOfStorageDischarge = createVariable('RateOfStorageDischarge', variables)
        NetChargeWithinYear = createVariable('NetChargeWithinYear', variables)
        NetChargeWithinDay = createVariable('NetChargeWithinDay', variables)
        StorageLevelYearStart = createVariable('StorageLevelYearStart', variables)
        StorageLevelYearFinish = createVariable('StorageLevelYearFinish', variables)
        StorageLevelSeasonStart = createVariable('StorageLevelSeasonStart', variables)
        StorageLevelTimesliceStart = createVariable('StorageLevelTimesliceStart', variables)
        StorageLosses = createVariable('StorageLosses', variables)
        StorageLevelDayTypeStart = createVariable('StorageLevelDayTypeStart', variables)
        StorageLevelDayTypeFinish = createVariable('StorageLevelDayTypeFinish', variables)
        StorageLowerLimit = createVariable('StorageLowerLimit', variables)
        StorageUpperLimit = createVariable('StorageUpperLimit', variables)
        AccumulatedNewStorageCapacity = createVariable('AccumulatedNewStorageCapacity', variables)
        StorageSurfaceArea = createVariable('StorageSurfaceArea', variables)
        NewStorageCapacity = createVariable('NewStorageCapacity', variables)
        CapitalInvestmentStorage = createVariable('CapitalInvestmentStorage', variables)
        DiscountedCapitalInvestmentStorage = createVariable('DiscountedCapitalInvestmentStorage', variables)
        SalvageValueStorage = createVariable('SalvageValueStorage', variables)
        DiscountedSalvageValueStorage = createVariable('DiscountedSalvageValueStorage', variables)
        TotalDiscountedStorageCost = createVariable('TotalDiscountedStorageCost', variables)

        # ====  Capacity Variables  ====

        NumberOfNewTechnologyUnits = createVariable('NumberOfNewTechnologyUnits', variables)
        NewCapacity = createVariable('NewCapacity', variables)
        AccumulatedNewCapacity = createVariable('AccumulatedNewCapacity', variables)
        TotalCapacityAnnual = createVariable('TotalCapacityAnnual', variables)

        # ====  Activity Variables  ====

        RateOfActivity = createVariable('RateOfActivity', variables)
        RateOfTotalActivity = createVariable('RateOfTotalActivity', variables)
        TotalTechnologyAnnualActivity = createVariable('TotalTechnologyAnnualActivity', variables)
        TotalAnnualTechnologyActivityByMode = createVariable('TotalAnnualTechnologyActivityByMode', variables)
        TotalTechnologyModelPeriodActivity = createVariable('TotalTechnologyModelPeriodActivity', variables)
        RateOfProductionByTechnologyByMode = createVariable('RateOfProductionByTechnologyByMode', variables)
        RateOfProductionByTechnology = createVariable('RateOfProductionByTechnology', variables)
        ProductionByTechnology = createVariable('ProductionByTechnology', variables)
        ProductionByTechnologyAnnual = createVariable('ProductionByTechnologyAnnual', variables)
        RateOfProduction = createVariable('RateOfProduction', variables)
        Production = createVariable('Production', variables)
        RateOfUseByTechnologyByMode = createVariable('RateOfUseByTechnologyByMode', variables)
        RateOfUseByTechnology = createVariable('RateOfUseByTechnology', variables)
        # UseByTechnologyAnnual = createVariable('UseByTechnologyAnnual', variables)
        # RateOfUse = createVariable('RateOfUse', variables)
        # UseByTechnology = createVariable('UseByTechnology', variables)
        Use = createVariable('Use', variables)
        Trade = createVariable('Trade', variables)
        # TradeAnnual = createVariable('TradeAnnual', variables)
        ProductionAnnual = createVariable('ProductionAnnual', variables)
        # UseAnnual = createVariable('UseAnnual', variables)

        # ====  Costing Variables  ====

        CapitalInvestment = createVariable('CapitalInvestment', variables)
        DiscountedCapitalInvestment = createVariable('DiscountedCapitalInvestment', variables)
        SalvageValue = createVariable('SalvageValue', variables)
        DiscountedSalvageValue = createVariable('DiscountedSalvageValue', variables)
        OperatingCost = createVariable('OperatingCost', variables)
        DiscountedOperatingCost = createVariable('DiscountedOperatingCost', variables)
        AnnualVariableOperatingCost = createVariable('AnnualVariableOperatingCost', variables)
        AnnualFixedOperatingCost = createVariable('AnnualFixedOperatingCost', variables)
        TotalDiscountedCostByTechnology = createVariable('TotalDiscountedCostByTechnology', variables)
        TotalDiscountedCost = createVariable('TotalDiscountedCost', variables)
        ModelPeriodCostByRegion = createVariable('ModelPeriodCostByRegion', variables)

        # ====  Reserve Margin  ====

        TotalCapacityInReserveMargin = createVariable('TotalCapacityInReserveMargin', variables)
        DemandNeedingReserveMargin = createVariable('DemandNeedingReserveMargin', variables)

        # ====  RE Gen Target  ====

        # TotalREProductionAnnual = createVariable('TotalREProductionAnnual', variables)
        RETotalProductionOfTargetFuelAnnual = createVariable('RETotalProductionOfTargetFuelAnnual', variables)

        # ====  Emissions  ====

        AnnualTechnologyEmissionByMode = createVariable('AnnualTechnologyEmissionByMode', variables)
        AnnualTechnologyEmission = createVariable('AnnualTechnologyEmission', variables)
        AnnualTechnologyEmissionPenaltyByEmission = createVariable('AnnualTechnologyEmissionPenaltyByEmission', variables)
        AnnualTechnologyEmissionsPenalty = createVariable('AnnualTechnologyEmissionsPenalty', variables)
        DiscountedTechnologyEmissionsPenalty = createVariable('DiscountedTechnologyEmissionsPenalty', variables)
        AnnualEmissions = createVariable('AnnualEmissions', variables)
        ModelPeriodEmissions = createVariable('ModelPeriodEmissions', variables)

        logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                     f"Variables are created.")

        # ------------------------------------------------------------------------------------------------------------------
        #    OBJECTIVE FUNCTION
        # ------------------------------------------------------------------------------------------------------------------

        Cost = pulp.LpVariable("Cost", cat='Continuous')
        model += Cost, "Objective"
        model += Cost == pulp.lpSum([TotalDiscountedCost.get(ci(ry)) for ry in REGION_YEAR]), "Cost_function"

        # ------------------------------------------------------------------------------------------------------------------
        #    CONSTRAINTS
        # ------------------------------------------------------------------------------------------------------------------
        for rfly in REGION_FUEL_TIMESLICE_YEAR:
            # EQ_SpecifiedDemand
            model += RateOfDemand.get(ci(rfly)) == SpecifiedAnnualDemand.get(ci([*rfly[0:2], rfly[3]]), dflt.get('SpecifiedAnnualDemand')) * SpecifiedDemandProfile.get(ci(rfly), dflt.get('SpecifiedDemandProfile')) / YearSplit.get(ci(rfly[2:4])), ""

        # ====  Capacity Adequacy A  ====

        for rlty in REGION_TIMESLICE_TECHNOLOGY_YEAR:
            # CAa3_TotalActivityOfEachTechnology
            model += RateOfTotalActivity.get(ci(rlty)) == pulp.lpSum([(RateOfActivity.get(ci([*rlty[0:2], m, *rlty[2:4]])) * OutputModeofoperation.get(ci([rlty[0], m, *rlty[2:4]]), dflt.get('OutputModeofoperation'))) for m in MODE_OF_OPERATION]), ""
            # CAa4_Constraint_Capacity
            model += RateOfTotalActivity.get(ci(rlty)) <= TotalCapacityAnnual.get(ci([rlty[0], *rlty[2:4]])) * CapacityFactor.get(ci(rlty), dflt.get('CapacityFactor')) * CapacityToActivityUnit.get(ci([rlty[0], rlty[2]]), dflt.get('CapacityToActivityUnit')), ""

        for rty in REGION_TECHNOLOGY_YEAR:
            # CAa1_TotalNewCapacity
            model += AccumulatedNewCapacity.get(ci(rty)) == pulp.lpSum([NewCapacity.get(ci([*rty[0:2], yy])) for yy in YEAR if (float(int(rty[2]) - int(yy)) < float(OperationalLife.get(ci(rty[0:2]), dflt.get('OperationalLife')))) and (int(rty[2]) - int(yy) >= 0)]), ""
            # CAa2_TotalAnnualCapacity
            model += TotalCapacityAnnual.get(ci(rty)) == AccumulatedNewCapacity.get(ci(rty)) + ResidualCapacity.get(ci(rty), dflt.get('ResidualCapacity')), ""

            if CapacityOfOneTechnologyUnit.get(ci(rty), dflt.get('CapacityOfOneTechnologyUnit')) != 0:
                # CAa5_TotalNewCapacity
                model += NewCapacity.get(ci(rty)) == CapacityOfOneTechnologyUnit.get(ci(rty), dflt.get('CapacityOfOneTechnologyUnit')) * NumberOfNewTechnologyUnits.get(ci(rty)), ""

        # ====  Capacity Adequacy B  ====

            # CAb1_PlannedMaintenance
            model += pulp.lpSum([RateOfTotalActivity.get(ci(rlty)) * YearSplit.get(ci([l, rlty[3]])) for l in TIMESLICE]) <= pulp.lpSum([TotalCapacityAnnual.get(ci([rlty[0], *rlty[2:4]])) * CapacityFactor.get(ci(rlty), dflt.get('CapacityFactor')) * YearSplit.get(ci([l, rlty[3]])) for l in TIMESLICE]) * AvailabilityFactor.get(ci([rlty[0], *rlty[2:4]]), dflt.get('AvailabilityFactor')) * CapacityToActivityUnit.get(ci([rlty[0], rlty[2]]), dflt.get('CapacityToActivityUnit')), ""

        # ====  Energy Balance A  ====

        for rflmty in REGION_FUEL_TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY_YEAR:
            # EBa1_RateOfFuelProduction1
            if OutputActivityRatio.get(ci([*rflmty[0:2], *rflmty[3:6]]), dflt.get('OutputActivityRatio')) != 0:
                model += RateOfProductionByTechnologyByMode.get(ci(rflmty)) == RateOfActivity.get(ci([rflmty[0], *rflmty[2:6]])) * OutputActivityRatio.get(ci([*rflmty[0:2], *rflmty[3:6]]), dflt.get('OutputActivityRatio')), ""
            else:
                model += RateOfProductionByTechnologyByMode.get(ci(rflmty)) == 0, ""
            # EBa4_RateOfFuelUse1
            if InputActivityRatio.get(ci([*rflmty[0:2], *rflmty[3:6]]), dflt.get('InputActivityRatio')) != 0:
                model += RateOfUseByTechnologyByMode.get(ci(rflmty)) == RateOfActivity.get(ci([rflmty[0], *rflmty[2:6]])) * InputActivityRatio.get(ci([*rflmty[0:2], *rflmty[3:6]]), dflt.get('OutputActivityRatio')), ""

        for rflty in REGION_FUEL_TIMESLICE_TECHNOLOGY_YEAR:
            # EBa2_RateOfFuelProduction2
            model += RateOfProductionByTechnology.get(ci(rflty)) == pulp.lpSum([RateOfProductionByTechnologyByMode.get(ci([*rflty[0:3], m, *rflty[3:5]])) for m in MODE_OF_OPERATION if OutputActivityRatio.get(ci([*rflty[0:2], m, *rflty[3:5]]), dflt.get('OutputActivityRatio')) != 0]), ""
            # EBa5_RateOfFuelUse2
            model += RateOfUseByTechnology.get(ci(rflty)) == pulp.lpSum([RateOfUseByTechnologyByMode.get(ci([*rflty[0:3], m, *rflty[3:5]])) for m in MODE_OF_OPERATION if InputActivityRatio.get(ci([*rflty[0:2], m, *rflty[3:5]]), dflt.get('InputActivityRatio')) != 0]), ""

        for rfly in REGION_FUEL_TIMESLICE_YEAR:
            # EBa3_RateOfFuelProduction3
            model += RateOfProduction.get(ci(rfly)) == pulp.lpSum([RateOfProductionByTechnology.get(ci([*rfly[0:3], t, rfly[3]])) for t in TECHNOLOGY]), ""
            # EBa6_RateOfFuelUse3
            # model += RateOfUse.get(ci(rfly)) == pulp.lpSum([RateOfUseByTechnology.get(ci([*rfly[0:3], t, rfly[3]])) for t in TECHNOLOGY]), ""
            # EBa7_EnergyBalanceEachTS1
            model += Production.get(ci(rfly)) == RateOfProduction.get(ci(rfly)) * YearSplit.get(ci(rfly[2:4])), ""
            # EBa8_EnergyBalanceEachTS2
            # model += Use.get(ci(rfly)) == RateOfUse.get(ci(rfly)) * YearSplit.get(ci(rfly[2:4])), ""
            model += Use.get(ci(rfly)) == pulp.lpSum([RateOfUseByTechnology.get(ci([*rfly[0:3], t, rfly[3]])) for t in TECHNOLOGY]) * YearSplit.get(ci(rfly[2:4])), ""

            # EBa9_EnergyBalanceEachTS3
            model += Demand.get(ci(rfly)) == RateOfDemand.get(ci(rfly)) * YearSplit.get(ci(rfly[2:4])), ""

            # EBa11_EnergyBalanceEachTS5
            model += Production.get(ci(rfly)) >= Demand.get(ci(rfly)) + Use.get(ci(rfly)) + pulp.lpSum([Trade.get(ci([rfly[0], rr, *rfly[1:4]])) * TradeRoute.get(ci([rfly[0], rr, rfly[1], rfly[3]]), dflt.get('TradeRoute')) for rr in REGION2]), ""

        for rr2fly in REGION_REGION2_FUEL_TIMESLICE_YEAR:
            # EBa10_EnergyBalanceEachTS4
            model += Trade.get(ci(rr2fly)) == -Trade.get(ci([rr2fly[1], rr2fly[0], *rr2fly[2:5]])), ""

        # ====  Energy Balance B  ====

        for rfy in REGION_FUEL_YEAR:
            # EBb1_EnergyBalanceEachYear1
            model += ProductionAnnual.get(ci(rfy)) == pulp.lpSum([Production.get(ci([*rfy[0:2], l, rfy[2]])) for l in TIMESLICE]), ""
            # EBb2_EnergyBalanceEachYear2
            # model += UseAnnual.get(ci(rfy)) == pulp.lpSum([Use.get(ci([rfy[0], l, *rfy[1:3]])) for l in TIMESLICE]), ""

        # for rr2fy in REGION_REGION2_FUEL_YEAR:
        #     # EBb3_EnergyBalanceEachYear3
        #     model += TradeAnnual.get(ci(rr2fy)) == pulp.lpSum([Trade.get(ci([*rr2fy[0:2], l, *rr2fy[2:4]])) for l in TIMESLICE]), ""
        #
        # for rfy in REGION_FUEL_YEAR:

            # EBb4_EnergyBalanceEachYear4
            # model += ProductionAnnual.get(ci(rfy)) >= UseAnnual.get(ci(rfy)) + pulp.lpSum([TradeAnnual.get(ci([rfy[0], rr, *rfy[1:3]])) * TradeRoute.get(ci([rfy[0], rr, *rfy[1:3]]), dflt.get('TradeRoute')) for rr in REGION2]) + AccumulatedAnnualDemand.get(ci(rfy), dflt.get('AccumulatedAnnualDemand')), ""
            #model += ProductionAnnual.get(ci(rfy)) >= pulp.lpSum([Use.get(ci([rfy[0], l, *rfy[1:3]])) for l in TIMESLICE])+ pulp.lpSum([pulp.lpSum([Trade.get(ci([rfy[0], rr, l, *rfy[1:3]])) for l in TIMESLICE]) * TradeRoute.get(ci([rfy[0], rr, *rfy[1:3]]), dflt.get('TradeRoute')) for rr in REGION2]) + AccumulatedAnnualDemand.get(ci(rfy), dflt.get('AccumulatedAnnualDemand')), ""

        # ====  Accounting Technology Production/Use  ====

        for rflty in REGION_FUEL_TIMESLICE_TECHNOLOGY_YEAR:
            # Acc1_FuelProductionByTechnology
            model += ProductionByTechnology.get(ci(rflty)) == pulp.lpSum([RateOfProductionByTechnologyByMode.get(ci([*rflty[0:3], m, *rflty[3:5]])) for m in MODE_OF_OPERATION if OutputActivityRatio.get(ci([*rflty[0:2], m, *rflty[3:5]]), dflt.get('OutputActivityRatio')) != 0]) * YearSplit.get(ci([rflty[2], rflty[4]])), ""
            # Acc2_FuelUseByTechnology
            # model += UseByTechnology.get(ci(rflty)) == RateOfUseByTechnology.get(ci(rflty)) * YearSplit.get(ci([rflty[2], rflty[4]])), ""

        for rmty in REGION_MODE_OF_OPERATION_TECHNOLOGY_YEAR:
            # Acc3_AverageAnnualRateOfActivity
            model += TotalAnnualTechnologyActivityByMode.get(ci(rmty)) == pulp.lpSum([RateOfActivity.get(ci([rmty[0], l, *rmty[1:4]])) * YearSplit.get(ci([l, rmty[3]])) for l in TIMESLICE]), ""

        for r in REGION:
            # Acc4_ModelPeriodCostByRegion
            model += ModelPeriodCostByRegion.get(r) == pulp.lpSum([TotalDiscountedCost.get(ci([r, y])) for y in YEAR]), ""

    #     
    #   # ====  Storage Equations  ====

    #     for rldlhlssy in REGION_DAYTYPE_DAILYTIMEBRACKET_SEASON_STORAGE_YEAR:
    #         # S1_RateOfStorageCharge
    #         model += RateOfStorageCharge.get(ci(rldlhlssy)) == pulp.lpSum([RateOfActivity.get(ci([rldlhlssy[0], *lmt, rldlhlssy[5]])) * TechnologyToStorage.get(ci([rldlhlssy[0],  *lmt[1:3], rldlhlssy[3]]), dflt.get('TechnologyToStorage')) * Conversionls.get(ci([lmt[0], rldlhlssy[3]]), dflt.get('Conversionls')) * Conversionld.get(ci([lmt[0], rldlhlssy[1]]), dflt.get('Conversionld')) * Conversionlh.get(ci([lmt[0], rldlhlssy[2]]), dflt.get('Conversionlh')) for lmt in TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY if TechnologyToStorage.get(ci([rldlhlssy[0], lmt[1], rldlhlssy[4], lmt[2]]), dflt.get('TechnologyToStorage')) > 0]), ""
    #         # S2_RateOfStorageDischarge
    #         model += RateOfStorageDischarge.get(ci(rldlhlssy)) == pulp.lpSum([RateOfActivity.get(ci([rldlhlssy[0], *lmt, rldlhlssy[5]])) * TechnologyFromStorage.get(ci([rldlhlssy[0], *lmt[1:3], rldlhlssy[3]]), dflt.get('TechnologyFromStorage')) * Conversionls.get(ci([lmt[0], rldlhlssy[3]]), dflt.get('Conversionls')) * Conversionld.get(ci([lmt[0], rldlhlssy[1]]), dflt.get('Conversionld')) * Conversionlh.get(ci([lmt[0], rldlhlssy[2]]), dflt.get('Conversionlh')) for lmt in TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY if TechnologyFromStorage.get(ci([rldlhlssy[0], lmt[1], rldlhlssy[4], lmt[2]]), dflt.get('TechnologyFromStorage')) > 0]), ""
    #         # S3_NetChargeWithinYear
    #         model += NetChargeWithinYear.get(ci(rldlhlssy)) == pulp.lpSum([(RateOfStorageCharge.get(ci(rldlhlssy)) - RateOfStorageDischarge.get(ci(rldlhlssy))) * YearSplit.get(ci([l, rldlhlssy[5]])) * Conversionls.get(ci([l, rldlhlssy[3]]), dflt.get('Conversionls')) * Conversionld.get(ci([l, rldlhlssy[1]]), dflt.get('Conversionld')) * Conversionlh.get(ci([l, rldlhlssy[2]]), dflt.get('Conversionlh')) for l in TIMESLICE if (Conversionls.get(ci([l, rldlhlssy[3]]), dflt.get('Conversionls')) > 0) and (Conversionld.get(ci([l, rldlhlssy[1]]), dflt.get('Conversionld')) > 0) and (Conversionlh.get(ci([l, rldlhlssy[2]]), dflt.get('Conversionlh')) > 0)]), ""
    #         # S4_NetChargeWithinDay
    #         model += NetChargeWithinDay.get(ci(rldlhlssy)) == (RateOfStorageCharge.get(ci(rldlhlssy)) - RateOfStorageDischarge.get(ci(rldlhlssy))) * DaySplit.get(ci([rldlhlssy[2], rldlhlssy[5]]), dflt.get('DaySplit')), ""

    #     for rsy in REGION_STORAGE_YEAR:
    #         # S5_and_S6_StorageLevelYearStart
    #         if int(rsy[2]) == int(min(YEAR)):
    #             model += StorageLevelYearStart.get(ci(rsy)) == StorageLevelStart.get(ci(rsy[0:2]), dflt.get('StorageLevelStart')), ""
    #         else:
    #             model += StorageLevelYearStart.get(ci(rsy)) == StorageLevelYearStart.get(ci([*rsy[0:2], str(int(rsy[2])-1)])) + pulp.lpSum([NetChargeWithinYear.get(ci([*rsy[0:2], *ldlhls, str(int(rsy[2])-1)])) for ldlhls in DAYTYPE_DAILYTIMEBRACKET_SEASON]), ""
    #         # S7_and_S8_StorageLevelYearFinish
    #         if int(rsy[2]) < int(max(YEAR)):
    #             model += StorageLevelYearFinish.get(ci(rsy)) == StorageLevelYearStart.get(ci([*rsy[0:2], str(int(rsy[2])-1)])), ""
    #         else:
    #             model += StorageLevelYearFinish.get(ci(rsy)) == StorageLevelYearStart.get(ci(rsy)) + pulp.lpSum([NetChargeWithinYear.get(ci([*rsy[0:2], *ldlhls, rsy[2]])) for ldlhls in DAYTYPE_DAILYTIMEBRACKET_SEASON]), ""

    #     for rlssy in REGION_SEASON_STORAGE_YEAR:
    #         # S9_and_S10_StorageLevelSeasonStart
    #         if int(rlssy[1]) == int(min(SEASON)):
    #             model += StorageLevelSeasonStart.get(ci(rlssy)) == StorageLevelYearStart.get(ci([rlssy[0], *rlssy[2:4]])), ""
    #         else:
    #             model += StorageLevelSeasonStart.get(ci(rlssy)) == StorageLevelSeasonStart.get(ci([rlssy[0], str(int(rlssy[1])-1), *rlssy[2:4]])) + pulp.lpSum([NetChargeWithinYear.get(ci([rlssy[0], str(int(rlssy[1])-1), *ldlh, *rlssy[2:4]])) for ldlh in DAYTYPE_DAILYTIMEBRACKET]), ""

    #     for rldlssy in REGION_DAYTYPE_SEASON_STORAGE_YEAR:
    #         # S11_and_S12_StorageLevelDayTypeStart
    #         if int(rldlssy[1]) == int(min(DAYTYPE)):
    #             model += StorageLevelDayTypeStart.get(ci(rldlssy)) == StorageLevelSeasonStart.get(ci([rldlssy[0], *rldlssy[2:5]])), ""
    #         else:
    #             model += StorageLevelDayTypeStart.get(ci(rldlssy)) == StorageLevelDayTypeStart.get(ci([rldlssy[0], str(int(rldlssy[1])-1), *rldlssy[2:5]])) + pulp.lpSum([NetChargeWithinDay.get(ci([rldlssy[0], str(int(rldlssy[1])-1), lh, rldlssy[2:5]])) * DaysInDayType.get(ci([rldlssy[2], str(int(rldlssy[1])-1), rldlssy[4]]), dflt.get('DaysInDayType')) for lh in DAILYTIMEBRACKET]), ""
    #         # S13_and_S14_and_S15_StorageLevelDayTypeFinish
    #         if (int(rldlssy[1]) == int(max(DAYTYPE))) and (int(rldlssy[2]) == int(max(SEASON))):
    #             model += StorageLevelDayTypeFinish.get(ci(rldlssy)) == StorageLevelYearFinish.get(ci([rldlssy[0], *rldlssy[3:5]])), ""
    #         elif int(rldlssy[1]) == int(max(DAYTYPE)):
    #             model += StorageLevelDayTypeFinish.get(ci(rldlssy)) == StorageLevelSeasonStart.get(ci([rldlssy[0], str(int(rldlssy[2])+1), *rldlssy[3:5]])), ""
    #         else:
    #             model += StorageLevelDayTypeFinish.get(ci(rldlssy)) == StorageLevelDayTypeFinish.get(ci([rldlssy[0], rldlssy[2], str(int(rldlssy[1])+1), *rldlssy[3:5]])) - pulp.lpSum([NetChargeWithinDay.get(ci([rldlssy[0], str(int(rldlssy[1])-1), lh, rldlssy[2:5]])) * DaysInDayType.get(ci([rldlssy[2], str(int(rldlssy[1])-1), rldlssy[4]]), dflt.get('DaysInDayType')) for lh in DAILYTIMEBRACKET]), ""

    #                      ====  Storage Constraints  ====
    #     for rldlhlssy in REGION_DAYTYPE_DAILYTIMEBRACKET_SEASON_STORAGE_YEAR:
    #         # SC1_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint
    #         model += (StorageLevelDayTypeStart.get(ci([*rldlhlssy[0:2], *rldlhlssy[3:6]])) + pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, *rldlhlssy[3:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2])-int(lhlh) > 0])) - StorageLowerLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) >= 0, ""
    #         # SC1_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInFirstWeekConstraint
    #         model += (StorageLevelDayTypeStart.get(ci([*rldlhlssy[0:2], *rldlhlssy[3:6]])) + pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, *rldlhlssy[3:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2])-int(lhlh) > 0])) - StorageUpperLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) <= 0, ""
    #         # SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint
    #         if int(rldlhlssy[1]) > int(min(DAYTYPE)):
    #             model += (StorageLevelDayTypeStart.get(ci([*rldlhlssy[0:2], *rldlhlssy[3:6]])) - pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, str(int(rldlhlssy[3])-1), *rldlhlssy[4:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2])-int(lhlh) < 0])) - StorageLowerLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) >= 0, ""
    #         # SC2_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInFirstWeekConstraint
    #         if int(rldlhlssy[1]) > int(min(DAYTYPE)):
    #             model += (StorageLevelDayTypeStart.get(ci([*rldlhlssy[0:2], *rldlhlssy[3:6]])) - pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, str(int(rldlhlssy[3])-1), *rldlhlssy[4:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2]) - int(lhlh) < 0])) - StorageUpperLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) <= 0, ""
    #         # SC3_LowerLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint
    #         model += (StorageLevelDayTypeFinish.get(ci([*rldlhlssy[0:2], *rldlhlssy[3:6]])) - pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, *rldlhlssy[3:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2]) - int(lhlh) < 0])) - StorageLowerLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) >= 0, ""
    #         # SC3_UpperLimit_EndOfDailyTimeBracketOfLastInstanceOfDayTypeInLastWeekConstraint
    #         model += (StorageLevelDayTypeFinish.get(ci([*rldlhlssy[0:2], *rldlhlssy[3:6]])) - pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, *rldlhlssy[3:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2]) - int(lhlh) < 0])) - StorageUpperLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) <= 0, ""
    #         # SC4_LowerLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint
    #         if int(rldlhlssy[1]) > int(min(DAYTYPE)):
    #             model += (StorageLevelDayTypeFinish.get(ci([rldlhlssy[0], str(int(rldlhlssy[1])-1), *rldlhlssy[3:6]])) + pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, *rldlhlssy[3:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2]) - int(lhlh) > 0])) - StorageLowerLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) >= 0, ""
    #         # SC4_UpperLimit_BeginningOfDailyTimeBracketOfFirstInstanceOfDayTypeInLastWeekConstraint
    #         if int(rldlhlssy[1]) > int(min(DAYTYPE)):
    #             model += (StorageLevelDayTypeFinish.get(ci([rldlhlssy[0], str(int(rldlhlssy[1])-1), *rldlhlssy[3:6]])) + pulp.lpSum([NetChargeWithinDay.get(ci([*rldlhlssy[0:2], lhlh, *rldlhlssy[3:6]])) for lhlh in DAILYTIMEBRACKET if int(rldlhlssy[2]) - int(lhlh) > 0])) - StorageUpperLimit.get(ci([rldlhlssy[0], *rldlhlssy[4:6]])) <= 0, ""

    #         # SC5_MaxChargeConstraint
    #         model += RateOfStorageCharge.get(ci(rldlhlssy)) <= StorageMaxChargeRate.get(ci(rldlhlssy[4:6]), dflt.get('StorageMaxChargeRate')), ""
    #         # SC6_MaxDischargeConstraint
    #         model += RateOfStorageDischarge.get(ci(rldlhlssy)) <= StorageMaxDischargeRate.get(ci(rldlhlssy[4:6]), dflt.get('StorageMaxDischargeRate')), ""

        # ====  Storage equations for Thermal storage -  ====

       # ====  Storage equations for Thermal storage -  ====
        for rsy in REGION_STORAGE_YEAR:
        #SL1_Storage_losses_thermal_storage
            if(StorageL2D.get(ci(rsy), dflt.get('StorageL2D')) == 0):
                model += StorageSurfaceArea.get(ci(rsy)) == 0.0361 * AccumulatedNewStorageCapacity.get(ci(rsy)), ""  
            elif(StorageL2D.get(ci(rsy), dflt.get('StorageL2D')) == 1):
                model += StorageSurfaceArea.get(ci(rsy)) == 0.065 * AccumulatedNewStorageCapacity.get(ci(rsy)), ""


        for rsly in REGION_STORAGE_TIMESLICE_YEAR:
            #SL1_Storage_losses
            #if (StorageL2D.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageL2D')) == 0):
                #model += StorageLosses.get(ci([*rsy[0:2], str(int(rsy[2])-1)])) ==  1.5374  * (8.76 / int(max(TIMESLICE))) * 0.0036 * (StorageUvalue.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageUvalue'))) * ((((StorageFlowTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageFlowTemperature'))) - (StorageReturnTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageReturnTemperature')))) * StorageLevelTimesliceStart.get(ci(rsly))) + (((StorageReturnTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageReturnTemperature'))) - (StorageAmbientTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageAmbientTemperature')))) * StorageUpperLimit.get(ci([*rsly[0:2], rsly[3]]))))  , ""
                model += StorageLosses.get(ci(rsly)) ==  StorageSurfaceArea.get(ci([*rsly[0:2], rsly[3]])) * 0.0036 * (8760 / int(max(TIMESLICE))) * (StorageUvalue.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageUvalue'))) * ((((StorageFlowTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageFlowTemperature'))) + (StorageReturnTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageReturnTemperature')))) / 2) - (StorageAmbientTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageAmbientTemperature')))) / 1000  , ""

            #elif (StorageL2D.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageL2D')) == 1):
                #model += StorageLosses.get(ci([*rsy[0:2], str(int(rsy[2])-1)])) ==  2.7673  * (8.76 / int(max(TIMESLICE))) * 0.0036 * (StorageUvalue.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageUvalue'))) * ((((StorageFlowTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageFlowTemperature'))) - (StorageReturnTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageReturnTemperature')))) * StorageLevelTimesliceStart.get(ci(rsly))) + (((StorageReturnTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageReturnTemperature'))) - (StorageAmbientTemperature.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageAmbientTemperature')))) * StorageUpperLimit.get(ci([*rsly[0:2], rsly[3]]))))  , ""

        for rsy in REGION_STORAGE_YEAR:
         #S5_and_S6_StorageLevelYearStart
            if int(rsy[2]) == int(min(YEAR)):
                model += StorageLevelYearStart.get(ci(rsy)) == StorageLevelStart.get(ci(rsy[0:2]), dflt.get('StorageLevelStart')), ""
            else:
                model += StorageLevelYearStart.get(ci(rsy)) == StorageLevelYearStart.get(ci([*rsy[0:2], str(int(rsy[2])-1)])) + pulp.lpSum([((RateOfStorageCharge.get(ci([*rsy[0:2], l, str(int(rsy[2])-1)])) - RateOfStorageDischarge.get(ci([*rsy[0:2], l, str(int(rsy[2])-1)]))) * YearSplit.get(ci([l, str(int(rsy[2])-1)]))) for l in TIMESLICE]), ""

        for rsly in REGION_STORAGE_TIMESLICE_YEAR:
            # S1_RateOfStorageCharge
             model += RateOfStorageCharge.get(ci(rsly)) == pulp.lpSum([RateOfActivity.get(ci([rsly[0], rsly[2], *mt, rsly[3]])) * TechnologyToStorage.get(ci([*rsly[0:2], *mt]), dflt.get('TechnologyToStorage'))  for mt in MODE_OF_OPERATION_TECHNOLOGY if TechnologyToStorage.get(ci(([*rsly[0:2],*mt])), dflt.get('TechnologyToStorage')) > 0]), ""
            # S2_RateOfStorageDischarge
             model += RateOfStorageDischarge.get(ci(rsly)) == pulp.lpSum([RateOfActivity.get(ci([rsly[0], rsly[2], *mt, rsly[3]])) * TechnologyFromStorage.get(ci([*rsly[0:2], *mt]), dflt.get('TechnologyFromStorage')) for mt in MODE_OF_OPERATION_TECHNOLOGY if TechnologyFromStorage.get(ci([*rsly[0:2], *mt]), dflt.get('TechnologyFromStorage')) > 0]), ""

        for rsly in REGION_STORAGE_TIMESLICE_YEAR:
            #S1_and_S2_StorageLevelTimesliceStart  
            if int(rsly[2]) == int(min(TIMESLICE)):
                model += StorageLevelTimesliceStart.get(ci(rsly)) == StorageLevelYearStart.get(ci([*rsly[0:2], rsly[3]])), ""
            else:
                model += StorageLevelTimesliceStart.get(ci(rsly)) == StorageLevelTimesliceStart.get(ci([*rsly[0:2], str(int(rsly[2])-1), rsly[3]])) - StorageLosses.get(ci([*rsly[0:2], str(int(rsly[2])-1), rsly[3]]))  + ((RateOfStorageCharge.get(ci([*rsly[0:2], str(int(rsly[2])-1), rsly[3]])) - RateOfStorageDischarge.get(ci([*rsly[0:2], str(int(rsly[2])-1), rsly[3]]))) * YearSplit.get(ci([str(int(rsly[2])-1), rsly[3]]))), ""

        for rs in REGION_STORAGE:
            #SC8_StorageRefilling 
            model += 0 == pulp.lpSum([RateOfActivity.get(ci([rs[0], *lmty])) * TechnologyToStorage.get(ci([*rs[0:2], *lmty[1:3]]), dflt.get('TechnologyToStorage')) * YearSplit.get(ci([lmty[0], lmty[3]])) for lmty in TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY_YEAR if TechnologyToStorage.get(ci(([*rs[0:2], *lmty[1:3]])), dflt.get('TechnologyToStorage')) > 0]) - pulp.lpSum([RateOfActivity.get(ci([rs[0], *lmty])) * TechnologyFromStorage.get(ci([*rs[0:2], *lmty[1:3]]), dflt.get('TechnologyFromStorage')) * YearSplit.get(ci([lmty[0], lmty[3]])) for lmty in TIMESLICE_MODE_OF_OPERATION_TECHNOLOGY_YEAR if TechnologyFromStorage.get(ci([*rs[0:2], *lmty[1:3]]), dflt.get('TechnologyFromStorage')) > 0]) , ""

        #===== Storage Constraints ====

        for rsy in REGION_STORAGE_YEAR:
        # SI3_TotalNewStorage
            model += AccumulatedNewStorageCapacity.get(ci(rsy)) ==  pulp.lpSum([NewStorageCapacity.get(ci([*rsy[0:2], yy])) for yy in YEAR if (float(int(rsy[2]) - int(yy)) < float(OperationalLifeStorage.get(ci(rsy[0:2]), dflt.get('OperationalLifeStorage')))) and (int(rsy[2])-int(yy) >= 0)]), ""

        # SI1_StorageUpperLimit
            model += StorageUpperLimit.get(ci(rsy)) == (AccumulatedNewStorageCapacity.get(ci(rsy)) + ResidualStorageCapacity.get(ci(rsy), dflt.get('ResidualStorageCapacity'))), ""

        # SI1_StorageMaxCapacity
            model += StorageUpperLimit.get(ci(rsy)) <= StorageMaxCapacity.get(ci([rsy[0:2]]), dflt.get('StorageMaxCapacity')), ""

        for rsly in REGION_STORAGE_TIMESLICE_YEAR:
            #SC1_LowerLimit
            model += StorageLevelTimesliceStart.get(ci(rsly)) >= MinStorageCharge.get(ci([*rsly[0:2], rsly[3]]), dflt.get('MinStorageCharge')) * StorageUpperLimit.get(ci([*rsly[0:2], rsly[3]])), ""

            #SC2_Upper_Limit
            model += StorageLevelTimesliceStart.get(ci(rsly)) <= StorageUpperLimit.get(ci([*rsly[0:2], rsly[3]])), "" 

            #SC3_Charging_Upper_Limit
            #model += StorageMaxChargeRate.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageMaxChargeRate')) >= StorageLevelTimesliceStart.get(ci(rsly)) - StorageLevelTimesliceStart.get(ci([*rsly[0:2], str(int(rsly[2])-1), rsly[3]])), ""

            #SC4_Charging_Lower_Limit
            #model += StorageMaxDischargeRate.get(ci([*rsly[0:2], rsly[3]]), dflt.get('StorageMaxDischargeRate')) >= StorageLevelTimesliceStart.get(ci([*rsly[0:2], str(int(rsly[2])-1), rsly[3]])) - StorageLevelTimesliceStart.get(ci(rsly)), ""

        # ====  Storage Investments  ====   

        # SI4_UndiscountedCapitalInvestmentStorage
        for rsy in REGION_STORAGE_YEAR: 
            model += CapitalInvestmentStorage.get(ci(rsy)) == CapitalCostStorage.get(ci(rsy), dflt.get('CapitalCostStorage')) * NewStorageCapacity.get(ci(rsy)), ""
            # SI5_DiscountingCapitalInvestmentStorage
            model += DiscountedCapitalInvestmentStorage.get(ci(rsy)) == CapitalInvestmentStorage.get(ci(rsy)) * (1/ ((1+DiscountRateSto.get(ci(rsy[0:2]), dflt.get('DiscountRateSto')))**(int(rsy[2]) - int(min(YEAR))))), ""
            # SI6_SalvageValueStorageAtEndOfPeriod1
            if float(int(rsy[2]) + OperationalLifeStorage.get(ci(rsy[0:2]), dflt.get('OperationalLifeStorage'))) - 1 <= float(max(YEAR)):
                model += SalvageValueStorage.get(ci(rsy)) == 0, ""
            # SI7_SalvageValueStorageAtEndOfPeriod2
            if ((DepreciationMethod.get(rsy[0], dflt.get('DepreciationMethod')) == 1) and (float(int(rsy[2])+OperationalLifeStorage.get(ci(rsy[0:2]), dflt.get('OperationalLifeStorage'))-1) > float(max(YEAR))) and (DiscountRateSto.get(ci(rsy[0:2]), dflt.get('DiscountRateSto')) == 0)) or ((DepreciationMethod.get(rsy[0], dflt.get('DepreciationMethod')) == 2) and (float(int(rsy[2])+OperationalLifeStorage.get(ci(rsy[0:2]), dflt.get('OperationalLifeStorage'))-1) > float(max(YEAR)))):
                model += SalvageValueStorage.get(ci(rsy)) == CapitalInvestmentStorage.get(ci(rsy)) * (1-(int(max(YEAR))-int(rsy[2])+1))/OperationalLifeStorage.get(ci(rsy[0:2]), dflt.get('OperationalLifeStorage')), ""
            # SI8_SalvageValueStorageAtEndOfPeriod3
            if (DepreciationMethod.get(rsy[0], dflt.get('DepreciationMethod')) == 1) and (float(int(rsy[2])+OperationalLifeStorage.get(ci(rsy[0:2]), dflt.get('OperationalLifeStorage'))-1) > float(max(YEAR))) and (DiscountRateSto.get(ci(rsy[0:2]), dflt.get('DiscountRateSto')) > 0):
                model += SalvageValueStorage.get(ci(rsy)) == CapitalInvestmentStorage.get(ci(rsy)) * (1-(((1+DiscountRateSto.get(ci(rsy[0:2]), dflt.get('DiscountRateSto')))**(int(max(YEAR)) - int(rsy[2])+1)-1)/((1+DiscountRateSto.get(ci(rsy[0:2]), dflt.get('DiscountRateSto')))**OperationalLifeStorage.get(ci(rsy[0:2]), dflt.get('OperationalLifeStorage'))-1))), ""
            # SI9_SalvageValueStorageDiscountedToStartYear
            model += DiscountedSalvageValueStorage.get(ci(rsy)) == SalvageValueStorage.get(ci(rsy)) * (1 /((1+DiscountRateSto.get(ci(rsy[0:2]), dflt.get('DiscountRateSto')))**(int(max(YEAR))-int(min(YEAR))+1))), ""
            # SI10_TotalDiscountedCostByStorage
            model += TotalDiscountedStorageCost.get(ci(rsy)) == DiscountedCapitalInvestmentStorage.get(ci(rsy))-DiscountedSalvageValueStorage.get(ci(rsy)), ""

        # ====  Capital Costs  ====

        for rty in REGION_TECHNOLOGY_YEAR:
            # CC1_UndiscountedCapitalInvestment
            model += CapitalInvestment.get(ci(rty)) == CapitalCost.get(ci(rty), dflt.get('CapitalCost')) * NewCapacity.get(ci(rty)),  ""
            # CC2_DiscountingCapitalInvestment
            model += DiscountedCapitalInvestment.get(ci(rty)) == CapitalInvestment.get(ci(rty)) * (1/((1 + DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech'))) ** (int(rty[2]) - int(min(YEAR))))), ""

        # ====  Salvage Value  ====

            # SV1_SalvageValueAtEndOfPeriod1
            if (DepreciationMethod.get(rty[0], dflt.get('DepreciationMethod')) == 1) and (float(int(rty[2]) + OperationalLife.get(ci(rty[0:2]), dflt.get('OperationalLife'))) - 1 > float(max(YEAR))) and (DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech')) > 0):
                model += SalvageValue.get(ci(rty)) == CapitalCost.get(ci(rty), dflt.get('CapitalCost')) * NewCapacity.get(ci(rty)) * (1 - (((1 +  DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech'))) ** (int(max(YEAR)) - int(rty[2]) + 1) - 1) / ((1 +  DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech'))) ** OperationalLife.get(ci(rty[0:2]), dflt.get('OperationalLife')) - 1))), ""
            # SV2_SalvageValueAtEndOfPeriod2
            if ((DepreciationMethod.get(rty[0], dflt.get('DepreciationMethod')) == 1) and (float(int(rty[2]) + OperationalLife.get(ci(rty[0:2]), dflt.get('OperationalLife'))) - 1 > float(max(YEAR))) and ( DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech')) == 0)) or ((DepreciationMethod.get(rty[0], dflt.get('DepreciationMethod')) == 2) and (float(int(rty[2]) + OperationalLife.get(ci(rty[0:2]), dflt.get('OperationalLife'))) - 1 > float(max(YEAR)))):
                model += SalvageValue.get(ci(rty)) == CapitalCost.get(ci(rty), dflt.get('CapitalCost')) * NewCapacity.get(ci(rty)) * (1 - (int(max(YEAR)) - int(rty[2]) + 1) / OperationalLife.get(ci(rty[0:2]), dflt.get('OperationalLife'))), ""
            # SV3_SalvageValueAtEndOfPeriod3)
            if float(int(rty[2]) + OperationalLife.get(ci(rty[0:2]), dflt.get('OperationalLife')) - 1) <= float(max(YEAR)):
                model += SalvageValue.get(ci(rty)) == 0, ""
            # SV4_SalvageValueDiscountedToStartYear
            model += DiscountedSalvageValue.get(ci(rty)) == SalvageValue.get(ci(rty)) * (1 / ((1 +  DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech'))) ** (1 + int(max(YEAR)) - int(min(YEAR))))), ""

        # ====  Operating Costs  ====

            # OC1_OperatingCostsVariable
            model += AnnualVariableOperatingCost.get(ci(rty)) == pulp.lpSum([TotalAnnualTechnologyActivityByMode.get(ci([rty[0], m, *rty[1:3]])) * VariableCost.get(ci([rty[0], m, *rty[1:3]]), dflt.get('VariableCost')) for m in MODE_OF_OPERATION]), ""
            # OC2_OperatingCostsFixedAnnual
            model += AnnualFixedOperatingCost.get(ci(rty)) == TotalCapacityAnnual.get(ci(rty)) * FixedCost.get(ci(rty), dflt.get('FixedCost')), ""
            # OC3_OperatingCostsTotalAnnual
            model += OperatingCost.get(ci(rty)) == AnnualFixedOperatingCost.get(ci(rty)) + AnnualVariableOperatingCost.get(ci(rty)), ""
            # OC4_DiscountedOperatingCostsTotalAnnual
            model += DiscountedOperatingCost.get(ci(rty)) == OperatingCost.get(ci(rty)) * (1 / ((1 +  DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech'))) ** (int(rty[2]) - int(min(YEAR)) + 0.5))), ""

        # ====  Total Discounted Costs  ====

        for ry in REGION_YEAR:
            # TDC2_TotalDiscountedCost
            model += TotalDiscountedCost.get(ci(ry)) == pulp.lpSum([TotalDiscountedCostByTechnology.get(ci([ry[0], t, ry[1]])) for t in TECHNOLOGY]) + pulp.lpSum([TotalDiscountedStorageCost.get(ci([ry[0], s, ry[1]])) for s in STORAGE]), ""

        for rty in REGION_TECHNOLOGY_YEAR:
            # TDC1_TotalDiscountedCostByTechnology
            model += TotalDiscountedCostByTechnology.get(ci(rty)) == DiscountedOperatingCost.get(ci(rty)) + DiscountedCapitalInvestment.get(ci(rty)) + DiscountedTechnologyEmissionsPenalty.get(ci(rty)) - DiscountedSalvageValue.get(ci(rty)), ""

        # ====  Total Capacity Constraints  ====

            # TCC1_TotalAnnualMaxCapacityConstraint
            model += TotalCapacityAnnual.get(ci(rty)) <= TotalAnnualMaxCapacity.get(ci(rty), dflt.get('TotalAnnualMaxCapacity')), ""
            # TCC2_TotalAnnualMinCapacityConstraint
            if TotalAnnualMinCapacity.get(ci(rty), dflt.get('TotalAnnualMinCapacity')) > 0:
                model += TotalCapacityAnnual.get(ci(rty)) >= TotalAnnualMinCapacity.get(ci(rty), dflt.get('TotalAnnualMaxCapacity')), ""

        # ====  New Capacity Constraints  ====

            # NCC1_TotalAnnualMaxNewCapacityConstraint
            model += NewCapacity.get(ci(rty)) <= TotalAnnualMaxCapacityInvestment.get(ci(rty), dflt.get('TotalAnnualMaxCapacityInvestment')), ""
            # NCC2_TotalAnnualMinNewCapacityConstraint
            if TotalAnnualMinCapacityInvestment.get(ci(rty), dflt.get('TotalAnnualMinCapacityInvestment')) > 0:
                model += NewCapacity.get(ci(rty)) >= TotalAnnualMinCapacityInvestment.get(ci(rty), dflt.get('TotalAnnualMinCapacityInvestment')), ""

        # ====  Annual Activity Constraints  ====

            # AAC1_TotalAnnualTechnologyActivity
            model += TotalTechnologyAnnualActivity.get(ci(rty)) == pulp.lpSum([RateOfTotalActivity.get(ci([rty[0], l, *rty[1:3]])) * YearSplit.get(ci([l, rty[2]])) for l in TIMESLICE]), ""
            # AAC2_TotalAnnualTechnologyActivityUpperLimit
            model += TotalTechnologyAnnualActivity.get(ci(rty)) <= TotalTechnologyAnnualActivityUpperLimit.get(ci(rty), dflt.get('TotalTechnologyAnnualActivityUpperLimit')), ""
            # AAC3_TotalAnnualTechnologyActivityLowerLimit
            if TotalTechnologyAnnualActivityLowerLimit.get(ci(rty), dflt.get('TotalTechnologyAnnualActivityLowerLimit')) > 0:
                model += TotalTechnologyAnnualActivity.get(ci(rty)) >= TotalTechnologyAnnualActivityLowerLimit.get(ci(rty), dflt.get('TotalTechnologyAnnualActivityLowerLimit')), ""

        # ====  Total Activity Constraints  ====

        for rt in REGION_TECHNOLOGY:
            # TAC1_TotalModelHorizonTechnologyActivity
            model += TotalTechnologyModelPeriodActivity.get(ci(rt)) == pulp.lpSum([TotalTechnologyAnnualActivity.get(ci([*rt, y])) for y in YEAR]), ""
            # TAC2_TotalModelHorizonTechnologyActivityUpperLimit
            if TotalTechnologyModelPeriodActivityUpperLimit.get(ci(rt), dflt.get('TotalTechnologyModelPeriodActivityUpperLimit')) > 0:
                model += TotalTechnologyModelPeriodActivity.get(ci(rt)) <= TotalTechnologyModelPeriodActivityUpperLimit.get(ci(rt), dflt.get('TotalTechnologyModelPeriodActivityUpperLimit')), ""
            # TAC3_TotalModelHorizenTechnologyActivityLowerLimit
            if TotalTechnologyModelPeriodActivityLowerLimit.get(ci(rt), dflt.get('TotalTechnologyModelPeriodActivityLowerLimit')) > 0:
                model += TotalTechnologyModelPeriodActivity.get(ci(rt)) >= TotalTechnologyModelPeriodActivityLowerLimit.get(ci(rt), dflt.get('TotalTechnologyModelPeriodActivityLowerLimit')), ""

        # ====  Reserve Margin Constraint  ====

        for ry in REGION_YEAR:
            # RM1_ReserveMargin_TechnologiesIncluded_In_Activity_Units
            model += TotalCapacityInReserveMargin.get(ci(ry)) == pulp.lpSum([TotalCapacityAnnual.get(ci([ry[0], t, ry[1]])) * ReserveMarginTagTechnology.get(ci([ry[0], t, ry[1]]), dflt.get('ReserveMarginTagTechnology')) * CapacityToActivityUnit.get(ci([ry[0], t]), dflt.get('CapacityToActivityUnit')) for t in TECHNOLOGY]), ""

        for rly in REGION_TIMESLICE_YEAR:
            # RM2_ReserveMargin_FuelsIncluded
            model += DemandNeedingReserveMargin.get(ci(rly)) == pulp.lpSum([RateOfProduction.get(ci([rly[0], f, *rly[1:3]])) * ReserveMarginTagFuel.get(ci([rly[0], f, rly[2]]), dflt.get('ReserveMarginTagFuel')) for f in FUEL]), ""
            # RM3_ReserveMargin_Constraint
            model += DemandNeedingReserveMargin.get(ci(rly)) <= TotalCapacityInReserveMargin.get(ci([rly[0], rly[2]])) * (1/ReserveMargin.get(ci([rly[0], rly[2]]), dflt.get('ReserveMargin'))), ""

        # ====  RE Production Target  ====

        for rfty in REGION_FUEL_TECHNOLOGY_YEAR:
            # RE1_FuelProductionByTechnologyAnnual
            model += ProductionByTechnologyAnnual.get(ci(rfty)) == pulp.lpSum([ProductionByTechnology.get(ci([rfty[0], l, *rfty[1:4]])) for l in TIMESLICE]), ""

        for ry in REGION_YEAR:
            # RE2_TechIncluded
            # model += TotalREProductionAnnual.get(ci(ry)) == pulp.lpSum([ProductionByTechnologyAnnual.get(ci([ry[0], *ft, ry[1]])) * RETagTechnology.get(ci([ry[0], ft[1], ry[1]]), dflt.get('RETagTechnology')) for ft in FUEL_TECHNOLOGY]), ""

            # RE3_FuelIncluded
            model += RETotalProductionOfTargetFuelAnnual.get(ci(ry)) == pulp.lpSum([RateOfProduction.get(ci([ry[0], *fl, ry[1]])) * YearSplit.get(ci([fl[1], ry[1]])) * RETagFuel.get(ci([ry[0], fl[0], ry[1]]), dflt.get('RETagFuel')) for fl in FUEL_TIMESLICE]), ""
            # RE4_EnergyConstraint
            # model += TotalREProductionAnnual.get(ci(ry)) >= REMinProductionTarget.get(ci(ry), dflt.get('REMinProductionTarget')) * RETotalProductionOfTargetFuelAnnual.get(ci(ry)), ""

            # Combined: RE4_EnergyConstraint >= RE2_TechIncluded
            model += pulp.lpSum([ProductionByTechnologyAnnual.get(ci([ry[0], *ft, ry[1]])) * RETagTechnology.get(ci([ry[0], ft[1], ry[1]]), dflt.get('RETagTechnology')) for ft in FUEL_TECHNOLOGY]) >= REMinProductionTarget.get(ci(ry), dflt.get('REMinProductionTarget')) * RETotalProductionOfTargetFuelAnnual.get(ci(ry)), ""

        # for rfty in REGION_FUEL_TECHNOLOGY_YEAR:
        #     # RE5_FuelUseByTechnologyAnnual
        #     model += UseByTechnologyAnnual.get(ci(rfty)) == pulp.lpSum([RateOfUseByTechnology.get(ci([*rfty[0:2], l, *rfty[2:4]])) * YearSplit.get(ci([l, rfty[3]])) for l in TIMESLICE]), ""

        # ====  Emissions Accounting  ====

        for remty in REGION_EMISSION_MODE_OF_OPERATION_TECHNOLOGY_YEAR:
            # E1_AnnualEmissionProductionByMode
            model += AnnualTechnologyEmissionByMode.get(ci(remty)) == EmissionActivityRatio.get(ci(remty), dflt.get('EmissionActivityRatio')) * TotalAnnualTechnologyActivityByMode.get(ci([remty[0], *remty[2:5]])), ""

        for rety in REGION_EMISSION_TECHNOLOGY_YEAR:
            # E2_AnnualEmissionProduction
            model += AnnualTechnologyEmission.get(ci(rety)) == pulp.lpSum([AnnualTechnologyEmissionByMode.get(ci([*rety[0:2], m, *rety[2:4]])) for m in MODE_OF_OPERATION]), ""
            # E3_EmissionsPenaltyByTechAndEmission
            model += AnnualTechnologyEmissionPenaltyByEmission.get(ci(rety)) == AnnualTechnologyEmission.get(ci(rety)) * EmissionsPenalty.get(ci([*rety[0:2], *rety[3]]), dflt.get('EmissionsPenalty')), ""
            print(EmissionsPenalty.get(ci([*rety[0:2], rety[3]]), dflt.get('EmissionsPenalty')))

        for rty in REGION_TECHNOLOGY_YEAR:
            # E4_EmissionsPenaltyByTechnology
            model += AnnualTechnologyEmissionsPenalty.get(ci(rty)) == pulp.lpSum([AnnualTechnologyEmissionPenaltyByEmission.get(ci([rty[0], e, *rty[1:3]])) for e in EMISSION]), ""
            # E5_DiscountedEmissionsPenaltyByTechnology
            model += DiscountedTechnologyEmissionsPenalty.get(ci(rty)) == AnnualTechnologyEmissionsPenalty.get(ci(rty)) * (1 / ((1 +  DiscountRateTech.get(ci(rty[0:2]), dflt.get('DiscountRateTech'))) ** (int(rty[2]) - int(min(YEAR)) + 0.5))), ""

        for rey in REGION_EMISSION_YEAR:
            # E6_EmissionsAccounting1
            model += AnnualEmissions.get(ci(rey)) == pulp.lpSum([AnnualTechnologyEmission.get(ci([*rey[0:2], t, rey[2]])) for t in TECHNOLOGY]), ""
            # E8_AnnualEmissionsLimit
            model += AnnualEmissions.get(ci(rey)) <= AnnualEmissionLimit.get(ci(rey), dflt.get('AnnualEmissionLimit')) - AnnualExogenousEmission.get(ci(rey), dflt.get('AnnualExogenousEmission')), ""

        for re in REGION_EMISSION:
            # E7_EmissionsAccounting2
            model += pulp.lpSum([AnnualEmissions.get(ci([*re, y])) for y in YEAR]) == ModelPeriodEmissions.get(ci(re)) - ModelPeriodExogenousEmission.get(ci(re), dflt.get('ModelPeriodExogenousEmission')), ""
            # E9_ModelPeriodEmissionsLimit
            model += ModelPeriodEmissions.get(ci(re)) <= ModelPeriodEmissionLimit.get(ci(re), dflt.get('ModelPeriodEmissionLimit')), ""

        logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                     f"Model is built.")

        # ------------------------------------------------------------------------------------------------------------------
        #    SAVE MODEL
        # ------------------------------------------------------------------------------------------------------------------

        # Write model to LP-file
        # model.writeLP(f"{modelName}_{i}.lp")

        # ------------------------------------------------------------------------------------------------------------------
        #    SOLVE
        # ------------------------------------------------------------------------------------------------------------------

        model.solve()
        logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                     f"Model is solved. Solution is: "
                     f"{pulp.LpStatus[model.status]}")

        # ------------------------------------------------------------------------------------------------------------------
        #    SAVE RESULTS
        # ------------------------------------------------------------------------------------------------------------------       
    
        if str(pulp.LpStatus[model.status]) == "Optimal":
                logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                             f"The optimal solution found a cost value of "
                             f"{round(model.objective.value(), 2)}")

                # Create dataframe to save results after the model was run the first time
                if i == 0:
                    res_df = pd.DataFrame()
                res_df = pd.concat([res_df, saveResultsTemporary(model, i, variables)])

                logging.info(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                             f"Results are saved temporarily.")
        else:
            logging.error(f"\t{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t"
                          f"Error: Optimisation status for Scenario_{i} is: {pulp.LpStatus[model.status]}")

        del model  # Delete model

        i += 1

    return (res_df)