#!/bin/bash
set -ex

download () {
	wget "https://www.python.org/ftp/python/3.7.13/Python-3.7.13.tgz"
	tar -zxvf Python-3.7.13.tgz
	cd  Python-3.7.13
}
build () {
	cd  Python-3.7.13
	sudo  mkdir -p  /home/python-3.7.13 && sudo ln -sf  /home/python-3.7.13 /usr/local/
	./configure --prefix=/home/python-3.7.13/ --with-ssl-default-suites=openssl --enable-loadable-sqlite-extensions  && make -j16
	sudo make install

}
clean () {
    sudo rm -fr  Python-3.7.13 Python-3.7.13.tgz
}



#build
#clean








