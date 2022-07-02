import time
import threading
import log
import centerspack.auth_center
import centerspack.table_center
import manager

"""Launch Poker Server with specified range of ports and IP-address of a machine which runs Poker Server. Note that 
you shall not specify number of ports by passing corresponding argument. This number should be set in the main.py and 
manager.py code manually. """

# Initialize all objects
log = log.Log()
log_thread = threading.Thread(target=log.run)

auth_center = centerspack.auth_center.AuthCenter()
auth_center_thread = threading.Thread(target=auth_center.run, name='auth_center_thread')

table_center = centerspack.table_center.TableCenter()
table_center_thread = threading.Thread(target=table_center.run, name='table_center_thread')

n = 4  # Managers' amount
ports = [5555 + i for i in range(n)]  # Range of allocated ports
managers = []
for i, port in enumerate(ports):
    mng = manager.Manager(log, auth_center, table_center, port)
    mng_thread = threading.Thread(target=mng.run, name=f'manager_thread0{i}')
    managers.append((mng, mng_thread))

# Run all threads
log_thread.start()
auth_center_thread.start()
table_center_thread.start()
for i in range(n):
    managers[i][1].start()

# Mainloop
while input() != 'exit':
    time.sleep(0.05)

# Stop all threads
for i in range(n):
    managers[i][0].mail.put(('DESTROY',))
    managers[i][1].join()

table_center.mail.put(('DESTROY',))
table_center_thread.join()

auth_center.mail.put(('DESTROY',))
auth_center_thread.join()

log.mail.put(('DESTROY',))
log_thread.join()
