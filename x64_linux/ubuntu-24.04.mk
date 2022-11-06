
iotedgedev:$(HOME)/anaconda3/envs/py3.8.10-iotedge/bin/iotedgedev



vim:base_package
	git config --global core.editor "vim"

base_package:/usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstx265.so

/usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstx265.so:
	sudo apt install  -y vim ncdu  fd-find ripgrep  terminator htop \
		meld cmake make   openssh-server fzf tldr  clang-format clangd  \
		git \
		inxi  gstreamer1.0-plugins-bad fuse libfuse2  curl python3-pip


pre_docker: /proc/sys/fs/binfmt_misc/qemu-aarch64
/proc/sys/fs/binfmt_misc/qemu-aarch64:
	sudo docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	sudo modprobe binfmt_misc
	ls /proc/sys/fs/binfmt_misc
	#docker run --rm -it bpcvregistry.azurecr.io/base_py:v1.0 bash

conda:$(HOME)/anaconda3
$(HOME)/anaconda3:
	sudo  ln -sf /mnt/c/for_linux/anaconda3_for_linux $@

#Option 2 : run  Anaconda3-2020.11-Linux-x86_64.sh
#https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh


az_login:
	az acr login --name $(AZ_REPO_NAME)
nv_login:
	docker login -u '$$oauthtoken'  $(NVCR_REPO)
