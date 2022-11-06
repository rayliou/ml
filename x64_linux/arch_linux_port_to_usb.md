
 ```
 lsblk
 sudo  mount /dev/sdb2 2
 sudo  rsync -avurP  /{bin,boot,etc,lib,lib64,opt,root,sbin,srv,usr,var} 2/
 sudo mkdir -p  2/{dev,efi,proc,run,sys,tmp}
 sudo arch-chroot 2/
 ```
 # Do

 ```
 # Mount /efi to the ESP partion 1st
  257  grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=2TGRUB  --removable  --recheck
  258  grub-mkconfig -o /boot/grub/grub.cfg
  260  genfstab -U / >> /etc/fstab
  exit
 ```

 1901  reboot

