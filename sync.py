import random
PRO_SPEED = 200000000
MASTER_ERR = 0.000005 # error of master node
SLAVE_ERR  = 0.000005 # error of slave node
PRO_ERR = 0.01 # error of propagation process 
SYNC_CYCLE = 0.01 # sync cycle, master fre as well 0.2 above
SLAVE_RANGE = 0.000005 # slave fre range
SLAVE_FRE = 1 + random.uniform(-1 * SLAVE_RANGE,1 * SLAVE_RANGE)
TOTAL_CYCLE = 50000 # to see how long the sync process undergo
T_START = 0.8 * TOTAL_CYCLE * SYNC_CYCLE

def master(masterClock):
	global MASTER_ERR,SYNC_CYCLE
	err = random.uniform(-1,1) * MASTER_ERR
	curClock = masterClock[0] + SYNC_CYCLE *(1 + err)
	masterClock[2] = curClock - masterClock[1]
	masterClock[1] = curClock
	return masterClock

def slave(slaveClock,slaveClock_p,masterClock):
	global SLAVE_ERR,SLAVE_FRE, SYNC_CYCLE
	err = random.uniform(-1,1) * SLAVE_ERR
	slaveClock[1] = slaveClock[1] + (masterClock[2]) * (SLAVE_FRE ) * ( 1 + err )
	slaveClock_p[1] = slaveClock_p[1] + + (masterClock[2]) * (SLAVE_FRE ) * ( 1 + err )
	return slaveClock,slaveClock_p

def sync(masterClock,slaveClock,slaveClock_p):
	global PRO_ERR, SYNC_CYCLE, PRO_SPEED, SLAVE_FRE, SLAVE_ERR, MASTER_ERR
	#some random parameter in each sync process
	propagation_time = 5.0 / PRO_SPEED #the estimated propagation time
	real_propagation_time =  propagation_time * (1 + random.uniform(-1 * PRO_ERR,1 * PRO_ERR))# to caculate by myself
	delta_t = 0.0000001 # time in slave node before the sync process
	real_t = delta_t * (SYNC_CYCLE / SLAVE_FRE ) * (1 + random.uniform(-1*SLAVE_ERR, 1* SLAVE_ERR))
	#end of random parameter
	

	temp_err = 0
	temp_err_p = 0
	slave_fre = SLAVE_FRE
	slaveClock[1] = slaveClock[1] + real_propagation_time * SLAVE_FRE + delta_t
	if slaveClock[1] - slaveClock[0] != 0 and slaveClock[0] != 0:#?
		slave_fre = slave_fre * (masterClock[1] - masterClock[0]) / (slaveClock[1] - slaveClock[0]) 
		#print "sync",slave_fre,masterClock[1]-masterClock[0],slaveClock[1]-slaveClock[0]

	temp_slave = slaveClock[1]#to caculate the err between the master and slave
	temp_slave_p = slaveClock_p[1]
	#slaveClock_p[1] = slaveClock_p[1] + real_propagation_time * SLAVE_FRE + delta_t
	slaveClock_p[1] = masterClock[1] + propagation_time + delta_t
	slaveClock_p[0] = slaveClock_p[1]
	slaveClock[0] = slaveClock[1]
	masterClock[0] = masterClock[1]
	masterClock[1] = masterClock[1] + real_propagation_time + delta_t * (1 + random.uniform(-1*MASTER_ERR,1*MASTER_ERR))
	temp_err = abs (masterClock[1] - temp_slave)
	temp_err_p = abs(masterClock[1] - temp_slave_p) 
	return slave_fre,slaveClock,slaveClock_p,masterClock,temp_err,temp_err_p

def main():
	global SLAVE_FRE,TOTAL_CYCLE
	max_err = 0
	max_err_p = 0
	temp_err = 0
	temp_err_p = 0
	masterClock = [0,0,0]
	#m[0] is the last sync process start time, 
	#m[1] is the last time
	#m[2] is the passing time
	slaveClock = [0,0]
	slaveClock_p = [0,0]
	for x in xrange(1,TOTAL_CYCLE):
		masterClock = master(masterClock)
		slaveClock,slaveClock_p = slave(slaveClock,slaveClock_p,masterClock)
		#print "master:",masterClock[1],"slave",slaveClock[1],"slave_fre",SLAVE_FRE,"slave_p",slaveClock_p[1]
		#the sync process start
		SLAVE_FRE,slaveClock,slaveClock_p,masterClock,temp_err,temp_err_p = sync(masterClock,slaveClock,slaveClock_p)
		if temp_err > max_err and masterClock[1] >= T_START:
			max_err = temp_err
		if temp_err_p > max_err_p and masterClock[1] >= T_START:
			max_err_p = temp_err_p
		#print "master:",masterClock[1],"slave",slaveClock[1],"slave_fre",SLAVE_FRE,"err is",temp_err,temp_err_p
		#the sync process start
	print "max_err of adjust fre is",max_err,"max_err of only adjust offset is",max_err_p
	pass

if __name__ == '__main__':
	main()