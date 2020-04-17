# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:41:38 2020

@author: mferr
"""


import pandapower.networks as pn
import pandapower as pp

net = pn.case4gs()

pp.runpp(net)

print(net.bus)
print(net)
print(net.res_bus)

#Result tables
print('==== External Grid ====')
print(net.res_ext_grid)
print('==== Lines info ====')
print(net.res_line)
print('==== Load info ====')
print(net.res_load)



