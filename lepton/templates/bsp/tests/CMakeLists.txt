# Tests du BSP {{name}} — squelette créé par lepton scion new (TST-2).
# Répertoire désigné par le champ « tests » du manifeste : ajouté par lepton_greffons_tests (lecteur
# des manifestes du greffon noyau) quand LEPTON_BOARD={{name}}.
# lepton_greffon_test : test « {{name}}.<NAME> », étiquettes greffon:{{name}}, arch:<cœur> et
# backend:<micro-noyau> ajoutées ; sélection : ctest --preset <P> -L greffon:{{name}}.
# Variables : LEPTON_TESTS_NOYAU (scripts du noyau : smoke_lsh.py), LEPTON_QEMU_MACHINE,
# LEPTON_QEMU_ARM, LEPTON_BOARD_SERIAL_PORT, LEPTON_OPENOCD, LEPTON_BOARD_OPENOCD_CFG,
# LEPTON_BOARD_UNAME_MACHINE, Python3_EXECUTABLE.
#
# peripheriques : « ls /dev » répond sans message d'erreur ; à remplacer par les contrôles propres
# à la carte (périphériques attendus, pilotes).
if(LEPTON_QEMU_MACHINE)
  lepton_greffon_test(NAME peripheriques
    COMMAND ${Python3_EXECUTABLE} ${LEPTON_TESTS_NOYAU}/smoke_lsh.py
            --qemu ${LEPTON_QEMU_ARM} --machine ${LEPTON_QEMU_MACHINE} --kernel $<TARGET_FILE:lepton>
            --expect-machine ${LEPTON_BOARD_UNAME_MACHINE} --command "ls /dev"
            --log ${CMAKE_CURRENT_BINARY_DIR}/peripheriques.log
    LABELS qemu
    PROPERTIES TIMEOUT 120 FIXTURES_REQUIRED kal_t0 ENVIRONMENT PYTHONDONTWRITEBYTECODE=1)
elseif(LEPTON_BOARD_SERIAL_PORT AND LEPTON_OPENOCD)
  lepton_greffon_test(NAME peripheriques
    COMMAND ${Python3_EXECUTABLE} ${LEPTON_TESTS_NOYAU}/smoke_lsh.py
            --transport serial --port ${LEPTON_BOARD_SERIAL_PORT}
            --reset-command "${LEPTON_OPENOCD} -f ${LEPTON_BOARD_OPENOCD_CFG} -c \"program $<TARGET_FILE:lepton> verify reset exit\""
            --expect-machine ${LEPTON_BOARD_UNAME_MACHINE} --command "ls /dev"
            --log ${CMAKE_CURRENT_BINARY_DIR}/peripheriques.log
    LABELS board
    PROPERTIES TIMEOUT 120 RUN_SERIAL TRUE FIXTURES_REQUIRED board_t0 ENVIRONMENT PYTHONDONTWRITEBYTECODE=1)
endif()
