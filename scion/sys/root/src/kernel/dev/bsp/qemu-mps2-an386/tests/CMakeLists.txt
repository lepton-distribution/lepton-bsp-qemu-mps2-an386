# Tests du BSP qemu-mps2-an386 (TST-2, PA-41 d'ENV-27) : répertoire désigné par le champ « tests »
# du manifeste, ajouté par lepton_greffons_tests (lepton_greffons.cmake du greffon noyau) quand
# LEPTON_BOARD=qemu-mps2-an386. Nom préfixé « qemu-mps2-an386. », étiquettes greffon:, arch:,
# backend: ajoutées par lepton_greffon_test.
#
# peripheriques : les périphériques du BSP (UART CMSDK ttys0 et ttys1, Ethernet LAN9118 eth0) sont
# présents dans /dev. Après la fumée canonique (fixture kal_t0).
if(LEPTON_QEMU_MACHINE)
  lepton_greffon_test(NAME peripheriques
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/peripheriques.py
            --tests-noyau ${LEPTON_TESTS_NOYAU}
            --qemu ${LEPTON_QEMU_ARM} --machine ${LEPTON_QEMU_MACHINE} --kernel $<TARGET_FILE:lepton>
            --expect ttys0 --expect ttys1 --expect eth0
            --log ${CMAKE_CURRENT_BINARY_DIR}/peripheriques.log
    LABELS qemu
    PROPERTIES TIMEOUT 120 FIXTURES_REQUIRED kal_t0 ENVIRONMENT PYTHONDONTWRITEBYTECODE=1)
endif()
