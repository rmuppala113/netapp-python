#!/usr/bin/env python
#This script will identify the relations provided in dest-cleanup-list file and delete the snapvault relations and rename the volumes
#Contact rmuppala@cisco.com for any qyestions
from dateutil.relativedelta import relativedelta
from datetime import  date
import argparse
from subprocess import PIPE, Popen

parser = argparse.ArgumentParser(description="\n This script will identify the relations provided in dest-cleanup-list file and delete the snapvault relations and rename the volumes to dlete after 90days from current date\n")
parser.add_argument("-filename","--file",dest="fname",help="Please provide file name with destination details",required=True)

myargs = parser.parse_args()
#Delete snapvault relations based on lag-report if source volumes or base snapshpts doesn't exist
def smcleanup():
    for line in destination_path:
        dest_split = line.strip().split(':')
        vserver_split = dest_split[0].split('-')
        cluster = vserver_split[0] +'-' +vserver_split[1] +'-' +vserver_split[2]
        vserver = dest_split[0]
        volume = dest_split[1]
        dest = line.strip()
        #print("Cluster is:{}\nVserver is:{}\nVolume is:{}\nDestination Path is {}\n".format(cluster,vserver,volume,dest))
        #print ("ssh admin@{} snapmirror delete {}".format(cluster,dest))
        smdelete = Popen("ssh admin@{} snapmirror delete {}".format(cluster,dest),shell=True, stdout=PIPE, stderr=PIPE)
        stdout,stderr = smdelete.communicate()
        output = stdout.strip().decode('utf-8')
        if 'not found' in output:
           print ("Relationship with {} doesn't exist\n".format(dest))
        else:
           print output
#Renaming volumes based on the ret ention period 90days, for example if there 30 snapshots on cleanup volume then rename the volume with _60days from now.
def volrename():
    currentdate = date.today()
    dateafter90days = currentdate+ relativedelta(days=90)
    a = currentdate.strftime('%d,%b,%Y')
    x = dateafter90days.strftime('%d,%b,%Y')
    #old = a.split(',')
    newname = x.split(',')

    #oldj = '_'.join(old)
    date90append = '_'.join(newname)
    for line in destination_path:
         dest_split = line.strip().split(':')
         vserver_split = dest_split[0].split('-')
         cluster = vserver_split[0] +'-' +vserver_split[1] +'-' +vserver_split[2]
         vserver = dest_split[0]
         volume = dest_split[1]
         dest = line.strip()
         #print("Cluster is:{}\nVserver is:{}\nVolume is:{}\nDestination Path is {}\n".format(cluster,vserver,volume,dest))
         #print ("ssh admin@{} vol rename -vserver {} -volume {} -newname {}_{}".format(cluster,vserver,volume,volume,date90append))
         rename = Popen("ssh admin@{} vol rename -vserver {} -volume {} -newname {}_{}".format(cluster,vserver,volume,volume,date90append),shell=True, stdout=PIPE, stderr=PIPE)
         stdout,stderr = rename.communicate()
         output = stdout.strip().decode('utf-8')
         if 'not found' in output:
             print ("Volume {} doesn't exist\n".format(volume))
         else:
             print output
             print("Volume {} has been succesfully renamed to {}_{}\n".format(volume,volume,date90append))
if __name__ == "__main__":
    destination_path = open(myargs.fname).readlines()

    print("\n")
    smcleanup()
    print("\n")
    volrename()
    print("\n")
    exit(1)
                                                                        
