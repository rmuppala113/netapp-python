#!/usr/bin/env python
#This script is to pull the exports/netgroups for 7mode filers
#Contact Rakesh Muppala

import argparse
import re
from subprocess import PIPE, Popen

parser = argparse.ArgumentParser(description="\nThis script is to pull the exports/netgroups for 7mode  VIF volumes\n")
parser.add_argument("-file", "--file", dest="fname", help="Please provide file name with 7mode nfs path details", required=True)

filer = parser.parse_args()

def main():

    for line in nfspath:
        path = line.strip().split(":")
        vfiler = path[0]
        volume = path[1].split("/")[2]
        lenpath = len(path[0]) + len(path[1]) + 3
        #print("cat /autonetapp/{}/etc/exports |grep {}".format(vfiler,volume))
        exports = Popen("cat /autonetapp/{}/etc/exports |grep {}".format(vfiler,volume),shell=True, stdout=PIPE, stderr=PIPE)
        stdout,stderr = exports.communicate()
        output1 = stdout.strip().decode('utf-8').split('\n')
        for line in output1:
            rw = line.strip().split(',')
            volume = rw[0].split()[0].split('/')[2]
            access = rw[1]
            r = access.split('=')
            myexports = []
            if len(r) > 1:
                y = r[1].split(':')
                print("\n{}:{}:\n{}".format(path[0],path[1],(lenpath*'+')))

                #print y
                for i in y:
                    if '@' not in i:
                        myexports.append(i)
                        print("{}".format(i))
                    else:
                        net = i.strip()[1:]
                        #print("cat /autonetapp/{}/etc/netgroup |grep {}".format(vfiler,net))
                        netgroup = Popen("cat /autonetapp/{}/etc/netgroup |grep {}".format(vfiler,net),shell=True, stdout=PIPE, stderr=PIPE)
                        stdout,stderr = netgroup.communicate()
                        output2 = stdout.strip().decode('utf-8').split('\n')
                        for k in output2:
                            if net in k:
                                f = k.strip().split()[1:]
                                c = ','.join(f)
                                cr = c.replace(",,)","").replace("(","").replace(",","\n")
                                print("{}".format(cr))
            #print ','.join(myexports)


if __name__ == "__main__":
    nfspath = open(filer.fname).readlines()
    main()
    print("\n")
                                                      
