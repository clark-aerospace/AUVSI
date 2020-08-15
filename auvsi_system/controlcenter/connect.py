import os

def connect(URL,Username,Password):
    cmd = "cd /interop/client && ./tools/interop_cli.py  --url "
    cmd += URL + " "
    cmd += "--username "
    cmd += Username + " "
    cmd += "--password " 
    cmd += Password + " "
    cmd += "mission --mission_id 1 > /interop/client/AUVSI_System/controlcenter/text.json"
    os.system(cmd)