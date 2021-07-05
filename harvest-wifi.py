import os
import re
import subprocess

def get_output(command):
    executed_object = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    executed_data = executed_object.stdout.read() + executed_object.stderr.read()
    raw_data = executed_data.decode()
    return raw_data

def get_profiles():
    command = "netsh wlan show profiles"
    raw_data = get_output(command)
    pattern = "All User Profile\s+:\s+\w+"
    matches = re.findall(pattern, raw_data)
    if matches != []:
        profiles = [match.split(":")[-1].strip() for match in matches]
        return profiles

def get_profile_key(profile):
    command = f"netsh wlan show profiles {profile} key=clear"
    raw_data = get_output(command)
    pattern = "\s+Key Content\s+:\s?\w+"
    matches = re.findall(pattern, raw_data)
    if matches != []:
        key = matches[0].split(":")[-1].strip() 
        return key

def main():
    profiles = get_profiles()
    if profiles:
        for profile in profiles:
            key = get_profile_key(profile)
            if key:
                print(f"[+] Key for {profile}: {key}")
            else:
                print(f"[-] Could not find key for {profile}")
    else:
        print("Did not find any Users!")

if __name__ == "__main__":
    if os.name == "nt":
        main()
    else:
        print("[-] This Script Can Only Run On Windows Machines.")
