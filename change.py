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

    flist = os.listdir(trace_data_dir)
    print(flist)
    for fname in flist:
        # print run_num
        pnt_big = np.loadtxt(trace_data_dir + fname, delimiter=',')

        data_changed=[]
        for line in pnt_big:
           current=[]
        #转化为24小时制

           time1=datetime.datetime.utcfromtimestamp(line[0])+timedelta(hours=8)

           current.append(time1.hour*3600+time1.minute*60+time1.second)
        #经度调整
           current.append(int(line[1]-420000))
           current.append(int(line[2]-4391000))
           data_changed.append(current)

        np.savetxt(savedir_tmp + fname, data_changed, fmt='%.10f', delimiter=',')

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
    dirname = data_root + 'data_taxi/'
    savedir = data_root + 'changed_data/'

    if os.path.exists(savedir) == False:
        os.makedirs(savedir)

    pool = Pool(4)
    #for i in range(start_day, start_day + 31):
    pool.apply_async(change_data, (dirname, savedir, logfile, str(20150701)))
    pool.close()
    pool.join()

    print 'end of main()'

# -------------



