# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 11:51:46 2020

@author: mferr
Network concoct tool
Given a preformated CSV with a nº of buses, loads, trafos, switches data
it builds the net

"""

import pandapower as pp
import csv

net = pp.create_empty_network() #create an empty network

#Bus creation
Buses = {}
with open('Bus_data_test.csv', 'r') as Bus_data:
    for index, row in enumerate(csv.reader(Bus_data)):
        Buses["Bus{0}".format(index)] = pp.create_bus(net,
            vn_kv=float(row[0]), name=row[1], index=index, 
            geodata=None, type=row[4], zone=int(row[5]),
            in_service=(row[6]=="True"), max_vm_pu=float(row[7]),
            min_vm_pu=float(row[8]), coords=row[9])

assert len(Buses) > 0


print(Buses["Bus0"])


for name,value in Buses.items():
    globals()[name.lower()] = value
    
#Load allocation
    
Loads = {}
with open('Load_data.csv', 'r') as Load_data:
    for index, row in enumerate(csv.reader(Load_data)):
        Loads["Load{0}".format(index)] = pp.create_load(net,
            int(row[0]), p_mw=float(row[1]), q_mvar=float(row[2]), 
            const_z_percent=float(row[3]),const_i_percent=float(row[4]),
            name=None,scaling=1.0,index=index,in_service=(row[8]=="True"),
            type=None,controllable=(row[10]=="True"))

assert len(Loads) > 0


print(Loads["Load0"])


for name,value in Loads.items():
    globals()[name.lower()] = value
    
    
#Generators allocation    
Generation = {}
with open('Gen_data.csv', 'r') as Gen_data:
    for index, row in enumerate(csv.reader(Gen_data)):
        Generation["Gen{0}".format(index)] = pp.create_gen(net,
            int(row[0]), p_mw=float(row[1]), vm_pu=float(row[2]), 
            name=None, index=index, max_q_mvar=float(row[7]),min_q_mvar=float(row[8]),
            min_p_mw=float(row[6]),max_p_mw=float(row[5]), scaling=1.0, type=None, 
            slack=(row[11]=="True"),in_service=(row[12]=="True"),controllable=(row[13]=="True"))

assert len(Generation) > 0


print(Generation["Gen0"])


for name,value in Generation.items():
    globals()[name.lower()] = value
    
    

    
#External grid allocation

pp.create_ext_grid(net, bus0, vm_pu=1.0, va_degree=0.0, name=None, in_service=True, max_p_mw=0, min_p_mw=0, max_q_mvar=100, min_q_mvar=-100, index=0)
    
#External_grid = {}
#with open('Ext_data.csv', 'r') as Ext_grid:
#    for index, row in enumerate(csv.reader(Ext_grid)):
#        External_grid["ext_grid{0}".format(index)] = pp.create_ext_grid(net,
#            int(row[0]), vm_pu=float(row[1]),va_degree=float(row[2]), 
#            name=None,in_service=(row[9]=="True"),max_p_mw=float(row[5]),
#            min_p_mw=float(row[6]),max_q_mvar=float(row[7]),
#            min_q_mvar=float(row[8]),index=index)
#
#assert len(External_grid) > 0
#
#
#print(External_grid["ext_grid0"])
#
#
#for name,value in External_grid.items():
#    globals()[name.lower()] = value    
    
#Lines definition   

Lines = {}
with open('Line_data.csv', 'r') as Line_data:
    for index, row in enumerate(csv.reader(Line_data)):
        Lines["Line{0}".format(index)] = pp.create_line_from_parameters(net,
            int(row[0]), int(row[1]),length_km = float(row[2]), r_ohm_per_km = float(row[3]),
            x_ohm_per_km = float(row[4]), c_nf_per_km = float(row[5]), max_i_ka =float(row[6]),
            name=None, index=index, type = str(row[9]), in_service=(row[10]=="True"), df=int(row[11]),
            parallel=int(row[12]), g_us_per_km=float(row[13]), max_loading_percent=float(row[14]))

assert len(Lines) > 0


print(Lines["Line0"])


for name,value in Lines.items():
    globals()[name.lower()] = value   


#Briefing    
print(net)
print(net.line)
pp.runpp(net)
#Powerflow result tables
print('====bus results===')
print(net.res_bus)
print('====ext grid results===')
print(net.res_ext_grid)
print('====line results===')
print(net.res_line)
print('====generation results===')
print(net.res_gen)
print('====load results===')
print(net.res_load)
print('====generation results===')
print(net.gen)