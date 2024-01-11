## Digital Heritage app.

### Steps to run ORBSLAM2 with app.
1. first connect jetson with same mobile's hotspot in which you want to run the app.
2. Now find the ip asigned to jetson... go to "manage devices" in your mobile hotspot and see jetson's ip. let's say it's ip is "IP". (You can do this in IIT_WIFI also if you don't want to run the app in mobile and can run in the jetson's browser itself.in that case you can use ip everywhere as 127.0.0.1 also).
3. Now update the ip in line-no. 176 in  `ORB_SLAM2/src/Viewer.cc`, (they have made changes in this file only in ORBSLAM2, they are just sending the current x,y,z,yaw to django server always, they have just added curl lines (from line no. 171 to 178)).
4. then compile ORBSLAM2 again using `./build.sh` command. (ORB_SLAM2/build.sh is the file.)
5. now go to dheritage folder in the app code. update the ip in `dheritage/dheritage/settings.py` and `dheritage/geoloc/static/script.js`. I have made a variable ip there just update that, that variable is used 3 times. 
6. Now go to dheritage home directory and run the app using `python manage.py runserver IP:8080`. No open this link in your mobile or in jetson itself. `https://IP:8080`. you'll see the app running.
7. In `dheritage/db.sqlite3`, this is the database having all marked locations, you can access it using `https://IP:8080/admin` the username pwd is `admin` and `aks123`, this pwd is wrong. ask from aakash what was it(Arka don't know that).
8. In this database you can manually change the location coordinates, add, delete locations, etc.
---
**Problem 1:**
Bug to resolve in app: while entering a location's name and pressing "mark location" button, the location is not getting added, and the app is toggled to off mode. (actually the error was happening(printing) in the orbslam terminal).  
**Problem 2:**
- App with map code was deleted due to jetson got format. and map was not updated in github code. 
- and in the new app code also, they didn't get time to complete the map part of the app, just made the frontend(html) for map, but not the js code,etc. So later from frontend also they removed the map part. So that has to be done.




### DROID-SLAM in jetson:

#### Installation: 
- In setup.py just add the compiler flags for `_87`. (or whatever is the gencode of jetson, google that).
- And to increase fps, Arka said they changed the hyperparameters in demo.py (but he was not not sure, and in negroni when we checked no changes were made there).
