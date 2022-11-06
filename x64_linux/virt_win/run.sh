#!/bin/bash

# Script to create a combined device with a fake EFI partition, a Windows partition,
# and a tail partition to reserve space for GPT. It then prepares the device for booting with QEMU/KVM.

set -e

# Variables (Modify these according to your setup)
START_RESERVED_IMAGE="start_reserved.img"
START_RESERVED_SIZE_MB=1        # Size of the start reserved image in MB
EFI_IMAGE="efi_partition.img"
EFI_IMAGE_SIZE_MB=100           # Size of the EFI image in MB
WIN_PARTITION="/dev/nvme0n1p3"  # Replace with your actual Windows partition
END_RESERVED_IMAGE="end_reserved.img"
END_RESERVED_SIZE_MB=1          # Size of the end reserved image in MB
EFI_PARTITION_NUMBER=1
WIN_PARTITION_NUMBER=2
COMBINED_DEVICE_NAME="combined_drive"
START_RESERVED_LOOP_DEVICE=""
EFI_LOOP_DEVICE=""
END_RESERVED_LOOP_DEVICE=""
SECTOR_SIZE=512                 # Usually 512 bytes
MOUNT_POINT_EFI="./efi_fake"
MOUNT_POINT_WIN="./win_fake"

# Function to create loop images
create_loop_images() {
    dd if=/dev/zero of="$START_RESERVED_IMAGE" bs=1M count="$START_RESERVED_SIZE_MB"
    dd if=/dev/zero of="$END_RESERVED_IMAGE" bs=1M count="$END_RESERVED_SIZE_MB"
    dd if=/dev/zero of="$EFI_IMAGE" bs=1M count="$EFI_IMAGE_SIZE_MB"
    mkfs.vfat "$EFI_IMAGE"
    TEMP_MOUNT="/tmp/efi_temp_mount"
    mkdir -p "$TEMP_MOUNT"
    sudo mount "$EFI_IMAGE" "$TEMP_MOUNT"
    sudo cp -afr /boot/efi/* "$TEMP_MOUNT/"
    #sudo rm -fr $TEMP_MOUNT/EFI/{ubuntu,arch,Boot}
    sudo rm -fr $TEMP_MOUNT/EFI/{ubuntu,arch,Boot}
    ls -l  "$TEMP_MOUNT/EFI/"
    echo "Listing contents of EFI image:"
    ls -l "$TEMP_MOUNT"
    sudo umount "$TEMP_MOUNT"
    echo After umount print $TEMP_MOUNT
    ls -l  $TEMP_MOUNT/
    rmdir "$TEMP_MOUNT"
}
mount_loop_devices() {
    START_RESERVED_LOOP_DEVICE=$(sudo losetup -f --show "$START_RESERVED_IMAGE")
    echo "Start Reserved Loop Device: $START_RESERVED_LOOP_DEVICE"
    EFI_LOOP_DEVICE=$(sudo losetup -f --show "$EFI_IMAGE")
    echo "EFI Loop Device: $EFI_LOOP_DEVICE"
    END_RESERVED_LOOP_DEVICE=$(sudo losetup -f --show "$END_RESERVED_IMAGE")
    echo "End Reserved Loop Device: $END_RESERVED_LOOP_DEVICE"
    echo "Mounted loop devices."
}
umount_loop_devices() {
    sudo losetup -d "$START_RESERVED_LOOP_DEVICE"
    sudo losetup -d "$EFI_LOOP_DEVICE"
    sudo losetup -d "$END_RESERVED_LOOP_DEVICE"
    echo "Unmounted loop devices."
}
get_size_sectors() {
    # Get sector sizes
    SECTOR_SIZE=$(cat /sys/block/$(basename "$EFI_LOOP_DEVICE")/queue/hw_sector_size)
    echo "EFI Sector Size: $SECTOR_SIZE bytes"

    # Get sector sizes for start and end reserved parts
    START_RESERVED_SIZE_SECTORS=$(sudo blockdev --getsz "$START_RESERVED_LOOP_DEVICE")
    EFI_SIZE_SECTORS=$(sudo blockdev --getsz "$EFI_LOOP_DEVICE")
    WIN_SIZE_SECTORS=$(sudo blockdev --getsz "$WIN_PARTITION")
    END_RESERVED_SIZE_SECTORS=$(sudo blockdev --getsz "$END_RESERVED_LOOP_DEVICE")
    printf "Start Reserved Size:     %12d sectors\n" "$START_RESERVED_SIZE_SECTORS"
    printf "EFI Size:                %12d sectors\n" "$EFI_SIZE_SECTORS"
    printf "Windows Partition Size:  %12d sectors\n" "$WIN_SIZE_SECTORS"
    printf "End Reserved Size:       %12d sectors\n" "$END_RESERVED_SIZE_SECTORS"

    # Calculate the total size required for the combined device
    TOTAL_MAPPED_SECTORS=$((START_RESERVED_SIZE_SECTORS + EFI_SIZE_SECTORS + WIN_SIZE_SECTORS + END_RESERVED_SIZE_SECTORS))
    echo "Total Mapped Sectors: $TOTAL_MAPPED_SECTORS sectors"
}
remove_combined_device() {
    echo "Removing combined device... current dmsetup ls:"
    sudo dmsetup ls
    # echo sudo dmsetup remove "${COMBINED_DEVICE_NAME}1"
    # echo sudo dmsetup remove "${COMBINED_DEVICE_NAME}2"
    # echo sudo dmsetup remove "$COMBINED_DEVICE_NAME"
    sudo dmsetup remove "${COMBINED_DEVICE_NAME}2" || true
    sudo dmsetup remove "${COMBINED_DEVICE_NAME}1" || true
    sudo dmsetup remove "$COMBINED_DEVICE_NAME" || true
    echo "After sudo dmsetup remove:"
    sudo dmsetup ls
}   
create_combined_device() {
    echo "Creating combined device with Device Mapper..."
    echo "Creating Device Mapper table..."
    {
        echo "0 $START_RESERVED_SIZE_SECTORS linear $START_RESERVED_LOOP_DEVICE 0"  # Start reserved
        echo "$START_RESERVED_SIZE_SECTORS $EFI_SIZE_SECTORS linear $EFI_LOOP_DEVICE 0"  # EFI partition
        echo "$((START_RESERVED_SIZE_SECTORS + EFI_SIZE_SECTORS)) $WIN_SIZE_SECTORS linear $WIN_PARTITION 0"  # Windows partition
        echo "$((START_RESERVED_SIZE_SECTORS + EFI_SIZE_SECTORS + WIN_SIZE_SECTORS)) $END_RESERVED_SIZE_SECTORS linear $END_RESERVED_LOOP_DEVICE 0"  # End reserved
    } | tee mapping_table.txt
    # Remove existing device-mapper device if it exists
    if sudo dmsetup info "$COMBINED_DEVICE_NAME" &>/dev/null; then
        remove_combined_device
    fi

    echo sudo dmsetup create "$COMBINED_DEVICE_NAME" mapping_table.txt
    sudo dmsetup create "$COMBINED_DEVICE_NAME" mapping_table.txt

    echo "Verifying combined device..."
    COMBINED_DEVICE="/dev/mapper/$COMBINED_DEVICE_NAME"
    COMBINED_SIZE_SECTORS=$(sudo blockdev --getsz "$COMBINED_DEVICE")
    echo "Combined Device Size: $COMBINED_SIZE_SECTORS sectors"

    # Verify that the total mapped sectors do not exceed the combined device size
    if [ "$TOTAL_MAPPED_SECTORS" -gt "$COMBINED_SIZE_SECTORS" ]; then
        echo "Error: Total mapped sectors ($TOTAL_MAPPED_SECTORS) exceed combined device size ($COMBINED_SIZE_SECTORS)."
        exit 1
    fi
    echo "Created combined device with Device Mapper: $COMBINED_DEVICE"
}
# Only run at the first time
# FLAG: 
PARTITION_FLAG_FILE="./partition_done.flag"
create_partitions() {
    if [ -f "$PARTITION_FLAG_FILE" ]; then
        echo "Partitions already created."
        return
    fi
    # echo "Partitioning the combined device..."
    echo sudo parted "$COMBINED_DEVICE" --script mklabel gpt
    sudo parted "$COMBINED_DEVICE" --script mklabel gpt

    START_RESERVED_END=$((START_RESERVED_SIZE_SECTORS - 1))
    EFI_PARTITION_START=$START_RESERVED_SIZE_SECTORS
    EFI_PARTITION_END=$((EFI_PARTITION_START + EFI_SIZE_SECTORS - 1))
    WIN_PARTITION_START=$((EFI_PARTITION_END + 1))
    WIN_PARTITION_END=$((WIN_PARTITION_START + WIN_SIZE_SECTORS - 1))
    END_RESERVED_START=$((WIN_PARTITION_END + 1))
    # 创建分区
    sudo parted "$COMBINED_DEVICE" --script unit s \
        mkpart primary fat32 "${EFI_PARTITION_START}s" "${EFI_PARTITION_END}s" \
        mkpart primary ntfs "${WIN_PARTITION_START}s" "${WIN_PARTITION_END}s"

    sudo parted "$COMBINED_DEVICE" --script set 1 esp on
    touch "$PARTITION_FLAG_FILE"
    echo "Partitioning complete."
}

remove_device_mapper() {
    # sudo kpartx -dv "/dev/mapper/$COMBINED_DEVICE_NAME"
    echo "remove device mapper"
}
# # Function to create device mapper
create_device_mapper() {
    echo "Verifying partitions with 'parted'..."
    sudo parted "$COMBINED_DEVICE" unit s print
    # echo "Setting up partition mappings with 'kpartx'..."
    # sudo kpartx -av "$COMBINED_DEVICE"
    # sleep 2
    EFI_MAPPED_PART="/dev/mapper/${COMBINED_DEVICE_NAME}1"
    WIN_MAPPED_PART="/dev/mapper/${COMBINED_DEVICE_NAME}2" 
    echo "EFI Mapped Partition: $EFI_MAPPED_PART"
    echo "Windows Mapped Partition: $WIN_MAPPED_PART"
    echo "Checking partition positions with 'file' command..."
    # sudo mount $EFI_MAPPED_PART $MOUNT_POINT_EFI
    # ls  -l $MOUNT_POINT_EFI/EFI/
    # echo 
    # echo 
    # echo 
    # sudo umount $EFI_MAPPED_PART

    sudo file -s "$EFI_MAPPED_PART"
    sudo file -s "$WIN_MAPPED_PART"
    echo "please debug....."

}

# Function to mount partitions
mount_partitions() {
    echo "Mounting partitions..."
    sudo kpartx -av "$COMBINED_DEVICE"
    EFI_MAPPED_PART="/dev/mapper/${COMBINED_DEVICE_NAME}p$EFI_PARTITION_NUMBER"
    WIN_MAPPED_PART="/dev/mapper/${COMBINED_DEVICE_NAME}p$WIN_PARTITION_NUMBER"
    sudo mount "$EFI_MAPPED_PART" "$MOUNT_POINT_EFI"
    sudo mount -o ro "$WIN_MAPPED_PART" "$MOUNT_POINT_WIN"
}

# Function to inspect partitions
inspect_partitions() {
    echo "Listing files in EFI partition..."
    ls "$MOUNT_POINT_EFI"
    echo "Listing files in Windows partition..."
    ls "$MOUNT_POINT_WIN"
}

# Function to unmount partitions
unmount_partitions() {
    echo "Unmounting partitions..."
    sudo umount "$MOUNT_POINT_EFI"
    sudo umount "$MOUNT_POINT_WIN"
    echo "Removing partition mappings..."
    sudo kpartx -dv "$COMBINED_DEVICE"
}

# Function to launch QEMU/KVM
launch_qemu_kvm() {
    echo "Launching QEMU/KVM..."
    
    # Update OVMF firmware path to match the 4M version
    OVMF_CODE="./OVMF_CODE_4M.fd"
    OVMF_VARS="./OVMF_VARS_4M.fd"  # Use absolute path
    
    if [ ! -f "$OVMF_CODE" ]; then
        echo "OVMF_CODE file not found at $OVMF_CODE. Attempting to copy from a different location."
        if [ -f "/usr/share/OVMF/OVMF_CODE_4M.fd" ]; then
            sudo cp "/usr/share/OVMF/OVMF_CODE_4M.fd" "$OVMF_CODE"
            echo "Copied OVMF_CODE.fd to $OVMF_CODE"
        else
            echo "Error: Could not find OVMF_CODE file to copy."
            exit 1
        fi
    fi
    
    if [ ! -f "$OVMF_VARS" ]; then
        echo "OVMF_VARS file not found at $OVMF_VARS. Attempting to copy from a different location."
        if [ -f "/usr/share/OVMF/OVMF_VARS_4M.fd" ]; then
            sudo cp "/usr/share/OVMF/OVMF_VARS_4M.fd" "$OVMF_VARS"
            echo "Copied OVMF_VARS.fd to $OVMF_VARS"
        else
            echo "Error: Could not find OVMF_VARS file to copy."
            exit 1
        fi
    fi
    sudo qemu-system-x86_64 \
    -display gtk,window-close=off \
    -machine type=q35,accel=kvm \
    -enable-kvm \
    -drive file=/dev/mapper/combined_drive,format=raw,if=none,id=drive0,cache=none \
    -device virtio-scsi-pci,id=scsi \
    -device scsi-hd,drive=drive0,bootindex=0,bus=scsi.0 \
    -cpu host,hv-relaxed,hv-spinlocks=0x1fff,topoext,svm \
    -smp 8 \
    -m 16G \
    -drive if=pflash,format=raw,unit=0,file="$OVMF_CODE",readonly=on \
    -drive if=pflash,format=raw,unit=1,file="$OVMF_VARS" \
    -object rng-random,id=rng0,filename=/dev/urandom \
    -device virtio-rng-pci,max-bytes=1024,period=1000 \
    -vga std \
    -device intel-hda \
    -device hda-duplex \
    -device qemu-xhci,id=xhci \
    -device usb-mouse,bus=xhci.0 \
    -device usb-kbd,bus=xhci.0

    #-cdrom /home/lxr/Downloads/Win11_24H2_English_x64.iso \

    

    

    


        # -acpitable file=./acpitables/MSDM \
        # -smbios file=./acpitables/smbios_type_0.bin \
        # -smbios file=./acpitables/smbios_type_1.bin \




        #-cdrom ./ubuntu-24.04-desktop-amd64.iso

        #-d cpu_reset,guest_errors,unimp

        # -vnc :0 \

        # -drive if=pflash,format=raw,readonly=on,file="$OVMF_CODE" \
        # -drive if=pflash,format=raw,file="$OVMF_VARS" \
}





# Main execution
case "$1" in
    create_loop_images)
        create_loop_images
        ;;
    create_partitions)
        mount_loop_devices
        get_size_sectors
        create_combined_device
        create_partitions
        remove_combined_device
        umount_loop_devices
        ;;
    create_device_mapper)
        mount_loop_devices
        get_size_sectors
        create_combined_device
        create_device_mapper
        ;;
    remove_device_mapper)
        remove_device_mapper
        remove_combined_device
        umount_loop_devices
        ;;
    mount_partitions)
        mount_partitions
        ;;
    inspect_partitions)
        inspect_partitions
        ;;
    unmount_partitions)
        unmount_partitions
        ;;
    remove_combined_device)
        remove_combined_device
        umount_loop_devices
        ;;
    test)
        create_loop_images
        mount_loop_devices
        get_size_sectors
        create_combined_device
        create_partitions
        create_device_mapper
        launch_qemu_kvm
        ;;
    launch_qemu_kvm)
        create_loop_images
        mount_loop_devices
        get_size_sectors
        create_combined_device
        create_device_mapper
        launch_qemu_kvm
        remove_device_mapper
        remove_combined_device
        umount_loop_devices
        ;;
    *)
        echo "Usage: $0 {create_loop_images|create_device_mapper|mount_partitions|inspect_partitions|unmount_partitions|remove_combined_device|launch_qemu_kvm}"
        exit 1
        ;;
esac

echo "Operation completed."
