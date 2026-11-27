# Points hors plan du chantier « espace-projet » — à rappeler en fin de chantier

Liste tenue par la session principale. Elle regroupe ce qui est écarté du plan, laissé en l'état
ou relevé sans suite, avec sa source. À présenter à l'utilisateur à la fin du plan (PA-E17), pour
décision : traiter, garder hors plan, ou abandonner. Toute session qui écarte un point l'ajoute
ici. Choix entre hors plan et ticket : règle en tête de `doc/devenv/HORS-PLAN.md`.

| ID | Point | Source | Suite |
| --- | --- | --- | --- |
| H1 | J-Link : validation différée, sur une autre carte, avec un projet et un BSP spécifiques. Le schéma garde `jlink` ; ce que `generate` émet pour `jlink` se décide au PA-E10 (T6). | `CADRAGE.md` §5 C9 | hors plan (décision de l'utilisateur du 2026-11-25) |
| H2 | Résidu `sys/user/tauon-basic/` du noyau après EP-3 (36 fichiers suivis attendus), présent dans le trunk à côté de `sys/user/lepton-basic/`. Option (ii) : déplacer le jeu Olimex du test hôte de mklepton sous `tests/host/` et supprimer le résidu. | `CADRAGE.md` §5 C7 | hors plan, « pour plus tard » (décision de l'utilisateur du 2026-11-25) |
| H3 | Graine de projet multi-BSP et multi-backend ; conversion de la graine de référence `original-tree` en graine de projet. | `CADRAGE.md` §5 C8 | hors chantier (décision de l'utilisateur du 2026-11-25) |
| H4 | Publication de l'extension Lepton sur Open VSX. | A4 de `doc/devenv/HORS-PLAN.md` ; `CADRAGE.md` §9 point 4 | hors plan (décision de l'utilisateur du 2026-11-25) |
| H5 | Fichiers de `sys/user/tauon-basic` non repris dans `lepton-basic` : `etc/.boot`, `etc/.init`, `etc/.mount`, les 5 variantes `.init_*`, `src/bin/*`, les 7 `user_kernel_mkconf.h`. | `CADRAGE.md` §5 C6 ; A3 de `doc/devenv/HORS-PLAN.md` | hors plan, comme A3 (décision de l'utilisateur du 2026-11-25) |
| H6 | QEMU lancé par Cortex-Debug (configurations `servertype: qemu` générées par `lepton generate`) écoute le port gdb sur toutes les interfaces (`-gdb "tcp::50000"`, `lsof` : `TCP *:50000 (LISTEN)`) ; une écoute restreinte à `localhost` n'est ni demandée ni essayée. | EP-0, `rapports/ep-0-essai-lien.md` §5 | hors plan (décision de l'utilisateur du 2026-11-26, PA-E1) |
| H7 | Graines à l'ancien format (`project/` dans le dépôt de la graine), refusées par lepton 0.2.0 et non migrées : Mac `essais/env-9` (`env9`), `essais/env-11/{qemu,qemu-gra2,f429zi,wl55jc1,bout-en-bout/rootstock}`, `essais/env-72-essai/{c4,c4d}/{rs,M}` ; VM `essais/env-53-c5` (`env11`, sort décidé en EP-8). Procédure manuelle au `README.md`. | EP-1, `rapports/ep-1-type-projet.md` §1.6 | abandonnées (décision de l'utilisateur du 2026-11-27, PA-E2) |
| H8 | `files.exclude` de l'espace garde `project/scion` (ancien format), sans effet depuis lepton 0.2.0 ; retrait laissé à EP-4 pour ne pas changer l'espace de la graine de référence en EP-1. | EP-1, `rapports/ep-1-type-projet.md` §3.4 | EP-4 (décision de l'utilisateur du 2026-11-27, PA-E2) |
