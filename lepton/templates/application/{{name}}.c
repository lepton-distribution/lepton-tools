/*
 * Application {{name}} — fichier exemple créé par lepton scion new.
 * Point d'entrée : {{c_name}}_main, à déclarer dans le XML mklepton du projet
 * (<binaries> : <bin name="{{c_name}}" … />).
 */
#include "kernel/core/libstd.h"
#include "lib/libc/stdio/stdio.h"

int {{c_name}}_main(int argc, char* argv[])
{
   (void)argc;
   (void)argv;
   printf("{{name}}\r\n");
   return 0;
}
