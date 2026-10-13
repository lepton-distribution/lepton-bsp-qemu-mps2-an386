# BSP qemu-mps2-an386 : paramètres hors manifeste (PA-7 Q3), inclus par le CMakeLists.txt racine
# du greffon noyau quand LEPTON_BOARD=qemu-mps2-an386. XML mklepton : LEPTON_MKCONF du preset.
set(LEPTON_NET_STACK lwip)   # USE_LWIP dans include/user_kernel_mkconf.h
set(LEPTON_BOARD_UNAME_MACHINE cortexM4-qemu-mps2-an386)   # __KERNEL_CPU_DEVICE_NAME (test de fumée)
# test réseau (label net, tests/net_qemu.py) : adresses du .init commun aux machines MPS2, fichier
# téléchargé par FTP et sa source dans l'arbre
set(LEPTON_NET_TEST_HOST_IP 192.168.100.1)
set(LEPTON_NET_TEST_GUEST_IP 192.168.100.2)
set(LEPTON_NET_TEST_FTP_FILE /usr/etc/.boot)
set(LEPTON_NET_TEST_FTP_REFERENCE sys/user/tauon-basic/etc/qemu-mps2/.boot)
