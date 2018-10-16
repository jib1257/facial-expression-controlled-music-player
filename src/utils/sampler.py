import time

def sampler(period,check_condition,base_condition):
    time.sleep(period)
    if check_condition == base_condition:
        return(True)
    else:
        return(False)