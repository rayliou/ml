#!/bin/bash
set -ex

install_tljh () {
	#https://tljh.jupyter.org/en/latest/install/custom-server.html
	sudo apt install -y python3 python3-dev git curl
	curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin buspas
}
install_deepstream_601 () {
	echo done
}



