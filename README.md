Installing Debian 12 (bookworm) on Lenovo Iomega ix4-300d NAS.

## Prerequisites

- USB-to-TTL adapter (mandatory)
- A TFTP server (faster) or and USB stick (slower)
- A PC with macOS or Windows. The following procedure is for macOS because we do not need any additional software to install for complete the task. The procedure for Windows is not documented here.
- A Linux box or a virtual machine with any Linux flavour (optional). I used an online Ubuntu VM on https://www.onworks.net.

## Preparing the file

Download `vmlinuz`, `initrd.gz` and `armada-xp-lenovo-ix4-300d.dtb` files from the Debian website: 

https://deb.debian.org/debian/dists/bookworm/main/installer-armhf/current/images/netboot/vmlinuz
https://deb.debian.org/debian/dists/bookworm/main/installer-armhf/current/images/netboot/initrd.gz
https://deb.debian.org/debian/dists/bookworm/main/installer-armhf/current/images/device-tree/armada-xp-lenovo-ix4-300d.dtb

On a Linux box append dtb file to the kernel: 

```
cat vmlinuz armada-xp-lenovo-ix4-300d.dtb > vmlinuz_ix4_300d
```

Create an uImage with appended init ramdisk:

```
mkimage -A arm -O linux -T multi -C none -a 0x04000000 -e 0x04000000  -n "Debian armhf installer" -d vmlinuz_ix4_300d:initrd.gz uImage_ix4_300d_bookworm
```

> [!NOTE]
> The `mkimage` command is used to create images for use with the U-Boot boot loader. Thes images can contain the linux kernel, device tree blob, root file system image, firmware images etc., either separate or combined.
> 
> mkimage supports many image formats. Some of these formats may be used by embedded boot firmware to load U-Boot. Others may be used by U-Boot to load Linux (or some other kernel):
>
>The legacy image format concatenates the individual parts (for example, kernel image, device tree blob and ramdisk image) and adds a 64 byte header containing information about the target architecture, operating system, image type, compression method, entry points, time stamp, checksums, etc.

For lazy people the final file is also available [here](uImage_ix4_300d_bookworm) ready to download.

## Preparing the TFTP server

Skip it if you want to proceed with an USB stick.

1. Copy the `uImage_ix4_300d_bookworm` file prepared into `/private/tftpboot` folder of macOS.
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

Skip it if you prepared a TFTP server.


## Connecting the USB-to-TTL adapter

UART is on connector CN9 (four pins). Connection parameters are 115200/8N1.

![](images/CN9_UART_Connector.png)

Pin|Function|Description
---|--------|-----------
1|VCC|VCC can be controlled by the adjacent JP1: bridging 1 and 2 provides 3V3, bridging 2 and 3 provides 5V - but beware that this does NOT change the TX/RX voltage which is 3V3 max. VCC is not connected to the USB-to-TTL adapter.
2|TX|Connect to the RX pin of your USB-to-TTL adapter
3|GND|Connect to GND of your USB-to-TTL adapter
4|RX|Connect to the TX pin of your USB-to-TTL adapter

1. Connect the USB-to-TTL adapter via USB to a PC. The following procedure is for macOS but once the necessary changes have been made can be completed with Windows too.
2. On macOS Open a Terminal and execute
   ```screen /dev/cu.SLAB_USBtoUART 115200```
3. Power on the Lenovo Iomega ix4-300d
4. Press any key to stop the booting process

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

## Links

https://forum.doozan.com/read.php?2,131833

https://github.com/benoitm974/ix4-300d/wiki

https://github.com/5p0ng3b0b/ix4-300d
