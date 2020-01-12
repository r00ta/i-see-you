import subprocess

cmd = 'cat /proc/cpuinfo | grep Serial | cut -d \' \' -f 2'
ps = subprocess.Popen(
    cmd,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
DEVICE_ID = str(ps.communicate()[0]).strip('\n')

