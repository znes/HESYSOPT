# -*- coding: utf-8 -*-
"""
This module is used to configure the plotting. At the momemt it reads for
the default all results path  and creates a multiindex dataframe. This is
used by the different plotting-modules. Also, colors are set here.

Note: This is rather ment to illustrate, how hesysopt results can be plotted,
than to depict a complete plotting ready to use library.

"""
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

scenarios = ['1HBP', '2HBP', '4HBP']
homepath = os.path.expanduser('~')

main_df = pd.DataFrame()
for s in scenarios:
    resultspath = os.path.join(homepath, 'hesysopt_simulation', s, 'results',
                               'all_results.csv')
    tmp = pd.read_csv(resultspath)
    tmp['Scenario'] = s
    main_df = pd.concat([main_df, tmp])

# restore orginial df multiindex
main_df.set_index(['Scenario', 'bus_label', 'type', 'obj_label', 'datetime'],
                   inplace=True)

# set colors
components = main_df.index.get_level_values('obj_label').unique()
colors = dict(zip(components,
                  sns.color_palette("coolwarm_r", len(components))))

# select heat flows from main_df
idx = pd.IndexSlice
heat_df = main_df.loc[idx[scenarios,
                          'heat_balance',
                          'to_bus', :, :]].unstack(['Scenario', 'obj_label'])
heat_df.columns = heat_df.columns.droplevel([0])
heat_df.columns.name = 'Unit'

el_df = main_df.loc[idx[scenarios,
                        'electrical_balance',
                        'to_bus', :, :]].unstack(['Scenario', 'obj_label'])