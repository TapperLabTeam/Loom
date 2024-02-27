def freeze_time_calc(time, velocity, mean_base_vel):
    #Calculate freeze time from timestamps and velocity data based on...
    #mean baseline velocity

    #Input Agruments:
    #time = list of timestamps
    #velocity = list of velocity values
    #mean_base_vel = float of baseline velocity for trial

    sum_freeze_time = []
    start_stop = []
    temp_freeze_time = []
    freeze_start = 0
    for point_num, point in enumerate(velocity):
        if point < mean_base_vel and freeze_start == 0:
            start_stop.append(abs(time[point_num]))
            freeze_start = 1
        if point > mean_base_vel and freeze_start == 1:
            start_stop.append(abs(time[point_num]))
            temp_freeze_time.append(max(start_stop) - min(start_stop))
            start_stop = []
            freeze_start = 0
        if freeze_start == 1 and point_num == len(velocity) - 1:
            start_stop.append(abs(time[point_num]))
            temp_freeze_time.append(max(start_stop) - min(start_stop))
            start_stop = []
            freeze_start = 0
    sum_freeze_time = sum(temp_freeze_time)
    
    return sum_freeze_time
