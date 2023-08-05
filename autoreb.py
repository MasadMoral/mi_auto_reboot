
import os
import shutil
import tarfile
import requests
import sys
import re
import time
import random
import hashlib
import platform
import socket



router_ip_address="miwifi.com"
#router_ip_address = "192.168.31.1"
router_ip_address = "192.168.0.108"
# get stok
def get_stok(router_ip_address):
    try: 
        r0 = requests.get("http://{router_ip_address}/cgi-bin/luci/web".format(router_ip_address=router_ip_address))
    except:
        print ("Xiaomi router not found...")
        return None
    try:	
        mac = re.findall(r'deviceId = \'(.*?)\'', r0.text)[0]
    except:
        print ("Xiaomi router not found...")
        return None
    key = re.findall(r'key: \'(.*)\',', r0.text)[0]
    nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
    router_password = "Djdg@@01"
    account_str = hashlib.sha1((router_password + key).encode('utf-8')).hexdigest()
    password = hashlib.sha1((nonce + account_str).encode('utf-8')).hexdigest()
    data = "username=admin&password={password}&logtype=2&nonce={nonce}".format(password=password,nonce=nonce)
    r1 = requests.post("http://{router_ip_address}/cgi-bin/luci/api/xqsystem/login".format(router_ip_address=router_ip_address), 
        data = data, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    try:
        stok = re.findall(r'"token":"(.*?)"',r1.text)[0]
    except:
        print("Failed to get stok in login response '{}'".format(r1.text))
        return None
    return stok

stok = get_stok(router_ip_address) or input("You need to get the stok manually, then input the stok here: ")

def reboot_router(router_ip_address, stok):
 
    reboot_url = f"http://{router_ip_address}/cgi-bin/luci/;stok={stok}/api/xqsystem/reboot"
    reboot_data = {"client": "web"}

    try:
        response = requests.post(reboot_url, data=reboot_data)
        if response.status_code == 200:
            print("Router reboot command sent successfully.\nRebooting.. . . .. .")
        else:
            print("Failed to send reboot command.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    router_ip_address="miwifi.com"
    #router_ip_address = "192.168.31.1"
    router_ip_address = input("Router IP address [press enter for using the default '{}']: ".format(router_ip_address)) or router_ip_address
    router_password = input("Enter router admin password: ")



    if stok:
        reboot_router(router_ip_address, stok)
