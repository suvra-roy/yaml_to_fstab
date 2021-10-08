### Sample output
# /dev/sda1 /boot xfs defaults 1 2
# /dev/sda2 / ext4 defaults 0 1
# /dev/sdb1 /var/lib/postgresql ext4 defaults 0 2
# 192.168.4.5:/home /var/nfs/home nfs defaults,noexec,nosuid 0 0

import yaml

with open("input.yaml", "r") as stream:
    try:
        yml = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

output = []
for key in yml['fstab']:
    r = key # /dev/sda1
    temp = key.split("/")
    mount = ""
    if len(temp)>1 and temp[1] == 'dev':
        r += " "
        for k,v in yml['fstab'][key].items(): # {'mount': '/boot', 'type': 'xfs'}
            if k == 'mount':
                mount = v
            r += v
            r += " "

        if mount == '/boot':
            # defaults 1 2
            r += "defaults 1 2"
        elif mount == '/':
            # defaults 0 1
            r += "defaults 0 1"
        else:
            # defaults 0 2
            r += "defaults 0 2"
    else:
        # 192.168.4.5:/home /var/nfs/home nfs defaults,noexec,nosuid 0 0
        # r = 192.168.4.5
        tail = "defaults"
        for k,v in yml['fstab'][key].items(): # { }
            if k == 'mount':
                r += ":" + v + " " # r = 192.168.4.5:/home
            elif k == 'options':
                for val in yml['fstab'][key]['options']: # []
                    tail += "," + val # defaults,noexec,nosuid

            else:
                r += v + " " # r = 192.168.4.5:/home /var/nfs/home nfs

        tail += " 0 0" # defaults,noexec,nosuid 0 0
        r += tail # r = 192.168.4.5:/home /var/nfs/home nfs defaults,noexec,nosuid 0 0

    output.append(r)

with open('output.txt', 'w') as stream:
    s = "\n".join(i for i in output)
    stream.writelines(s)
