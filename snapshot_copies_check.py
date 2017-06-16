#!/usr/bin/env python

from prettytable import PrettyTable
from subprocess import PIPE, Popen
x = PrettyTable(["Source-Path","Destination-Path","Snapshots","Is-Healthy"])

def main():
    #print("{}\t{}\t{}\t{}\t{}".format(fh[0],fh[1],cluster,vserver,volume))
    #print ("ssh admin@{} vol show -vserver {} -volume {} |grep -i \"Snapshot copies in the volume\"".format(cluster,vserver,volume))
    snapcount = Popen("ssh admin@{} vol show -vserver {} -volume {} |grep -i \"Snapshot copies in the volume\"".format(cluster,vserver,volume),shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout,stderr = snapcount.communicate()
    output1 = stdout.strip().decode('utf-8')
    #print("ssh admin@{} snapmirror show {}:{} |grep -i \"Healthy:\"".format(cluster,vserver,volume))
    smhealth = Popen("ssh admin@{} snapmirror show {}:{} |grep -i \"Healthy:\"".format(cluster,vserver,volume),shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout,stderr = smhealth.communicate()
    output2 = stdout.strip().decode('utf-8')
    length1 = len(fh[0])
    length2 = len(fh[1])
    if  output1 == "" or output2 == "":
        print ("\nThis Volume {} doesn't exist\n".format(volume))
    else:
        copies = output1.split(':')
        health = output2.split(':')
        mylist = []
        source = mylist.append(fh[0])
        dest = mylist.append(str(fh[1]))
        snap = mylist.append(str(copies[1]))
        ishealthy = mylist.append(str(health[1]))
        #x.add_row(mylist)
        print("{},{}:{},{},{}".format(fh[0],vserver,volume,copies[1],health[1]))

if __name__ == "__main__":
    snapreport = open('lag-snapvault-report').readlines()
    print("Source-Path,Destination-Path,Number of Snapshot-Copies,Snapmirror Healthy")
    count = 0
    for line in snapreport:
        fh = line.strip().split()
        if len(fh) >= 1:
            path = fh[1].split(':')
            vsm = path[0].split('-')
            cluster = vsm[0] +'-' +vsm[1] +'-' +vsm[2]
            vserver = path[0]
            volume = path[1]
            count = count+1
            main()
        else:
            continue
    #print("\n{}\n".format(x))
    print("\n\t\t\t\t{} Duplicate relations have been found\n".format(count))
    exit(1)
                                                                                          
