import os

try:
    for _ in range(10000):
        # os.system('curl -H \'Content-Type: applications/json\' -d \'{ x:0.345, y:0.234, yaw:0.7987 }\' -X POST http://127.0.0.1:8080/updatecurrent')
        os.system('curl -d \'x=0.23423&y=0.23423&yaw=0.34534\' http://127.0.0.1:8080/updatecurrent/')
        print('sending request ...')
except KeyboardInterrupt:
    print('Exit ...')
