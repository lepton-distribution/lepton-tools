import json,sys,shlex,subprocess,re
B,S,variant=sys.argv[1:4]
T='/Users/cle_d_anton/lepton/trunk/sys/root/src'
FAM=T+'/kernel/dev/arch/cortexm/stm32f4xx'
HALI=FAM+'/hal_driver/Inc'; DEV=T+'/kernel/core/ucore/cmsis-5/Device/ST/STM32F4xx/Include'
C5=T+'/kernel/core/ucore/cmsis-5/CMSIS/Core/Include'
cc={e['file']:e for e in json.load(open(B+'/compile_commands.json'))}
ref=cc[FAM+'/gpio.c']
base=shlex.split(ref['command']); i=base.index('-o'); del base[i:i+2]
base=[x for x in base if x not in ('-c',ref['file'])]
def flags():
    a=list(base)
    if variant=='apres':   # inclusions HAL ajoutées après celles de la famille (ordre actuel du lecteur)
        j=a.index('-I'+FAM+'/dev_stm32f4xx')+1
        a[j:j]=['-I'+HALI,'-I'+DEV]
    elif variant=='avant': # inclusions HAL avant driverlib
        j=a.index('-I'+FAM+'/driverlib')
        a[j:j]=['-I'+HALI,'-I'+DEV]
    a+=['-DUSE_HAL_DRIVER','-I'+S+'/coex/conf']
    return a
files={'hal_gpio':FAM+'/hal_driver/Src/stm32f4xx_hal_gpio.c','hal_rcc':FAM+'/hal_driver/Src/stm32f4xx_hal_rcc.c',
 'hal_cortex':FAM+'/hal_driver/Src/stm32f4xx_hal_cortex.c','hal_eth':FAM+'/hal_driver/Src/stm32f4xx_hal_eth.c',
 'spl_gpio':FAM+'/driverlib/stm32f4xx_gpio.c','spl_eth':FAM+'/driverlib/stm32f4x7_eth.c',
 'lep_gpio':FAM+'/gpio.c','lep_uart':FAM+'/uart.c','lep_eth':FAM+'/eth.c'}
for k,f in files.items():
    r=subprocess.run(flags()+['-fsyntax-only','-H',f],cwd=ref['directory'],capture_output=True,text=True)
    hs=[l.split(' ',1)[1] for l in r.stderr.splitlines() if re.match(r'^\.+ ',l)]
    pick=lambda n:[h.replace(T+'/','') for h in hs if h.endswith('/'+n)][:1]
    errs=[l for l in r.stderr.splitlines() if 'error' in l]
    warns=[l for l in r.stderr.splitlines() if 'warning' in l]
    print(f"{variant}\t{k}\trc={r.returncode}\terr={len(errs)}\twarn={len(warns)}\t{pick('stm32f4xx.h')}\t{pick('stm32f429xx.h')}\t{pick('core_cm4.h')}")
    open(f'{S}/coex/{variant}-{k}.log','w').write(r.stderr)
