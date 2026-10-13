# ENV-6 — Validation (non-régression des extractions)

## Commandes

Oracle : `scripts/oracle/rejouer-oracle.sh` (lepton-tools), constructions neuves. Le script attend un
drapeau par preset ; la forme à accolades de `env-5-validation.md` (`--qemu a b c`) est refusée
(« argument inconnu ») : la liste est construite ainsi.

```
args=()
for p in qemu-mps2-an386-{embos,embos-soft,freertos,freertos-soft} qemu-mps2-an500-{embos,freertos}; do args+=(--qemu $p); done
for p in nucleo-f439zi-{embos,freertos} nucleo-wl55jc1-{embos,freertos} stm32f746g-disco-{embos,freertos} samd21-xplained-pro-{embos,freertos}; do args+=(--carte $p); done
scripts/oracle/rejouer-oracle.sh ~/lepton doc/devenv/rapports/oracles/env-6-<avant|lot-…> "${args[@]}"
```

## Oracle avant (`oracles/env-6-avant/`, clone noyau 1551afb = fusion de e564714)

Comparaison avec `oracles/env-5-apres/` (même code) : `comparer-oracle.py` code 0 sur les 14 presets
(sections et symboles identiques) ; host : ctest 7/7, empreintes mklepton identiques à la référence.

| Preset | Sections/symboles | Empreinte | Fumée | Banc KAL | Écarts expliqués |
| --- | --- | --- | --- | --- | --- |
| qemu-mps2-an386-embos | code 0 | différente | identique | 18/18, même liste | date |
| qemu-mps2-an386-embos-soft | code 0 | différente | identique | 14/14, même liste | date |
| qemu-mps2-an386-freertos | code 0 | différente | identique | 18/18, même liste | date |
| qemu-mps2-an386-freertos-soft | code 0 | différente | identique | 14/14, même liste | date |
| qemu-mps2-an500-embos | code 0 | différente | identique | 18/18, même liste | date |
| qemu-mps2-an500-freertos | code 0 | différente | identique | 18/18, même liste | date |
| nucleo-f439zi-embos, -freertos | code 0 | différente | – | – | date |
| nucleo-wl55jc1-embos, -freertos | code 0 | différente | – | – | date |
| stm32f746g-disco-embos, -freertos | code 0 | différente | – | – | date |
| samd21-xplained-pro-embos, -freertos | code 0 | différente | – | – | date |

Écarts ignorés dans les journaux de fumée : date de compilation (`__DATE__`/`__TIME__` de
`kernel.c`), jeton aléatoire du test UART1 (`lepton-uart1-<n>`), position du message asynchrone
`rcv SIGCHLD` (avant ou après l'invite suivante). Banc KAL : lignes de résultat identiques, durées
ignorées.
