#!/bin/bash
# author: Sean O'Haver
# description: Automating the fixes required to compile the broadcom wifi
#              drivers in CentOS 7
# documentation: https://wiki.centos.org/HowTos/Laptops/Wireless/Broadcom

check_rv()
{
  # $1 = return value; $2 = command run
  if [ "$1" -ne 0 ]; then
    echo "${2} return ${1}. Exiting"
    exit $1
  fi
}


# STATIC VARIABLES - Begin
blacklist_conf=/etc/modprobe.d/blacklist.conf
destdir=/usr/local/src/hybrid-wl
bcom_driver=~/Downloads/hybrid*.tar.gz
kmodwl_modules="#!/bin/bash\n\n
for M in lib80211 cfg80211 wl; do\n
modprobe $M &>/dev/null\n
done\n"
patch_file=wl-kmod-kernel_4.7_IEEE80211_BAND_to_NL80211_BAND.patch
# STATIC VARIABLES - End


if [ "$(whoami)" != "root" ]; then
  echo "Must be run as sudo/root, exiting"
  exit 2
fi

if [ ! -e "${bcom_driver}" ]; then
  model_num=$(/sbin/lspci | grep Broadcom | grep 802 | awk '{ print $6 }')
  echo -e "Download the Broadcom BCM43xx linux driver archive from Broadcom Official website - you'll find it as in the search results list as either Linux® STA 32-bit driver or Linux® STA 64-bit driver - to your machine and extract it to /usr/local/src/hybrid-wl and feel free to change the ownership of the directory and it's contents to some unprivileged user\n\nhttps://www.broadcom.com//site-search?q=${model_num}+sta+wl\n\nModel Number: ${model_num}"
  exit 3
fi

broadcom_devices=$(/sbin/lspci | grep Broadcom)
echo $broadcom_devices


if [ -n "$(/sbin/lspci | grep Broadcom | grep 802 | awk '{ print $1 }')" ]; then
  yum install -y kernel-headers kernel-devel gcc
  cd ~/Downloads
  wget -O wl-kmod-kernel_4.7_IEEE80211_BAND_to_NL80211_BAND.patch "https://wiki.centos.org/HowTos/Laptops/Wireless/Broadcom?action=AttachFile&do=get&target=wl-kmod-kernel_4.7_IEEE80211_BAND_to_NL80211_BAND.patch"
  mkdir -p ${destdir}
  cd ${destdir}
  tar -xzvf ${bcom_driver}
  chown -R ${USER}.wheel ${destdir}
  make -C /lib/modules/`uname -r`/build/ M=`pwd`
  echo "This should error and this is fine."
  sleep 7
  cp ~/Downloads/${patch_file} .
  patch -p1 < ${patch_file}
  sed -i 's/ >= KERNEL_VERSION(3, 11, 0)/ >= KERNEL_VERSION(3, 10, 0)/' src/wl/sys/wl_cfg80211_hybrid.c
  sed -i 's/ >= KERNEL_VERSION(3, 15, 0)/ >= KERNEL_VERSION(3, 10, 0)/' src/wl/sys/wl_cfg80211_hybrid.c
  sed -i 's/ < KERNEL_VERSION(3, 18, 0)/ < KERNEL_VERSION(3, 9, 0)/' src/wl/sys/wl_cfg80211_hybrid.c
  sed -i 's/ >= KERNEL_VERSION(4, 0, 0)/ >= KERNEL_VERSION(3, 10, 0)/' src/wl/sys/wl_cfg80211_hybrid.c
  sed -i 's/ < KERNEL_VERSION(4,2,0)/ < KERNEL_VERSION(3, 9, 0)/' src/wl/sys/wl_cfg80211_hybrid.c
  sed -i 's/ >= KERNEL_VERSION(4, 7, 0)/ >= KERNEL_VERSION(3, 10, 0)/' src/wl/sys/wl_cfg80211_hybrid.c
  make -C /lib/modules/`uname -r`/build/ M=`pwd`
  strip --strip-debug wl.ko

  if [ ! -e "${blacklist_conf}" ]; then
    touch ${blacklist_conf}
  fi
  for i in bcm43xx b43 b43legacy ssb bcma brcmsmac ndiswrapper; do
    modprobe -r ${i}
    echo "blacklist ${j}" | sudo tee -a ${blacklist_conf}
    sleep 1
  done

  cp -vi /usr/local/src/hybrid-wl/wl.ko /lib/modules/`uname -r`/extra/

  depmod $(uname -r)

  modprobe wl
  sleep 3

  if [ -f ~/Downloads/kmod-wl.modules ]; then
    cp ~/Downloads/kmod-wl.modules /etc/sysconfig/modules/
  else
    echo $kmodwl_modules > /etc/sysconfig/modules/kmod-wl.modules
  fi
fi
