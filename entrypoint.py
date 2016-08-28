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
    with open("/root/.ssh/id_rsa", "w") as privateKeyFile:
        os.chmod("/root/.ssh/id_rsa", 0600)
        privateKeyFile.write(privateKey)

    os.system("ssh-keygen -f ~/.ssh/id_rsa -y > ~/.ssh/id_rsa.pub")
    os.system("eval \"$(ssh-agent -s)\"")
    os.system("ssh-add ~/.ssh/id_rsa")

    # cd to path
    src_path = argv['workspace']['path']
    # print '[+] cd to', src_path
    if src_path:
        os.chdir(src_path + "/.ansible")
    # run commands
    print '[+] Running commands'

    commands = argv['vargs']['commands']
    for command in commands:
        print '[+] Running:', command
        print os.system(command)

except Exception, e:
    print e