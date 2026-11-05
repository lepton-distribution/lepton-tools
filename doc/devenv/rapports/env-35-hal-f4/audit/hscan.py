import json,sys,shlex,subprocess,re
from concurrent.futures import ThreadPoolExecutor
B,out=sys.argv[1:3]
cc=json.load(open(B+'/compile_commands.json'))
pre='/Users/cle_d_anton/lepton/trunk/sys/root/src/'
def run(e):
    a=shlex.split(e['command']); i=a.index('-o'); del a[i:i+2]
    a=[x for x in a if x!='-c']; a[1:1]=['-fsyntax-only','-H']
    r=subprocess.run(a,cwd=e['directory'],capture_output=True,text=True)
    hs=[l.split(' ',1)[1].replace(pre,'') for l in r.stderr.splitlines() if re.match(r'^\.+ ',l)]
    st=[h for h in hs if re.search(r'stm32|core_cm|system_stm',h,re.I)]
    return e['file'].replace(pre,''),r.returncode,st
with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,cc))
with open(out,'w') as f:
    for fi,rc,st in sorted(res):
        f.write(f"{fi}\trc={rc}\tnST={len(st)}\t{st[0] if st else '-'}\n")
