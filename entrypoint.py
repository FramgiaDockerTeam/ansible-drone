#!/usr/bin/python

import sys
import os
import json
import subprocess
import shlex

try:
    argv = sys.argv[2]
    argv = json.loads(argv)
    privateKey = argv['workspace']['keys']['private']
    print '[+] Setup injected private key'

    # cd to path
    src_path = argv['workspace']['path']

    # ansible_path
    ansible_path = src_path + "/.ansible"

    # ssh_key
    ssh_key = ansible_path + "/ssh_key/id_rsa"

    # ssh_key
    scm_key = ansible_path + "/scm_key/id_rsa"

    # print ("Repository's Private Key: %s") % privateKey

    with open(ssh_key, "w") as privateKeyFile:
        os.chmod(ssh_key, 0777)
        privateKeyFile.write(privateKey)

    with open("~/.ssh/id_rsa", "w") as privateKeyFile:
        os.chmod("~/.ssh/id_rsa", 0600)
        privateKeyFile.write(privateKey)

    os.system("ssh-keygen -f ~/.ssh/id_rsa -y > ~/.ssh/id_rsa.pub")
    os.system("eval \"$(ssh-agent -s)\"")
    os.system("ssh-add ~/.ssh/id_rsa")

    # print '[+] cd to', src_path
    if src_path:
        os.chdir(ansible_path)
    # run commands
    print '[+] Running commands'

    commands = argv['vargs']['commands']
    for command in commands:
        print '[+] Running:', command
        print os.system(command)

except Exception, e:
    print e