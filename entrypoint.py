#!/usr/bin/python

import sys
import os
import json
import pexpect

TIMEOUT = 30 * 60

def exit_from(child):
    exit_code = get_exit_code(child)
    print '[!] Exit code:', exit_code
    sys.exit(exit_code)

def get_exit_code(child):
    return child.exitstatus if child.exitstatus != None else child.signalstatus

try:
    argv = sys.argv[2]
    argv = json.loads(argv)
    privateKey = argv['workspace']['keys']['private']
    print '[+] Setup injected private key'

    # cd to path
    src_path = argv['workspace']['path']

    # ansible_path
    ansible_path = src_path + "/.ansible"

    # print ("Repository's Private Key: %s") % privateKey

    with open("/root/.ssh/id_rsa", "w") as privateKeyFile:
        os.chmod("/root/.ssh/id_rsa", 0600)
        privateKeyFile.write(privateKey)

    # print '[+] cd to', src_path
    if src_path:
        os.chdir(ansible_path)
    # run commands
    print '[+] Running commands'

    commands = argv['vargs']['commands']
    for command in commands:
        try:
            child = pexpect.spawn(command)
            print '[+] Running:', command
            child.logfile = sys.stdout
            child.expect(pexpect.EOF, timeout=TIMEOUT)

            exit_code = get_exit_code(child)
            print '[+] Exit code:', get_exit_code(child)
            if exit_code != 0:
                sys.exit(exit_code)

        except pexpect.TIMEOUT:
            print '[!] Timeout after %d seconds while running command: %s' % (TIMEOUT, command)
            exit_from(child)
        except Exception, e:
            print '[!] Error:', e
            if 'child' in vars() or 'child' in globals():
                exit_from(child)
            else:
                sys.exit(1)

except Exception, e:
    print '[!] Error:', e
    sys.exit(1)
