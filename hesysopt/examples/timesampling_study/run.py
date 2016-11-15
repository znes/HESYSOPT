# -*- coding: utf-8 -*-
"""
This module uses the functionalities from the app.py module for more flexbile
node manipulation.

"""
import os
import pdb
import logging
#from oemof.solph import Investment
from hesysopt.app import (create_nodes, create_energysystem, simulate,
                          main_path, write_results, dump_energysystem)

def run_scenario(sc, scenarios):
    """ Runs scenario

    Parameter
    ----------
    sc : string
        Name of the scenario (key in the scenarios dictionary)
    scenarios : dict
        Dictionary with scenario defintion build by scenario_builder
    """

    ####################### configure app #####################################
    arguments = {}
    arguments['--scenario_name'] = sc
    arguments['--node_data'] = scenarios[sc]['node_path']
    arguments['--sequence_data'] = scenarios[sc]['seq_path']
    arguments['--start'] = '01/01/2010T00:00'
    arguments['--end'] = '12/31/2010T23:00'
    arguments['--freq'] = scenarios[sc]['freq']
    arguments['--loglevel'] = 'INFO'
    arguments['--solver-output'] = 'True'
    arguments['--solver'] = 'gurobi'
    arguments['--mipgap'] = scenarios[sc].get('--mipgap', 0.0001)
    # output directory
    homepath = os.path.expanduser("~")
    mainpath = os.path.join(homepath, 'hesysopt_simulation')
    arguments['--output-directory'] =  mainpath

    ###########################################################################
    logging.info("Starting simulation with HESYSOPT!")
    # setting the path
    arguments['--output-directory'] = main_path(**arguments)
    # setting some logging stuff
    logging.getLogger().setLevel(getattr(logging, arguments['--loglevel']))
    if arguments['--loglevel'] == 'DEBUG':
        print(arguments)
    #if sc == '4HBP':
    #    pdb.set_trace()
    # create the nodes from csv-file
    # get the storage object
    #storage = [n for n in nodes.values() if n.label == 'STO'][0]
    # set the investment costs base points
    #storage.investment = Investment(ep_costs=basepoints)
    #pdb.set_trace()
    # create energy system
    es = create_energysystem(**arguments)

    # these will be added automatically
    create_nodes(**arguments)

    # create optimization model and solve it and write results back to energys
    om = simulate(es=es, **arguments)
    om.write(sc+'.lp',io_options={'symbolic_solver_labels':True})
    # write results to csv file
    write_results(es=es, om=om, **arguments)

    # dump the energysystem
    dump_energysystem(es, **arguments)

    #om.write(io_options={'symbolic_solver_labels': True})
    logging.info("Done with scenario {0}!".format(sc))

    return om, es

if __name__ == "__main__":
    from scenario_builder import scenarios_2013 as scenarios
    for k in scenarios.keys():
        run_scenario(sc=k, scenarios=scenarios)
