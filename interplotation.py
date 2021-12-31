#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from multiprocessing import Pool
import time
import numpy as np
from datetime import timedelta
import datetime
def inter_function(time1,time2,po1,po2,inter_time):
    if (time2-time1)%inter_time==0:
        num = ((time2 - time1) // inter_time)-1
    else:
        num = ((time2 - time1) // inter_time)
    x_speed=(po2[0]-po1[0])*1.0/(time2-time1)
    y_speed=(po2[1]-po1[1])*1.0/(time2-time1)
    inter_po=[]
    #print(num,x_speed,y_speed)
    for i in range(1,int(num)+1):
        incretime=inter_time*i
        time_interpo=time1+incretime
        po_x=po1[0]+x_speed*incretime
        po_y=po1[1]+y_speed*incretime
        #print(time_interpo,po_x,po_y)
        inter_po.append([time_interpo,int(po_x),int(po_y)])
    return inter_po
def interplotation_data(dirname,
                      savedir,
                      logfile,
                      day,
                      ):



    start_time = time.clock()
    print 'begin of day ' + day

    trace_data_dir = dirname + day + "/"
    savedir_tmp = savedir + day + '/'
    if os.path.exists(savedir_tmp) == False:
        os.makedirs(savedir_tmp)

    flist = os.listdir(trace_data_dir)
    print(flist)
    num=1
    print(num)
    for fname in flist:
        # print run_num
        pnt_big = np.loadtxt(trace_data_dir + fname, delimiter=',')
        print(num)
        num+=1
        data_inter=[]
        first_node=pnt_big[0]
        data_inter.append(first_node)
        for node in pnt_big[1:]:
           #两秒插一个
           inter_po=inter_function(first_node[0],node[0],(first_node[1],first_node[2]),(node[1],node[2]),1)
           #print(inter_po)
           for i in inter_po:
               data_inter.append(i)
           data_inter.append(node)
           first_node=node

        np.savetxt(savedir_tmp + fname, data_inter, fmt='%d', delimiter=',')

    print 'end of day ' + day
    end_time = time.clock()
    f1 = open(logfile, 'a')
    f1.write('\nThe step is 6, day is ' + day + ', The code ran for ' + str(end_time - start_time) + ' seconds' +
             '\nIt starts at ' + time.ctime(start_time) +
             '\nIt ends at ' + time.ctime(end_time))
    f1.close()


if __name__ == "__main__":

    # 配置以下2项
    data_root = 'G:/view_data/'
    start_day = 20140701

    logfile = data_root + 'logfile.txt'
    dirname = data_root + 'changed_data/'
    savedir = data_root + 'interplotation_data/'

    if os.path.exists(savedir) == False:
        os.makedirs(savedir)

    pool = Pool(4)
    #for i in range(start_day, start_day + 31):
    pool.apply_async(interplotation_data, (dirname, savedir, logfile, str(20150701)))
    pool.close()
    pool.join()

    print 'end of main()'

# -------------



