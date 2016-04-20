import random
import decimal
PRO_SPEED = 2
MASTER_ERR = 0.000005 # error of master node
SLAVE_ERR  = 0.000005 # error of slave node
PRO_ERR = 0.000002 # error of propagation process 
SYNC_CYCLE = 1 # sync cycle, master fre as well 0.2 above
SLAVE_RANGE = 0.000005 # slave fre range
SLAVE_FRE = 1 + random.uniform(-1 * SLAVE_RANGE,1 * SLAVE_RANGE)
TOTAL_CYCLE = 10 # to see how long the sync process undergo
decimal.getcontext().prec = 40

def master(masterClock):
	global MASTER_ERR,SYNC_CYCLE
	err = random.uniform(-1,1) * MASTER_ERR
	curClock = masterClock[0] + SYNC_CYCLE *(1 + err)
	masterClock[2] = decimal.Decimal(curClock) - decimal.Decimal(masterClock[1])
	masterClock[1] = curClock
	return masterClock

def slave(slaveClock,masterClock):
	global SLAVE_ERR,SLAVE_FRE, SYNC_CYCLE
	err = random.uniform(-1,1) * SLAVE_ERR
	slaveClock[1] = decimal.Decimal(slaveClock[1]) + decimal.Decimal(masterClock[2]) * decimal.Decimal(decimal.Decimal(SLAVE_FRE) / decimal.Decimal(SYNC_CYCLE)) * decimal.Decimal( 1 + err )
	return slaveClock

def sync(masterClock,slaveClock):
	global PRO_ERR, SYNC_CYCLE, SLAVE_FRE, SLAVE_ERR, MASTER_ERR
	#some random parameter in each sync process
	propagation_time = 0.0001 #the estimated propagation time
	real_propagation_time =  propagation_time * (1 + random.uniform(-1 * PRO_ERR,1 * PRO_ERR))# to caculate by myself
	delta_t = 0.00001 # time in slave node before the sync process
	real_t = decimal.Decimal(delta_t) * decimal.Decimal(decimal.Decimal(SYNC_CYCLE) / decimal.Decimal(SLAVE_FRE) ) * (1 + decimal.Decimal(random.uniform(-1*SLAVE_ERR, 1* SLAVE_ERR)) )
	#end of random parameter
	

	temp_err = 0
	slave_fre = SLAVE_FRE
	slaveClock[1] = decimal.Decimal(decimal.Decimal(slaveClock[1]) + decimal.Decimal(real_propagation_time) )* decimal.Decimal(decimal.Decimal(SLAVE_FRE) + decimal.Decimal(delta_t) )
	if decimal.Decimal(slaveClock[1]) - decimal.Decimal(slaveClock[0]) != 0 and slaveClock[0] != 0:#?
		slave_fre = abs(decimal.Decimal(slave_fre) * decimal.Decimal(decimal.Decimal(masterClock[1]) - decimal.Decimal(masterClock[0]) ) / decimal.Decimal(decimal.Decimal(slaveClock[1]) - decimal.Decimal(slaveClock[0]) ) ) 
		#print "sync",slave_fre,masterClock[1]-masterClock[0],slaveClock[1]-slaveClock[0]

	temp_slave = decimal.Decimal(slaveClock[1])#to caculate the err between the master and slave
	slaveClock[1] = masterClock[1] + propagation_time + delta_t
	slaveClock[0] = slaveClock[1]
	masterClock[0] = masterClock[1]
	masterClock[1] = decimal.Decimal(masterClock[1]) + decimal.Decimal(real_propagation_time) + decimal.Decimal(real_t) * (1 + decimal.Decimal(random.uniform(-1*MASTER_ERR,1*MASTER_ERR)))
	temp_err = abs (decimal.Decimal(masterClock[1]) - decimal.Decimal(temp_slave) )
	return slave_fre,slaveClock,masterClock,temp_err

def main():
	global SLAVE_FRE,TOTAL_CYCLE
	max_err = 0
	temp_err = 0
	masterClock = [0,0,0]
	#m[0] is the last sync process start time, 
	#m[1] is the last time
	#m[2] is the passing time
	slaveClock = [0,0]
	for x in xrange(1,TOTAL_CYCLE):
		masterClock = master(masterClock)
		slaveClock = slave(slaveClock,masterClock)
		print "master:",masterClock[1],"slave",slaveClock[1],"slave_fre",SLAVE_FRE
		#the sync process start
		SLAVE_FRE,slaveClock,masterClock,temp_err = sync(masterClock,slaveClock)
		if temp_err > max_err:
			max_err = temp_err
		print "master:",masterClock[1],"slave",slaveClock[1],"slave_fre",SLAVE_FRE,"err is",temp_err
		#the sync process start
	print "max_err of adjust fre is",max_err,"max_err of only adjust offset is"
	pass

if __name__ == '__main__':
	main()