import sys
import os
import time

# Get the current directory of the script
server_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate one folder back to reach the parent directory
exp_dir = os.path.abspath(os.path.join(server_dir, os.pardir))

print("ok")


sys.path.append(f"{exp_dir}/server/scope")
from scope import Scope

# *** Local includes ***
from yaml_utils import *

#   Read YAML file
config = read_yaml_file(f"{exp_dir}/config.yaml")

print("ok")

#   INFO
info = config.get('info', {})
exp_name = info.get('exp_name')
server_user_name = info.get('server_user_name')
data_save_path = info.get('data_save_path')

print("ok")

#   CONTROL
control_yaml = config.get('control', {})

#   ENERGY PROFILER SYSTEM SETTINGS --> ToDo Check if it is definied in config file
scope_yaml = config.get('scope', {})


import subprocess

# def ping_ip(ip_address):
#     try:
#         # Execute the ping command
#         output = subprocess.check_output(["ping", "-n", "4", ip_address], universal_newlines=True)
#         return output
#     except subprocess.CalledProcessError as e:
#         return f"Failed to ping {ip_address}. Error: {e}"


# result = ping_ip(scope_yaml.get("ip"))
# print(result)



# try:
scope = Scope(scope_yaml.get("ip"))
print(scope)
print(scope_yaml.get("bandwidth_hz"))
print(scope_yaml.get("center_hz"))
print(scope_yaml.get("span_hz"))
print(scope_yaml.get("rbw_hz"))
scope.setup(scope_yaml.get("bandwidth_hz"), scope_yaml.get("center_hz"), scope_yaml.get("span_hz"), scope_yaml.get("rbw_hz"))
print("Setup scope")
# except:
    # print("Can not connect to the scope or something went wrong!")
    # print("1) Check network connection")
    # print("2) (optionally) Reboot system")
    # exit()

# no_active_transmitters = None

# while 1:
#     # power_dBm = scope.get_power_dBm_peaks(scope_yaml.get("cable_loss"), no_active_transmitters)


#     print(f"channel 1: {scope.get_channel_peak_power_dBm(1)}")
#     time.sleep(1)
#     print(f"channel 2: {scope.get_channel_peak_power_dBm(2)}")
#     time.sleep(1)