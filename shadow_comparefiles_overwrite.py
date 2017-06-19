#!/usr/bin/env python
def main():
    f1_list = []
    f2_list = []
    common = []
    same_user = []
    sendFile('shadow-rh7.rhel7',f1_list)
    sendFile('shadow-rh5.rhel5', f2_list)
    print("\nOriginal File1 has {} lines\nOriginal File2 has {} lines\n".format(len(f1_list),len(f2_list)))
    for element in f2_list:
        if not element.startswith("root:") and element not in f1_list:
            common.append(element)
    print("Number of lines that are different from RH5 and RH7 are {}:\n{}\n".format(len(common),60*'+'))
    if len(common) > 0:
        for lg in  f1_list:
            lg_user = lg.strip().split(':')[0]
            for cname in common:
                cname_user = cname.strip().split(':')[0]
                if cname_user == lg_user:
                    user_combine = cname + ','+lg
                    same_user.append(user_combine)
                    f1_list.remove(lg)
        userPrint(common)
        print("\nUsers already present in RH7 file and RH5 are {},lines from RH5 and RH7 are combined using delimiter comma in case for comparing two lines :\n{}\n".format(len(same_user),150*'+'))
        userPrint(same_user)
        print("\n")
        print("{} lines after removing common users from RH7 file \n".format(len(f1_list)))
        f1_list.extend(common)
        print("{} lines after appending new lines from RH5 file".format(len(f1_list)))
        print ("\nOverwriting RH7 file now\n")
        with open('shadow-rh7.rhel7','w') as wfile1:
            for item in f1_list:
                wfile1.write(item + '\n')
        print("Overwriting completed")
    else:
        print("Nothing found to overwrite RH7 file")
def sendFile(f,flist):
    with open(f, 'r') as file:
        fh = file.readlines()
        for fline in fh:
            line_list = fline.strip()
            flist.append(line_list)
def userPrint(ulist):
    for lc in ulist:
        print("{}".format(lc))
    return lc
    print("\n")
if __name__ ==  "__main__":
    main()

