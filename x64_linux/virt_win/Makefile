# WIN_PARTITION := /dev/nvme0n1p3    # Replace with your actual Windows partition
# START_RESERVED_IMAGE := start_reserved.img
# START_RESERVED_SIZE_MB := 1        # Size of the start reserved image in MB
EFI_IMAGE := efi_partition.img
# EFI_IMAGE_SIZE_MB := 100
# END_RESERVED_IMAGE := end_reserved.img
# END_RESERVED_SIZE_MB := 1          # Size of the end reserved image in MB
# EFI_PARTITION_NUMBER := 1
# WIN_PARTITION_NUMBER := 2
# COMBINED_DEVICE_NAME := combined_drive
# START_RESERVED_LOOP_DEVICE :=
# EFI_LOOP_DEVICE :=
# END_RESERVED_LOOP_DEVICE :=
# SECTOR_SIZE := 512                 # Usually 512 bytes
# MOUNT_POINT_EFI := ./efi_fake
# MOUNT_POINT_WIN := ./win_fake

test:
	./run.sh test
launch_qemu_kvm:
	./run.sh launch_qemu_kvm

create_device_mapper:
	./run.sh create_device_mapper
remove_device_mapper:
	./run.sh remove_device_mapper
	
PARTITION_FLAG_FILE=./partition_done.flag

create_loop_images:$(PARTITION_FLAG_FILE)

$(EFI_IMAGE):
	./run.sh create_loop_images

$(PARTITION_FLAG_FILE): $(EFI_IMAGE)
	./run.sh create_partitions
all: $(EFI_IMAGE)
	echo done
clean: remove_device_mapper
	rm -vf *.img mapping_table.txt partition_done.flag
	echo "losetup -a |rg lxr |awk -F: '{print $$1}'|xargs sudo losetup -d"
	losetup -a |rg lxr |awk -F: '{print $$1}'|xargs sudo losetup -d
start:
	./run.sh
stop:
	./run.sh

# Ensure the Windows partition is unmounted
install_packages:
	sudo apt install -y qemu-kvm ovmf parted kpartx util-linux
