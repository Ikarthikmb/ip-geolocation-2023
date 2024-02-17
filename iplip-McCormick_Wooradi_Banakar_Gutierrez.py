#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 18:43:26 2023

@author: karthikmb
"""

import pandas as pd
import ipaddress
from scipy.interpolate import interp1d
import csv
import numpy as np

class IpLocation:
    def __init__(self):
        # with open("db/geolocationDatabaseIPv4-indiana-hammond.csv", "r") as csvfile:
        with open("geolocationDatabaseIPv4-indiana.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            self.data = []
            for row in reader:
                start_ip = int(ipaddress.IPv4Address(row[1]))
                end_ip = int(ipaddress.IPv4Address(row[2]))
                location_data = {"latitude": row[-3], "longitude": row[-2], "city": row[7]}
                self.data.append((start_ip, end_ip, location_data))

    def locate(self, ip):
        ipv4 = int(ipaddress.IPv4Address(ip))
        # print(f"IP address: {ip} -> {ipv4}")
        upper_ip = 0
        lower_ip = 0
        location_data = None
        for i in range(len(self.data)):
            if self.data[i][0] <= ipv4 <= self.data[i][1]:
                lower_ip, upper_ip = self.data[i][0], self.data[i][1]
                location_data = self.data[i][2]
                break

        if location_data is None:
            raise ValueError("IP address not found in geolocation database")

        latitude = location_data["latitude"]
        longitude = location_data["longitude"]

        f_lat = interp1d([lower_ip, upper_ip], [latitude, latitude], kind='linear')
        f_lon = interp1d([lower_ip, upper_ip], [longitude, longitude], kind='linear')

        interpolated_lat = f_lat(ipv4)
        interpolated_lon = f_lon(ipv4)
        interpolated_city = location_data['city']

        return interpolated_lat, interpolated_lon, interpolated_city

if __name__ == "__main__":
    print("Linear Interpolation Technique")
    # test_ip = "65.175.34.127"
    ip_locator = IpLocation()
    with open('test_ips.txt', 'r') as ip_testfile:
        for test_ip in ip_testfile:
            test_ip = test_ip.strip()
            print(f"Location for IP {test_ip}:")
            try:
                location = ip_locator.locate(test_ip)    
            except ValueError as error:
                print("\t", error)
            else:
                print(f"\t {location[2]}, Latitude: {location[0]}, Longitude: {location[1]}\n")
