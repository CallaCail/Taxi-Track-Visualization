#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from multiprocessing import Pool
import time
import numpy as np
from datetime import timedelta
import datetime
def change_data(dirname,
                      savedir,
                      logfile,
                      day,
                      ):
    """
    与dt0.remove_jump_point相对应，没有去处时间间隔比较大的点
    """


    start_time = time.clock()
    print 'begin of day ' + day

    trace_data_dir = dirname + day + "/"
    savedir_tmp = savedir + day + '/'
    if os.path.exists(savedir_tmp) == False:
        os.makedirs(savedir_tmp)
    #print(os.path.exists(savedir_tmp))
    flist = os.listdir(trace_data_dir)
    print(flist)
    hour_list = [[] for i in range(24)]
    index=0
    for fname in flist:
        pnt_big = np.loadtxt(trace_data_dir + fname, delimiter=',')
        print(index)
        index=index+1
        for line in pnt_big:
            hour_list[int(line[0])/3600].append(line)

    for hour in range(len(hour_list)):
       name=str(hour)+'.txt'
       np.savetxt(savedir_tmp + name, hour_list[hour], fmt='%d', delimiter=',')

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
    dirname = data_root + 'interplotation_data/'
    savedir = data_root + 'hour_split/'

    if os.path.exists(savedir) == False:
        os.makedirs(savedir)

    pool = Pool(4)
    #for i in range(start_day, start_day + 31):
    pool.apply_async(change_data, (dirname, savedir, logfile, str(20150701)))
    pool.close()
    pool.join()

    print 'end of main()'

# -------------



