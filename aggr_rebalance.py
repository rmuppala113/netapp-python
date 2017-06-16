#!/usr/bin/env python

import argparse
from prettytable import PrettyTable
from subprocess import PIPE,Popen
from operator import itemgetter

def main(a,p):
    volcount = []
    #print("ssh admin@{} \"aggr show -aggregate aggr1* -percent-used >85% -fields node,size,used,percent-used,volcount \"".format(a))
    aggrlist = sendCommand("ssh admin@{} \"aggr show -aggregate aggr1* -percent-used >{} -fields node,size,used,percent-used,volcount \"".format(a,p))
    if aggrlist:
        print("\n{}\n{}".format(a,len(a)*'+'))
        #print("ssh admin@{} \"aggr show -aggregate aggr1* -percent-used >85% -fields node,size,used,percent-used,volcount \"".format(a))
        for i in aggrlist:
            if i:
                x = i.split()
                aggregate = x[0]
                aggr_report.add_row(x)
                vollist = sendCommand("ssh admin@{} \"vol show -aggregate {}  -used >1TB  -fields aggregate,size,used,percent-used\"".format(a,aggregate))
                for i in vollist:
                    y = i.split()
                    m = i.splitlines()
                    volcount.append(m)
                    vol_report.add_row(y)
        aggrsort = aggr_report.get_string(sort_key=itemgetter(0),sortby="Percent-Used",reversesort=True)
        volsort =  vol_report.get_string(sortby=("percent-used"),reversesort=True)
        print("{}\n{}\n".format(aggrsort,volsort))
        #print aggr_report.get_html_string(format=True)
        #print vol_report.get_html_string(format=True)
        print("\n{} volumes are greater than 90% utilized\n".format(len(volcount)))
        aggr75(a)
    else:
        print("\n{}\n{}\nNothing Found above {} usage".format(a,len(a)*'+',p))
def aggr75(c):
    aggr_less = PrettyTable(["Aggregate","Node","Percent-Used","Size","Used","VolumeCount"])
    aggr_75 = sendCommand("ssh admin@{} \"aggr show -aggregate aggr1* -percent-used <75% -fields node,size,used,percent-used,volcount \"".format(c))
    if aggr_75:
        for i in aggr_75:
            if i:
                t = i.split()
                aggr_less.add_row(t)
        print("{}\n".format(aggr_less))
        #print aggr_less.get_html_string(format=True)

def sendCommand(cmd):
    clusterconnect = Popen(cmd,shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = clusterconnect.communicate()
    output = stdout.strip().decode('utf-8').splitlines()
    if len(output) == 3:
        return output[2:]
    elif len(output) > 3:
        return output[2:-1]

if __name__ == "__main__":
    aggr_report = PrettyTable(["Aggregate","Node","Percent-Used","Size","Used","VolumeCount"])
    vol_report = PrettyTable(["vserver","volume","aggregate","size","used","percent-used"])
    parser = argparse.ArgumentParser()
    parser.add_argument('-clusters',nargs='*',help="Enter cDot cluster names separated by space",required=True)
    parser.add_argument('-percent','--PERCENT',help="Enter aggr",required=True)
    filer = parser.parse_args()
    percent = (filer.PERCENT)
    for cluster in filer.clusters:
        main(cluster,percent)
    print "\n"
                                                                                                                      
