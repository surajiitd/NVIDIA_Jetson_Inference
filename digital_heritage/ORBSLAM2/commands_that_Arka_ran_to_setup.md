These are the commands that I extracted from history of terminal which Arka ran to setup orbslam2 again and integrate with app.
```
 1366  vim ~/.bashrc
 1367  git clone https://github.com/luxonis/depthai-python.git
 1368  cd depthai-python/examples
 1369  python3 install_requirements.py
 1370  ./build.sh
 1371  sudo apt update && sudo apt upgrade
 1372  cd ../depthai-core/
 1373  ls
 1374  cmake --build build
 1375  cd ..
 1376  cd ORB_SLAM2/
 1377  ls
 1378  ./build.sh
 1379  cd ..
 1380  git clone https://github.com/luxonis/depthai-core-example.git
 1381  cd depthai-core-example/
 1382  git submodule update --init --recursive
 1383  mkdir -p build and cd build
 1384  ls
 1385  ls cd
 1386  rm cd
 1387  rm -r cd
 1388  ls
 1389  ls build/
 1390  cd build
 1391  cmake ..
 1392  cd --build . --parallel
 1393  cmake --build . --parallel
 1394  ls
 1395  ls ..
 1396  ./myapp
 1397  cd ..
 1398  cd ORB_SLAM2/
 1399  ./build.sh
 1400  cmake -B build
 1401  ./build.sh
 1402  ls /usr |  grep -r "texthere"
 1403  ls /usr |  grep -r "depthai"
 1404  ls /usr
 1405  ls /usr/lib
 1406  ls /usr/local/
 1407  ls /usr/local/include/
 1408  ls /usr/local/lib/
 1409  ls /usr/local/bin/
 1410  cd ..
 1411  sudo wget -qO- https://docs.luxonis.com/install_depthai.sh | bash
 1412  sudo apt install python3-pyqt5
 1413  sudo wget -qO- https://docs.luxonis.com/install_depthai.sh | bash
 1414  sudo apt-get install python3-pyqt5
 1415  sudo apt update
 1416  sudo telnet google.com 80
 1417  sudo apt-get install python3-pyqt5
 1418  pip install python3-pyqt5
 1419  sudo apt install python3-pyqt5
 1420  sudo dpkg --configure -a
 1421  sudo apt install --fix-broken
 1422  sudo apt clean
 1423  sudo apt install --fix-broken
 1424  sudo apt autoremove
 1425  sudo reboot
 1426  ls /usr
 1427  ls /usr/include/
 1428  sudo wget -qO- https://docs.luxonis.com/install_dependencies.sh | bash
 1429  cd ..
 1430  gh repo clone luxonis/depthai-core
 1431  git repo clone luxonis/depthai-core
 1432  git clone https://github.com/luxonis/depthai-core.git
 1433  cd depthai-core/
 1434  ls
 1435  cmake -S. -Bbuild
 1436  git submodule update --init --recursive
 1437  ls
 1438  sudo apt install libopencv-dev
 1439  git submodule update --init --recursive
 1440  cmake -S. -Bbuild
 1441  cmake --build build
 1442  ls
 1443  cmake --build build --target install
 1444  cd /usr
 1445  grep -r "depthai"
```

****************************************************
```
 1527  find ./ -iname install_opencv*
 1528  ls /usr/inc
 1529  ls /usr/include/
 1530  ls /usr/lib
 1531  ls /usr/
 1532  ls /usr/bin
 1533  ls /usr/local
 1534  ls /usr/local/bin
 1535  ls /usr/local/include/
 1536  ls /usr/local/include/opencv4/
 1537  ls /usr/local/include/opencv4/opencv2/
 1538  ls /usr/local/include/
 1539  ls /opt
 1540  find / -maxdepth 2 -iname opencv
 1541  sudo find / -maxdepth 2 -iname opencv
 1542  sudo find / -maxdepth 3 -iname opencv
 1543  sudo find / -maxdepth 3 -iname opencv*
 1544  sudo find / -maxdepth 3 -iname *opencv*
 1545  sudo find / -maxdepth 3 -iname *opencv
 1546  sudo find / -maxdepth 3 -iname opencv*
 1547  pkg-config --modversion opencv
 1548  ls /usr/local/lib/cmake/opencv4
 1549  sudo find / -maxdepth 4 -iname opencv*
 1550  sudo find / -maxdepth 5 -iname opencv*
 1551  sudo find / -maxdepth 5 -iname opencv
 1552  ./git
 1553  ./git-commit 
 1554  ifconfig
 1555  cmake -S. -Bbuild -D'BUILD_SHARED_LIBS=ON'
 1556  cmake --build build
 1557  cmake -S. -Bbuild
 1558  cmake --build build
 1559  ./build.sh
 1560  ./myapp
 1561  git submoduke update --init --recursive
 1562  git submodule update --init --recursive
 1563  cmake -S. -Bbuild
 1564  cmake --build build
 1565  cd ..
 1566  sudo wget -qO- https://docs.luxonis.com/install_dependencies.sh
 1567  sudo wget https://docs.luxonis.com/install_dependencies.sh
 1568  bash install_dependencies.sh 
 1569  sudo wget -qO- https://docs.luxonis.com/install_dependencies.sh | bash
 1570  code /etc/apt/sources.list
 1571  code /etc/apt/sources.list.d
 1572  sudo do-release-upgrade
 1573  sudo apt-get update
 1574  uname -m
 1575  code /etc/apt/sources.list
 1576  cd depthai-core/
 1577  ls
 1578  rm -r ~/.hunter
 1579  rm -rf build
 1580  ls
 1581  cmake -H. -Bbuild -D BUILD_SHARED_LIBS=ON -D CMAKE_CXX_FLAGS=-fPIC
 1582  cmake -Bbuild -D BUILD_SHARED_LIBS=ON -D CMAKE_CXX_FLAGS=-fPIC
 1583  cd ..
 1584  wget https://curl.se/download/curl-7.77.0.tar.gz
 1585  ./configure
 1586  make
 1587  sudo make installls
 1588  ls
 1589  cd curl-7.77.0/
 1590  ./configure
 1591  make
 1592  ./configure --with-openssl
 1593  make
 1594  sudo make install
 1595  cmake -H. -Bbuild -D BUILD_SHARED_LIBS=ON -D CMAKE_CXX_FLAGS=-fPIC
 1596  cd ..
 1597  ls
 1598  cd depthai-core/
 1599  ls
 1600  cmake -H. -Bbuild -D BUILD_SHARED_LIBS=ON -D CMAKE_CXX_FLAGS=-fPIC
 1601  cmake --build build --parallel 8
 1602  ls /usr
 1603  find / -maxdepth 4 -iname depthai
 1604  sudo find / -maxdepth 4 -iname depthai
 1605  sudo find / -maxdepth 4 -iname depth-ai
 1606  sudo find / -maxdepth 4 -iname depthai*
 1607  sudo find / -maxdepth 4 -name depthai*
 1608  sudo find / -maxdepth 4 -name *depthai*
 1609  sudo find / -maxdepth 4 -name *depthai
 1610  sudo find / -maxdepth 4 -name depthai
 1611  sudo find / -maxdepth 4 -name depthai*
 1612  sudo find / -maxdepth 4 -name depth*
 1613  sudo find / -maxdepth 6 -name depth*
 1614  sudo find / -maxdepth 8 -name depthai*
 1615  make install
 1616  grep -inr "install" ./
 1617  grep -inr "installpath" ./
 1618  grep -inr "install_path" ./
 1619  ls /usr
 1620  ls /usr/include/
 1621  ls /usr/local
 1622  ls /usr/local/include/
 1623  sudo cp ./* /usr/local/
 1624  sudo cp -r ./* /usr/local/
 1625  ls /usr/local
 1626  ls /usr/local/include
 1627  ls /usr/local/lib
 1628  git clone https://github.com/luxonis/depthai-core-example.git
 1629  git submodule update --init --recursive
 1630  cd depthai-core-example/
 1631  ls
 1632  git submodule update --init --recursive
 1633  mkdir -p build && cd build
 1634  cmake ..
 1635  cmake --build . --parallel
 1636  cd ..
 1637  cd depthai-core
 1638  ls
 1639  cmake -S. -Bbuild -D'BUILD_SHARED_LIBS=ON'
 1640  cmake --build build
 1641  scp -r share spatni@10.194.113.172:~/
 1642  cd ..
 1643  cd ORB_SLAM2/
 1644  ./build.sh
 1645  cd ..
 1646  gedit issues
 1647  cd ORB_SLAM2/
 1648  ./build.sh
 1649  sudo apt-get install libnop-dev
 1650  sudo apt-get update
 1651  sudo apt-get install libnop-dev
 1652  cd ..
 1653  git clone https://salsa.debian.org/deeplearning-team/libnop.git
 1654  ls
 1655  cd libnop/
 1656  ls
 1657  make
 1658  make install
 1659  cd build/
 1660  ls
 1661  host-executable.mk
 1662  make host-executable.mk
 1663  make
 1664  cd ../..
 1665  git clone https://github.com/google/libnop.git
 1666  cd libnop/
 1667  ls
 1668  make
 1669  make all
 1670  cd ..
 1671  cd ORB_SLAM2/
 1672  ls
 1673  ./build.sh
 1674  sudo apt-get install nlohmann-json-dev
 1675  sudo apt-get install nlohmann-json3-dev
 1676  ./build.sh
 1677  sudo apt install libopencv-dev
 1678  sudo apt autoremove
 1679  sudo apt install libopencv-dev
 1680  ./build.sh
 1681  sudo cp -r ./* /usr/local/
 1682  ls /usr/local
 1683  sudo cp -r ./* /usr/local/include/
 1684  ls /usr/local/include
```

********************************************
```
 1769  ls /usr/local/
 1770  cp -r ./include /usr/local
 1771  sudo cp -r ./include /usr/local
 1772  ls
 1773  ls /usr/local/
 1774  ls /usr/local/include/
 1775  sudo cp -r ./lib /usr/local
 1776  sudo cp -r ./bin /usr/local
 1777  sudo cp -r ./licenses /usr/local
 1778  sudo cp -r ./share /usr/local
 1779  cd /usr/local/include/
 1780  ls
 1781  mkdir tl
 1782  sudo mkdir tl
 1783  cd tl
 1784  nano optional.hpp
 1785  sudo nano optional.hpp
 1786  ls /usr/bin
 1787  ls /usr/bin/cmake
 1788  cat /usr/bin/cmake
 1789  cd ..
 1790  clear
 1791  g++ -L/home/vision/slam/depthai-core/build/libdepthai-opencv.so -ldepthai test.cc -o test
 1792  g++ -L/home/vision/slam/depthai-core/build/libdepthai-opencv.so -ldepthai -lopencv test.cc -o test
 1793  g++ -L/home/vision/slam/depthai-core/build/libdepthai-opencv.so -ldepthai `pkg-config --libs opencv` test.cc -o test
 1794  ./build.sh
 1795  sudo apt-get install depthai
 1796  ls /usr/local/
 1797  ls /usr/local/include
 1798  ls /usr/local/include/depthai
 1799  cat /usr/local/include/depthai/depthai.hpp
 1800  code /usr/local/include/
 1801  sudo apt-get install xlink
 1802  sudo apt-get install Xlink
 1803  sudo apt-get install XLink
 1804  sudo apt-get install xlink-dev
 1805  ./build.sh
 1806  ./build.sh
 1807  code /usr/local/include/
 1808  sudo code /usr/local/include/
 1809  ./build.sh
 1810  ls /usr/local
 1811  ls /usr/local/lib
 1812  ./build.sh
 1813  ./myapp
 1814  lsusb
 1815  lsusb | grep 03e7
 1816  lsusb
 1817  dmesg -w
 1818  sudo dmesg -w
 1819  echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
 1820  sudo udevadm control --reload-rules && sudo udevadm trigger
 1821  ./myapp
 1822  code .
 1823  ./test
 1824  ./build.sh
 1825  cd ..
 1826  cd depthai-core-example/
 1827  ls
 1828  cd build/
 1829  ls
 1830  ./myapp
 1831  cd ..
 1832  cd ORB_SLAM2/
 1833  ./build.sh
 1834  lsusb
 1835  whereis cuda
 1836  cd /usr/local/cuda
 1837  cd ..
 1838  ls
```
********************************************** 
```
 1870  ./build.sh
 1871  ifconfig
 1872  ./build.sh
 1873  pip install django
 1874  pip install djangorestframework
 1875  python manage.py runserver 172.10.20.15:8080
 1876  python --version
 1877  python3.6 -m pip install django
 1878  python3.6 -m pip install djangorestframework
 1879  python manage.py runserver 172.10.20.15:8080
 1880  ifconfig
 1881  python manage.py runserver 172.10.20.4:8080
 1882  python manage.py runserver 172.20.10.15:8080
 1883  python manage.py runserver 172.20.10.4:8080
```
