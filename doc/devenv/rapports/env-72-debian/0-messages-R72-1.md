# Messages R72-1 non remis (VM → Mac)

## AVANCEMENT §10 — non remis (ECONNRESET ×2, 2026-11-24 ~15:5x UTC)

[AVANCEMENT R72-1] ENV-72 — §10 terminé : deux code=0 ; écarts=15 / 165 et 2 / 244 ; un écart hors des classes listées, relevé sans arrêt (§10).

- chemins.sh : code=0, 165 relevés. graine.sh : code=0, 244 relevés. Les deux scripts sont passés par le classifieur, sans refus.
- resume.tsv, colonnes 1 à 6 = Mac. Liens de c4/rs : liens=3059 casses=0 reguliers=0.

c4-chemins, écarts=15 / 165 (Mac : 13 / 165), tous dans les classes listées :
- hôte : p6-n.cmd, p6-n.clangd (clangd, /usr/bin/clangd) ;
- longueur des chemins : resume.tsv, colonne 7 tronquée (m1-h, m1-th, p6-*) ;
- fichiers ignorés du Mac : n1-a, n1-d, n1-r, n1-t, n1-u .err (ligne « 13 chemin(s) ignoré(s) » absente) ;
- graine env11 : 7 fichiers p6-{a,n,r,rd,rs,rw,t}.out (« presets : env11-debug-qemu » seul).

c4-graine, écarts=2 / 244 : g1-status.out et r1-status.out.
- Dans les classes listées : graine branch/commit main 124db52 → master 6d3d2a5 (graine et projet) ; preset release-qemu absent ; r1 : commit de library-env68lib f6aed02 → 98ec8ea (commits locaux).
- HORS des classes listées : "location" des clones noyau, family-qemu-mps2 et bsp-qemu-mps2-an386 :
  « https://github.com/lepton-distribution/<dépôt>.git » au Mac, « ssh://git@github.com/lepton-distribution/<dépôt>.git » sur la VM.
  Cause : dans $C5 (état d'origine de la VM), l'origin des clones est en ssh. git -C $C5/depots/lepton/original/master remote get-url origin → ssh://git@github.com/lepton-distribution/lepton-original-tree.scions.git.
  Classe nouvelle (D37 date d'ENV-68, R66-1 ne pouvait pas la voir) : URL d'origine des clones de $C5. C'est un défaut de la consigne selon D38 (3), consigné au rapport.

Je passe au §11.1 : git clone de seed.scions (règle allow), puis les 4 fixtures.
