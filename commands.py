import wmi
import pythoncom
from tabulate import tabulate
import argparse
import sys

def battery_wmi(key, dict, computer = '.', password = '', user = ''):
    try:
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password='123', user=user)
        dict[key] = ''
        for property in obj.win32_Battery():
            dict[key] += '\tName : ' + property.Name + '\n'
            dict[key] += '\tStatus : ' + property.Status + '\n'
            dict[key] += '\n'
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception.args)
    finally:
        pythoncom.CoUninitialize()
        return 0

def cpu_wmi(key, dict, computer = '.', password = '', user = ''):
    try:
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password=password, user=user)
        dict[key] = ''
        for property in obj.win32_Processor():
            dict[key] += '\tName : ' + property.Name + '\n'
            dict[key] += '\tStatus : ' + property.Status + '\n'
            dict[key] += '\n'
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception.args)
    finally:
        pythoncom.CoUninitialize()
        return 0

def gpu_wmi(key, dict, computer = '.', password='', user=''):
    try:
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password=password, user=user)
        dict[key] = ''
        for property in obj.win32_VideoController():
            dict[key] += '\tName : ' + property.Name + '\n'
            dict[key] += '\tStatus : ' + property.Status + '\n'
            dict[key] += '\n'
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception.args)
    finally:
        pythoncom.CoUninitialize()
        return 0
    

def disk_wmi(key, dict, computer = '.', password='', user=''):
    try:
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password=password, user=user)
        dict[key] = ''
        for property in obj.win32_DiskDrive():
            dict[key] += '\tName : ' + property.Model + '\n'
            dict[key] += '\tStatus : ' + property.Status + '\n'
            dict[key] += '\n'
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception)
    finally:
        pythoncom.CoUninitialize()
        return 0

def monitor_wmi(key, dict, computer = '.', password='', user = ''):
    try:
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password=password, user=user)
        dict[key] = ''
        for property in obj.win32_DesktopMonitor():
            dict[key] += '\tName : ' + str(property.PNPDeviceID) + '\n'
            dict[key] += '\tStatus : ' + property.Status + '\n'
            dict[key] += '\n'
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception.args)
    finally:
        pythoncom.CoUninitialize()
        return 0

def ram_wmi(key, dict, computer = '.', password='', user=''):
    try:
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password=password, user=user)
        dict[key] = ''
        for property in obj.win32_PhysicalMemory():
            dict[key] += '\tName : ' + property.PartNumber + '\n'
            dict[key] += '\tCapacity : ' + property.Capacity + '\n'
            dict[key] += '\tSpeed : ' + str(property.Speed) + '\n'
            dict[key] += '\n'
        return 0
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception.args)
    finally:
        pythoncom.CoUninitialize()
        return 0

def adapters_wmi(key, dict, computer = '.', password='', user=''):
    try:    
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password=password, user=user)
        active = ''
        disabled = ''
        for property in obj.win32_NetworkAdapterConfiguration():
            if property.IPEnabled == True:
                active += '\tName : ' + property.Caption + '\n'
                active += '\tIPv4 : ' + str(property.IPAddress[0]) + '\n'
                active += '\tMAC : ' + str(property.MACAddress) + '\n'
                if property.DefaultIPGateway != None:
                    if len(property.DefaultIPGateway) > 0:
                        active += '\tDefault Gateway : ' + str(property.DefaultIPGateway[0]) + '\n'
                if property.DNSServerSearchOrder != None:
                    DNS_available = len(property.DNSServerSearchOrder)
                else:
                    DNS_available = 0
                if DNS_available > 0:
                    active += '\tDNS : ' + str(property.DNSServerSearchOrder[0]) + '\n'
                    if DNS_available > 1:
                        active += '\tAlternate DNS : ' + str(property.DNSServerSearchOrder[1]) + '\n'
                active += '\n'
            else:
                disabled += '\tName : ' + property.Caption + '\n'
        dict[key] = 'ACTIVE:\n' + active + 'DISABLED:\n' + disabled
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception.args)
    finally:
        pythoncom.CoUninitialize()
        return 0

def route_wmi(key, dict, computer = '.', password='', user=''):
    try:
        pythoncom.CoInitialize()
        obj = wmi.WMI(computer,password=password, user=user)
        obj1 = wmi.WMI(computer,password=password, user=user)
        table = {'Network Destination':[], 'Netmask':[], 'Gateway':[], 'Interface':[], 'Metric':[] }
        interface_map = {1:'127.0.0.1'}
        for property in obj1.win32_NetworkAdapterConfiguration():
            if property.IPEnabled == True:
                interface_map[property.InterfaceIndex] = property.IPAddress[0]
            else:
                interface_map[property.InterfaceIndex] = '127.0.0.1'
        for property in obj.win32_IP4RouteTable():
            table['Network Destination'].append(str(property.Destination))
            table['Netmask'].append(str(property.Mask))
            table['Gateway'].append(str(property.NextHop))
            table['Interface'].append(interface_map[property.InterfaceIndex])
            table['Metric'].append(str(property.Metric1))
        dict[key] = tabulate(table, headers='keys', tablefmt='fancy_grid')
    except wmi.x_access_denied:
        dict[key] = 'Access Denied'
    except wmi.x_wmi_authentication:
        dict[key] = 'Invalid combination of authentication properties'
    except Exception:
        dict[key] = 'Unknown error: ' + str(Exception.args)
    finally:
        pythoncom.CoUninitialize()
        return 0
    