# Installing Debian 12 (bookworm) on Lenovo Iomega ix4-300d

Lenovo Iomega ix4-300s is a NAS released in late 2012 equipped with:
- Marvell Armada XP 1.3GHz Dual Core (MV78230 ARMv7 SoC)
- 512MB DDR3 Memory
- 4 x 3.5” SATA II (No Hot Swap)
- 2 x 1 GbE Ethernet ports
- 1 x USB 3.0 port
- 2 x USB 2.0 ports

The latest **firmware** update Version 4.1.414.34909 can be found here:

http://download.lenovo.com/nas/lifeline/h4c-4.1.414.34909.tgz

The latest **imager** with that version can be found here:

https://download.lenovo.com/nasupdate/asgimage/h4c-4.1.414.34909.zip

The original firmware is based on Debian 7 (wheezy) and it is stored into a flash memory. NAS can boot without any disk if the flash is ok. If the flash is corrupted the above imager must be used.

```
BootROM 1.15
Booting from NAND flash
DDR3 Training Sequence - Ver 2.3.4 
DDR3 Training Sequence - Ended Successfully 
BootROM: Image checksum verification PASSED

 __   __                      _ _
|  \/  | __ _ _ ____   _____| | |
| |\/| |/ _` | '__\ \ / / _ \ | |
| |  | | (_| | |   \ V /  __/ | |
|_|  |_|\__,_|_|    \_/ \___|_|_|
         _   _     ____              _
        | | | |   | __ )  ___   ___ | |_ 
        | | | |___|  _ \ / _ \ / _ \| __| 
        | |_| |___| |_) | (_) | (_) | |_ 
         \___/    |____/ \___/ \___/ \__| 
 ** LOADER 2.3.2.6  **


U-Boot 2009.08 (Mar 04 2013 - 11:13:04) Marvell version:  2.3.2 PQ
U-Boot Addressing:
       Code:            00600000:006BFFF0
       BSS:             00708EC0
       Stack:           0x5fff70
       PageTable:       0x8e0000
       Heap address:    0x900000:0xe00000
Board: DB-78230-BP rev 2.0 Wistron
SoC:   MV78230 A0
       running 2 CPUs
       Custom configuration
CPU:   Marvell PJ4B (584) v7 (Rev 2) LE
       CPU # 0
       CPU @ 1333Mhz, L2 @ 667Mhz
       DDR @ 667Mhz, TClock @ 250Mhz
       DDR 32Bit Width, FastPath Memory Access
       DDR ECC Disabled
PEX 0.0(0): Root Complex Interface, Detected Link X4, GEN 1.1
PEX 1.0(1): Root Complex Interface, Detected Link X1, GEN 2.0
DRAM:  512 MB
       CS 0: base 0x00000000 size 512 MB
       Addresses 14M - 0M are saved for the U-Boot usage.
NAND:  1024 MiB
Bad block table found at page 524224, version 0x01
Bad block table found at page 524160, version 0x01
nand_read_bbt: Bad block at 0x000003c60000
FPU initialized to Run Fast Mode.
USB 0: Host Mode
USB 1: Host Mode
USB 2: Device Mode
Modules Detected:
MMC:   MRVL_MMC: 0
Net:   egiga0 [PRIME], egiga1
Hit any key to stop autoboot:  0 

NAND read: device 0 offset 0x120000, size 0x400000
 4194304 bytes read: OK

NAND read: device 0 offset 0x520000, size 0x400000
 4194304 bytes read: OK
## Booting kernel from Legacy Image at 00040000 ...
   Image Name:   Linux-3.2.40
   Created:      2020-01-02  11:18:50 UTC
   Image Type:   ARM Linux Kernel Image (uncompressed)
   Data Size:    3656376 Bytes =  3.5 MB
   Load Address: 00008000
   Entry Point:  00008000
   Verifying Checksum ... OK
## Loading init Ramdisk from Legacy Image at 02000000 ...
   Image Name:   
   Created:      2020-01-14  10:40:35 UTC
   Image Type:   ARM Linux RAMDisk Image (bzip2 compressed)
   Data Size:    3012478 Bytes =  2.9 MB
   Load Address: 00000000
   Entry Point:  00000000
   Verifying Checksum ... OK
   Loading Kernel Image ... OK
OK

Starting kernel ...

Uncompressing Linux... done, booting the kernel.



Welcome to CenterPoint.
ix4-300d login:
```
```
root@ix4-300d:/# cat /etc/debian_version 
7.11
```
```
root@ix4-300d:/# cat /proc/version 
Linux version 3.2.40 (soho@bsoho083.iomegacorp.com) (gcc version 4.7.2 (crosstool-NG 1.20.0) ) #1 SMP Thu Jan 2 06:18:39 EST 2020 v2.1.1.1
```
```
root@ix4-300d:/# cat /proc/mtd        
dev:    size   erasesize  name
mtd0: 000e0000 00020000 "uboot"
mtd1: 00020000 00020000 "env"
mtd2: 00020000 00020000 "env2"
mtd3: 00400000 00020000 "zImage"
mtd4: 00400000 00020000 "initrd"
mtd5: 3f200000 00020000 "boot"
mtd6: 40000000 00020000 "flash"
```
```
root@ix4-300d:/# cat /proc/cpuinfo 
Processor       : Marvell PJ4Bv7 Processor rev 2 (v7l)
processor       : 0
BogoMIPS        : 1332.01

processor       : 1
BogoMIPS        : 1332.01

Features        : swp half thumb fastmult vfp edsp vfpv3 tls 
CPU implementer : 0x56
CPU architecture: 7
CPU variant     : 0x2
CPU part        : 0x584
CPU revision    : 2

Hardware        : Marvell Armada XP Development Board
Revision        : 0000
Serial          : 0000000000000000
```

The bootloader is Marvell U-Boot. My NAS has the following signature:

`U-Boot 2009.08 (Mar 04 2013 - 11:13:04) Marvell version:  2.3.2 PQ`.

The End Of Service Life (EOSL) was March 31, 2020.


## Prerequisites

- USB-to-TTL adapter (mandatory) to connect to the bootloader
- A TFTP server (faster) or and USB stick (slower) to download the Debian installer
- A PC with macOS or Windows. The following procedure is for macOS because we do not need any additional software to install for complete the task. The procedure for Windows is not documented here.
- A Linux box or a virtual machine with any Linux flavour (optional) to prepare the Debian installed image. I used an online Ubuntu VM on https://www.onworks.net.
- Wired connection from NAS Ethernet port 1 (the top one) with DHCP and internet access to continue the Debian installation after boot.

## Preparing the files

On a Linux box:

1. Download `vmlinuz`, `initrd.gz` and `armada-xp-lenovo-ix4-300d.dtb` files from the Debian website: 

   https://deb.debian.org/debian/dists/bookworm/main/installer-armhf/current/images/netboot/vmlinuz
   https://deb.debian.org/debian/dists/bookworm/main/installer-armhf/current/images/netboot/initrd.gz
   https://deb.debian.org/debian/dists/bookworm/main/installer-armhf/current/images/device-tree/armada-xp-lenovo-ix4-300d.dtb

2. Append dtb file to the kernel: 
   ```
   cat vmlinuz armada-xp-lenovo-ix4-300d.dtb > vmlinuz_ix4_300d
   ```

3. Create an uImage with appended init ramdisk for TFTP boot:
   ```
   mkimage -A arm -O linux -T multi -C none -a 0x04000000 -e 0x04000000 -n "Debian armhf installer" -d vmlinuz_ix4_300d:initrd.gz uImage_di_ix4_300d_bookworm
   ```
4. Create separate uImage and uInitrd for USB boot:
   ```
   mkimage -A arm -O linux -T kernel  -C none -a 0x04000000 -e 0x04000000  -n "Debian armhf installer" -d vmlinuz_ix4_300d uImage_ix4_300d_bookworm
   mkimage -A arm -O linux -T ramdisk -C none -a 0x2000000  -e 0x2000000   -n "Debian armhf installer" -d initrd.gz        uInitrd_ix4_300d_bookworm
   ```
   > [!NOTE]
   > The `mkimage` command is used to create images for use with the U-Boot boot loader. Thes images can contain the linux kernel, device tree blob, root file system image, firmware images etc., either separate or combined.
   > 
   > mkimage supports many image formats. Some of these formats may be used by embedded boot firmware to load U-Boot. Others may be used by U-Boot to load Linux (or some other kernel):
   >
   >The legacy image format concatenates the individual parts (for example, kernel image, device tree blob and ramdisk image) and adds a 64 byte header containing information about the target architecture, operating system, image type, compression method, entry points, time stamp, checksums, etc.

For smart people the final files are also available here ready to download:
TFTP boot|USB boot
---------|--------
[uImage_di_ix4_300d_bookworm](uImage_di_ix4_300d_bookworm)|[uImage_ix4_300d_bookworm](uImage_ix4_300d_bookworm)<br>[uInitrd_ix4_300d_bookwom](uInitrd_ix4_300d_bookwom)

## Preparing the TFTP server

_Skip it if you want to proceed with an USB stick._

1. Copy the `uImage_di_ix4_300d_bookworm` file prepared above into `/private/tftpboot` folder of macOS.
   > [!NOTE]
   > By default the built in macOS TFTP server uses the folder `/private/tftpboot` which is hidden in Finder, but can be accessed by using “Go to Folder” or hitting Command+Shift+G and entering `/private/tftpboot`
3. Open a Terminal an execute the following command
   ```
   sudo launchctl load -F /System/Library/LaunchDaemons/tftp.plist
   ```
   ```
   sudo launchctl start com.apple.tftpd
   ```
   
## Preparing the USB stick

_Skip it if you prepared a TFTP server._

1. Create an USB stick with an ext2 partition as first partition. Marvell U-Boot can only boot from the first partition.
2. Copy `uImage_ix4_300d_bookworm` and `uinitrd_ix4_300d_bookworm` into it.
> [!NOTE]
> We do not need an bootable USB stick.


## Connecting the USB-to-TTL adapter

UART is on connector CN9 (four pins). Connection parameters are 115200/8N1.

![](images/CN9_UART_Connector.png)

Pin|Function|Description
---|--------|-----------
1|VCC|VCC can be controlled by the adjacent JP1: bridging 1 and 2 provides 3V3, bridging 2 and 3 provides 5V - but beware that this does NOT change the TX/RX voltage which is 3V3 max. VCC is not used.
2|TX|Connect to the RX pin of your USB-to-TTL adapter
3|GND|Connect to GND of your USB-to-TTL adapter
4|RX|Connect to the TX pin of your USB-to-TTL adapter

1. Connect the USB-to-TTL adapter via USB to your PC.
2. On macOS Open a Terminal and execute
   ```
   screen /dev/cu.SLAB_USBtoUART 115200
   ```
3. Power on the Lenovo Iomega ix4-300d
4. Press any key to stop the booting process and receive the Marvell U-Boot prompt

```
BootROM 1.15
Booting from NAND flash
DDR3 Training Sequence - Ver 2.3.4 
DDR3 Training Sequence - Ended Successfully 
BootROM: Image checksum verification PASSED

 __   __                      _ _
|  \/  | __ _ _ ____   _____| | |
| |\/| |/ _` | '__\ \ / / _ \ | |
| |  | | (_| | |   \ V /  __/ | |
|_|  |_|\__,_|_|    \_/ \___|_|_|
         _   _     ____              _
        | | | |   | __ )  ___   ___ | |_ 
        | | | |___|  _ \ / _ \ / _ \| __| 
        | |_| |___| |_) | (_) | (_) | |_ 
         \___/    |____/ \___/ \___/ \__| 
 ** LOADER 2.3.2.6  **


U-Boot 2009.08 (Mar 04 2013 - 11:13:04) Marvell version:  2.3.2 PQ
U-Boot Addressing:
       Code:            00600000:006BFFF0
       BSS:             00708EC0
       Stack:           0x5fff70
       PageTable:       0x8e0000
       Heap address:    0x900000:0xe00000
Board: DB-78230-BP rev 2.0 Wistron
SoC:   MV78230 A0
       running 2 CPUs
       Custom configuration
CPU:   Marvell PJ4B (584) v7 (Rev 2) LE
       CPU # 0
       CPU @ 1333Mhz, L2 @ 667Mhz
       DDR @ 667Mhz, TClock @ 250Mhz
       DDR 32Bit Width, FastPath Memory Access
       DDR ECC Disabled
PEX 0.0(0): Root Complex Interface, Detected Link X4, GEN 1.1
PEX 1.0(1): Root Complex Interface, Detected Link X1, GEN 2.0
DRAM:  512 MB
       CS 0: base 0x00000000 size 512 MB
       Addresses 14M - 0M are saved for the U-Boot usage.
NAND:  1024 MiB
Bad block table found at page 524224, version 0x01
Bad block table found at page 524160, version 0x01
nand_read_bbt: Bad block at 0x000003c60000
FPU initialized to Run Fast Mode.
USB 0: Host Mode
USB 1: Host Mode
USB 2: Device Mode
Modules Detected:
MMC:   MRVL_MMC: 0
Net:   egiga0 [PRIME], egiga1
Hit any key to stop autoboot:  0 
Marvell>> 
```

## Boot the NAS from TFTP server

_Skip it if you prepared the USB stick._

Assuming `192.168.1.10` is the macOS IP address (TFTP server) and `192.168.1.111` ia an available IP address in your network not assigned by DHCP, from `Marvell>>` prompt enter the following commands:

1. Set the IP address of the NAS: 
   ```
   setenv ipaddress 192.168.1.111
   ```

2. Set the IP address of the macOS TFTP server: 
   ```
   setenv serverip 192.168.1.10
   ```

3. Check if network connection works:
   ```
   ping 192.168.1.10
   ```

4. Transfer the Debian installer via TFTP into the NAS RAM:
   ```
   tftpboot uImage_di_ix4_300d_bookworm
   ```

5. Boot the Debian installer in RAM:
   ```
   bootm 0x2000000
   ```

## Boot th NAS from USB stick

_Skip it if you prepared the TFTP server._

1. Insert the USB stick into the **rear top** USB port. Marvell U-Boot can only boot from the rear top USB port.

2. From `Marvell>>` prompt enter the following commands:
   ```
   usb start
   usb tree
   usb info
   usb part
   usb stop
   ext2load usb 0:1 0x0040000 uImage_ix4_300d_bookworm
   ext2load usb 0:1 0x2000000 uInitrd_ix4_300d_bookworm
   setenv bootargs $console $mtdparts root=/dev/sda2 rw rootdelay=10
   bootm 0x40000 0x2000000
   ```
   > [!NOTE]
   > `usb tree`, `usb info` and `usb part` are for information only.

The log of previous commands is available in the following:
```
Marvell>> usb start
(Re)start USB...
USB:   Active port:     0
Register 10011 NbrPorts 1
USB EHCI 1.00
scanning bus for devices... 2 USB Device(s) found
Waiting for storage device(s) to settle before scanning...
       scanning bus for storage devices... 1 Storage Device(s) found
Marvell>> usb tree

Device Tree:
  1  Hub (480 Mb/s, 0mA)
  |  u-boot EHCI Host Controller 
  |
  +-2  Mass Storage (480 Mb/s, 200mA)
         13111409002422
     
Marvell>> usb info
1: Hub,  USB Revision 2.0
 - u-boot EHCI Host Controller 
 - Class: Hub
 - PacketSize: 64  Configurations: 1
 - Vendor: 0x0000  Product 0x0000 Version 1.0
   Configuration: 1
   - Interfaces: 1 Self Powered 0mA
     Interface: 0
     - Alternate Setting 0, Endpoints: 1
     - Class Hub
     - Endpoint 1 In Interrupt MaxPacket 8 Interval 255ms

2: Mass Storage,  USB Revision 2.0
 -   13111409002422
 - Class: (from Interface) Mass Storage
 - PacketSize: 64  Configurations: 1
 - Vendor: 0x0718  Product 0x07f0 Version 1.18
   Configuration: 1
   - Interfaces: 1 Bus Powered 200mA
     Interface: 0
     - Alternate Setting 0, Endpoints: 2
     - Class Mass Storage, Transp. SCSI, Bulk only
     - Endpoint 1 Out Bulk MaxPacket 512
     - Endpoint 2 In Bulk MaxPacket 512

Marvell>> usb part

Partition Map for USB device 0  --   Partition Type: DOS

Partition     Start Sector     Num Sectors     Type
    1                 2048         2097152      83

Marvell>> usb stop
stopping USB..
Marvell>> ext2load usb 0:1 0x0040000 uImage_ix4_300d_bookworm
Loading file "uImage_ix4_300d_bookworm" from usb device 0:1 (usbda1)
5351835 bytes read
Marvell>> ext2load usb 0:1 0x2000000 uInitrd_ix4_300d_bookworm
Loading file "uInitrd_ix4_300d_bookworm" from usb device 0:1 (usbda1)
26337308 bytes read
Marvell>> setenv bootargs $console $mtdparts root=/dev/sda2 rw rootdelay=10
Marvell>> bootm 0x40000 0x2000000
## Booting kernel from Legacy Image at 00040000 ...
   Image Name:   Debian armhf installer
   Created:      2023-08-24  21:17:04 UTC
   Image Type:   ARM Linux Kernel Image (uncompressed)
   Data Size:    5351771 Bytes =  5.1 MB
   Load Address: 04000000
   Entry Point:  04000000
   Verifying Checksum ... OK
## Loading init Ramdisk from Legacy Image at 02000000 ...
   Image Name:   Debian armhf installer
   Created:      2023-08-24  21:14:13 UTC
   Image Type:   ARM Linux RAMDisk Image (uncompressed)
   Data Size:    26337244 Bytes = 25.1 MB
   Load Address: 02000000
   Entry Point:  02000000
   Verifying Checksum ... OK
   Loading Kernel Image ... OK
OK

Starting kernel ...
```

## Debian installation

The Debian installer should start in the serial console window with the following screen:
```
[            (1*installer)  2 shell  3 shell  4- log           ][ Aug 24 21:36 ]
                                                                                
                                                                                
                                                                                
  ┌───────────────────────┤ [!!] Select a language ├────────────────────────┐   
  │                                                                         │   
  │ Choose the language to be used for the installation process. The        │   
  │ selected language will also be the default language for the installed   │   
  │ system.                                                                 │   
  │                                                                         │   
  │ Language:                                                               │   
  │                                                                         │   
  │                               C                                         │   
  │                               English                                   │   
  │                                                                         │   
  │     <Go Back>                                                           │   
  │                                                                         │   
  └─────────────────────────────────────────────────────────────────────────┘   
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
<Tab> moves; <Space> selects; <Enter> activates buttons                         
```

Go through the process as shown on screen. You will receive an error related to `grub` installation at the end. Don't worry and skip bootloader installation. You will receive the following warning: 

```
You will need to boot manually with the /vmlinuz kernel on partition /dev/sda1 and root=/dev/sda2 passed as a kernel argument.
```

Do not complete the final stage of the install but choose to `Execute a shell` instead. Run the following commands: 

```
mount --bind /dev /target/dev
mount -t proc none /target/proc
mount -t sysfs none /target/sys
chroot /target /bin/sh
apt-get update
apt-get install flash-kernel
```

Replace the content of the flash-kernel database file `/etc/flash-kernel/db` using `nano`: 
```
nano /etc/flash-kernel/db
```

with the following content
```
Machine: Lenovo Iomega ix4-300d
Kernel-Flavors: armmp armmp-lpae
DTB-Id: armada-xp-lenovo-ix4-300d.dtb
DTB-Append: yes
U-Boot-Kernel-Address: 0x00008000
U-Boot-Initrd-Address: 0x0
Boot-Kernel-Path: /boot/uImage
Boot-Initrd-Path: /boot/uInitrd
Boot-DTB-Path: /boot/dtb
Required-Packages: u-boot-tools
Bootloader-Sets-Incorrect-Root: no
```

Update initramfs and kernel: 
```
update-initramfs -u
```

Set label on the rootfs partition: 
```
e2label /dev/sda2 rootfs
```

Exit chroot and reboot: 
```
exit
reboot
```

Press any key to stop the booting process again.


## Links

https://forum.doozan.com/read.php?2,131833

https://github.com/benoitm974/ix4-300d/wiki

https://github.com/5p0ng3b0b/ix4-300d
