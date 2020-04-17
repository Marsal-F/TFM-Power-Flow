# -*- coding: utf-8 -*-
"""
mferr: case4gs from scratch (decimal error somewhere)


"""
import pandapower as pp
#import pandapower.networks as pn





net = pp.create_empty_network() #create an empty network

#Bus definition
bus0 = pp.create_bus (net, vn_kv=230, name='Bus1', index=0, geodata=None, type='b', zone=1, in_service=True, max_vm_pu=1.1, min_vm_pu=0.9, coords=None)
bus1 = pp.create_bus (net, vn_kv=230, name='Bus2', index=1, geodata=None, type='b', zone=1, in_service=True, max_vm_pu=1.1, min_vm_pu=0.9, coords=None)
bus2 = pp.create_bus (net, vn_kv=230, name='Bus3', index=2, geodata=None, type='b', zone=1, in_service=True, max_vm_pu=1.1, min_vm_pu=0.9, coords=None)
bus3 = pp.create_bus (net, vn_kv=230, name='Bus4', index=3, geodata=None, type='b', zone=1, in_service=True, max_vm_pu=1.1, min_vm_pu=0.9, coords=None)

#Load definition
load0 = pp.create_load(net, bus0, p_mw=50, q_mvar=30.99, const_z_percent=0, const_i_percent=0, name=None, scaling=1.0, index=0, in_service=True, type=None, controllable=False)
load1 = pp.create_load(net, bus1, p_mw=170, q_mvar=105.35, const_z_percent=0, const_i_percent=0, name=None, scaling=1.0, index=1, in_service=True, type=None, controllable=False)
load2 = pp.create_load(net, bus2, p_mw=200, q_mvar=123.94, const_z_percent=0, const_i_percent=0, name=None, scaling=1.0, index=2, in_service=True, type=None, controllable=False)
load3 = pp.create_load(net, bus3, p_mw=80, q_mvar=49.58, const_z_percent=0, const_i_percent=0, name=None, scaling=1.0, index=3, in_service=True, type=None, controllable=False)

#External grid definition

pp.create_ext_grid(net, bus0, vm_pu=1.0, va_degree=0.0, name=None, in_service=True, max_p_mw=0, min_p_mw=0, max_q_mvar=100, min_q_mvar=-100, index=0)

#Generation definition
gen0 = pp.create_gen(net, bus3, p_mw=318, vm_pu=1.02, name=None, index=0, max_q_mvar=100, min_q_mvar=-100, min_p_mw=0, max_p_mw=318, scaling=1.0, type=None, slack=False, controllable=True, in_service=True)

#Line definition
line0 = pp.create_line_from_parameters(net, from_bus = 0, to_bus = 1, length_km = 1, r_ohm_per_km = 5.33232, x_ohm_per_km = 26.6616, c_nf_per_km = 513.969, max_i_ka = 0.627555, name=None, index=0, type = 'ol', in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, max_loading_percent=100)
line1 = pp.create_line_from_parameters(net, from_bus = 0, to_bus = 2, length_km = 1, r_ohm_per_km = 3.93576, x_ohm_per_km = 19.6788, c_nf_per_km = 388.611, max_i_ka = 0.627555, name=None, index=1, type = 'ol', in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, max_loading_percent=100)
line2 = pp.create_line_from_parameters(net, from_bus = 1, to_bus = 3, length_km = 1, r_ohm_per_km = 3.93576, x_ohm_per_km = 19.6788, c_nf_per_km = 388.611, max_i_ka = 0.627555, name=None, index=2, type = 'ol', in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, max_loading_percent=100)
line3 = pp.create_line_from_parameters(net, from_bus = 2, to_bus = 3, length_km = 1, r_ohm_per_km = 6.72888, x_ohm_per_km = 33.6444, c_nf_per_km = 639.328, max_i_ka = 0.627555, name=None, index=3, type = 'ol', in_service=True, df=1.0, parallel=1, g_us_per_km=0.0, max_loading_percent=100)

pp.runpp(net)

print(net)
print('====bus results===')
print(net.res_bus)

#Result tables
print('====ext grid results===')
print(net.res_ext_grid)
print('====line results===')
print(net.res_line)
print('====load results===')
print(net.res_load)


