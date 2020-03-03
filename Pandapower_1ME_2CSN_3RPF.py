# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 22:26:37 2020

@author: mferr
"""
#=================TFM Power-Flow: Previous Steps====================
##Example 1
#import pandapower as pp
##create empty net
#net = pp.create_empty_network() 
#
##create buses
#b1 = pp.create_bus(net, vn_kv=20., name="Bus 1") #20kV voltage level bus
#b2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2") #0.4kV voltage level bus
#b3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3") #0.4kV voltage level bus
#
##create bus elements
#pp.create_ext_grid(net, bus=b1, vm_pu=1.02, name="Grid Connection")
#pp.create_load(net, bus=b3, p_mw=0.1, q_mvar=0.05, name="Load")
#
##create branch elements
#tid = pp.create_transformer(net, hv_bus=b1, lv_bus=b2, std_type="0.4 MVA 20/0.4 kV", name="Trafo")
#pp.create_line(net, from_bus=b2, to_bus=b3, length_km=0.1, name="Line",std_type="NAYY 4x50 SE")
#
#print(net.bus)
#print(net.trafo)
#pp.runpp(net)


#=========================================================
#Example 2: Creating Pandapower Networks
import pandapower as pp #import pandapower

net = pp.create_empty_network() #create an empty network

#Defining buses
bus1 = pp.create_bus(net, name="HV Busbar", vn_kv=110, type="b")
bus2 = pp.create_bus(net, name="HV Busbar 2", vn_kv=110, type="b")
bus3 = pp.create_bus(net, name="HV Transformer Bus", vn_kv=110, type="n")
bus4 = pp.create_bus(net, name="MV Transformer Bus", vn_kv=20, type="n")
bus5 = pp.create_bus(net, name="MV Main Bus", vn_kv=20, type="b")
bus6 = pp.create_bus(net, name="MV Bus 1", vn_kv=20, type="b")
bus7 = pp.create_bus(net, name="MV Bus 2", vn_kv=20, type="b")

print(net.bus)

#External grid definition
pp.create_ext_grid(net, bus1, vm_pu=1.02, va_degree=50) # Create an external grid connection

net.ext_grid #show external grid table

#Trafo definition
trafo1 = pp.create_transformer(net, bus3, bus4, name="110kV/20kV transformer", std_type="25 MVA 110/20 kV")

print(net.trafo)

#Linking lines
line1 = pp.create_line(net, bus1, bus2, length_km=10, std_type="N2XS(FL)2Y 1x300 RM/35 64/110 kV",  name="Line 1")
line2 = pp.create_line(net, bus5, bus6, length_km=2.0, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 2")
line3 = pp.create_line(net, bus6, bus7, length_km=3.5, std_type="48-AL1/8-ST1A 20.0", name="Line 3")
line4 = pp.create_line(net, bus7, bus5, length_km=2.5, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 4")

print(net.line)

#Switches (circuit breakers) on the low and high voltage sides
sw1 = pp.create_switch(net, bus2, bus3, et="b", type="CB", closed=True)
sw2 = pp.create_switch(net, bus4, bus5, et="b", type="CB", closed=True)

#Switches on the load side (Load Break Switches)

sw3 = pp.create_switch(net, bus5, line2, et="l", type="LBS", closed=True)
sw4 = pp.create_switch(net, bus6, line2, et="l", type="LBS", closed=True)
sw5 = pp.create_switch(net, bus6, line3, et="l", type="LBS", closed=True)
sw6 = pp.create_switch(net, bus7, line3, et="l", type="LBS", closed=False)
sw7 = pp.create_switch(net, bus7, line4, et="l", type="LBS", closed=True)
sw8 = pp.create_switch(net, bus5, line4, et="l", type="LBS", closed=True)

#Load details
#pp.create_load(net, bus7, p_mw=2, q_mvar=4, scaling=0.6, name="load")
pp.create_load(net, bus7, p_mw=2, q_mvar=4, const_z_percent=30, const_i_percent=20, name="zip_load")
print(net.load)

#Static generator
#Note that as pandapower is set on consumers point of view, to modalize generation it is needed to
#asign a negative value to the reactive power parameter
pp.create_sgen(net, bus7, p_mw=2, q_mvar=-0.5, name="static generator")
print(net.sgen)

#Create a voltage controlled generator. Same costumer point of view criteria.
pp.create_gen(net, bus6, p_mw=6, max_q_mvar=3, min_q_mvar=-3, vm_pu=1.03, name="generator") 

net.gen

#Shunt (capacitor bank model)
pp.create_shunt(net, bus3, q_mvar=-0.96, p_mw=0, name='Shunt')
net.shunt

#=========================================================
#Example/Continuation 3: #Running the powerflow
 
import pandapower as pp
import pandapower.networks
pp.runpp(net)

print(net)
print(net.res_bus)

#Loadflow analyis commands:
#Minimum voltage at a bus with load or generation
print(net.res_bus[net.bus.vn_kv==20.].vm_pu.min())

#Maximum voltage at a bus with load or generation
#Check steps in the net creation, differs from heading result
load_or_generation_buses = set(net.load.bus.values) | set(net.sgen.bus.values) | set(net.gen.bus.values)
print(net.res_bus.vm_pu.loc[load_or_generation_buses].max())

#Result tables
print(net.res_ext_grid)
print(net.res_line)
print(net.res_trafo)
print(net.res_load)
print(net.res_sgen)
print(net.res_gen)
print(net.res_shunt)

#Voltage angles and initialization
print(net.ext_grid.va_degree)
print(net.trafo.shift_degree)
print(net.res_bus.va_degree)

#Changing the condition into true to stop ignoring angle calculations. Somehow shift between radial (no angle influence) to meshed (necessty to calculate voltage angles)
pp.runpp(net, calculate_voltage_angles=True)

#As the power flow does not converge, initialization is nedded. Using DC loadflow.
pp.runpp(net, calculate_voltage_angles=True, init="dc")
print(net.res_bus.va_degree)

#Initialization using the last loadflow voltage results
pp.runpp(net, calculate_voltage_angles=True, init="results")
print(net.res_bus.va_degree) #What is stored in the "results" variable?

#Transformer model: Select either 'pi' or 't' transformer model

pp.runpp(net, trafo_model="t")
print(net.res_trafo)

pp.runpp(net, trafo_model="pi")
print(net.res_trafo)

#Rated current transformer loading criteria

pp.runpp(net, trafo_loading="current")
net.res_trafo

#Rated power transformer loading criteria

pp.runpp(net, trafo_loading="power")
net.res_trafo

#Note that the transformer loading does not affect any other power flow results except loading_percent parameter

#Generator reactive power limits (-3/3 MVar)
print(net.gen)

#The reactive power is exceeding the limits because the parameter enforce_q_lims is set to false (should appear to the previous variable print, but it does not, idk if for space reasons)
pp.runpp(net)
print(net.res_gen)

#Now we set this parameter to 'true' to apply the 3MVar threshold
pp.runpp(net, enforce_q_lims=True)
print(net.res_gen)

#Changing the power flow algorythm: as NR is set as default and GS does not provide better results in a complete analysis (according to papers),this section will be omitted.





