#!/usr/bin/env python
#This script is useful for getting source volume status,state,snapshot-policy,snap-reserve,snapshot-space-used and also investigate the destination relations errors and reasons why relations has failed to update
#contact Rakesh Muppala for any questions or concerns

import argparse
from subprocess import PIPE, Popen
from prettytable import PrettyTable

#Getting source volume details-snapshot-policy,snap-reserve,volume=name
def source(spath):
    mysrc = []
    for line in spath:
        if line.strip().split():
            mylist = []
            scluster,svserver,svolume = lineData(line,0)
            srcpath = svserver+ ':'+ svolume
            #print("ssh admin@{} vol show -vserver {} -volume {} |egrep -i \"Snapshot Policy|Snapshot Reserve Used\"".format(scluster,svserver,svolume))
            srcdetails = sendRequest("ssh admin@{} vol show -vserver {} -volume {} |egrep -i \"Volume State|Snapshot Policy|Snapshot Reserve Used\"".format(scluster,svserver,svolume))
            if srcdetails:
                sourcepath = mylist.append(srcpath)
                volstate = mylist.append(srcdetails[0].strip())
                snapreserve = mylist.append(srcdetails[1].strip())
                snappolicy = mylist.append(srcdetails[2].strip())
                comments = mylist.append("-")
                x = '|'.join(mylist)
                mysrc.append(x)
                srcpretty.add_row(mylist)
            else:
                sourcepath = mylist.append(srcpath)
                volstate = mylist.append("N/A")
                snapreserve = mylist.append("N/A")
                snappolicy = mylist.append("N/A")
                comments = mylist.append("doesn't exist")
                y = '|'.join(mylist)
                mysrc.append(y)
                srcpretty.add_row(mylist)
        #print("Volume|Volume State|Snapshot-Reserve|Snapshot-policy|comments")
       # for line in  mysrc:
        #    print line

def destination(dpath):
    mydest = []
    for item in dpath:
        if item.strip().split():
            mydlist = []
            dcluster,dvserver,dvolume = lineData(item,1)
            destpath = dvserver+ ':'+ dvolume
            #print("ssh admin@{} snapmirror show {}:{}  |egrep -i \"Healthy|Unhealthy Reason|Last Transfer Error|Lag Time\"".format(dcluster,dvserver,dvolume))
            destdetails = sendRequest("ssh admin@{} snapmirror show {}:{}  |egrep -i \"Healthy|Relationship Status|Unhealthy Reason|Last Transfer Error|Lag Time\"".format(dcluster,dvserver,dvolume))
            if destdetails:
                destination = mydlist.append(destpath)
                halthy = mydlist.append(destdetails[1].strip())
                status = mydlist.append(destdetails[0].strip())
                transfer = mydlist.append(destdetails[3].strip())
                reason = mydlist.append(destdetails[2].strip())
                lagtime = mydlist.append(destdetails[4].strip())
                y = '|'.join(mydlist)
                mydest.append(y)
                destpretty.add_row(mydlist)
    print("Destination-Path|Is-healthy|Status|Failure-Reason|Last Transfer Error|Lag-time")
    for line in  mydest:
        print line

def sendRequest(cmd):
    clusterconnect = Popen(cmd,shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = clusterconnect.communicate()
    output = stdout.strip().decode('utf-8').splitlines()
    return output

def lineData(l,element):
    ls = l.strip().split()
    sou = ls[element].strip().split(':')
    vs = sou[0]
    vol = sou[1]
    rs = sou[0].split('-')
    if element == 0:
        sc = rs[0] + '-' + rs[1]
        return sc,vs,vol
    else:
        dc = rs[0] + '-' + rs[1] + '-' + rs[2]
        return dc,vs,vol

if __name__ == "__main__":
    srcpretty = PrettyTable(["Source-Path","State","Snapshot-Reserve","Snapshot-policy","comments"])
        destpretty = PrettyTable(["Destination-Path","Is-healthy","Status","Failure-Reason","Last Transfer Error","Lag-time"])
    parser = argparse.ArgumentParser(description="\nThis script is useful for getting source volume status,snapshot-policy,snap-reserve,snapsh-space-used and also investigate the destination relations errors and reasons why relationshas failed to update\n")
    parser.add_argument("-filename","--file",dest="fname",help="Please provide file name with source and destination paths separated by space",required=True)
    myargs = parser.parse_args()
    fh = open(myargs.fname)
    lag = fh.readlines()
    source(lag)
    print("\nSource Volume details:\n{}\n".format(len("Source Volume details:")*'-'))
    print("\n{}\n".format(srcpretty))
    print("\nDestination Volume details:\n{}\n".format(len("Destination Volume details:")*'-'))
    print("The output will be generated in csv format with filed separator'|'(PIPE), please copy it to MSExcel and use 'Delimited' option to separate each field '|' \n")
    destination(lag)
    #print("\n{}\n".format(destpretty))
    fh.close()
    print("\n")
                                                        
                                                                                                            
