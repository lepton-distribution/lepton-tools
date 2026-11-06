import re,sys
def corps(path,name):
    t=open(path,encoding='latin-1').read().replace('\r','')
    m=re.search(r'(__STATIC_(FORCE)?INLINE|__attribute__\(\(always_inline\)\) __STATIC_INLINE)[^;{]*\b'+re.escape(name)+r'\s*\([^)]*\)\s*\{',t)
    if not m: return None
    i=m.end(); d=1
    while d: 
        d+= {'{':1,'}':-1}.get(t[i],0); i+=1
    b=t[m.start():i]
    b=re.sub(r'/\*.*?\*/','',b,flags=re.S); b=re.sub(r'//.*','',b)
    return re.sub(r'\s+',' ',b)
v3=[sys.argv[1]+'/'+f for f in ('core_cm4.h','core_cmFunc.h','core_cmInstr.h')]
v5=[sys.argv[2]+'/'+f for f in ('core_cm4.h','cmsis_gcc.h')]
for n in sys.argv[3:]:
    a=next((x for x in (corps(p,n) for p in v3) if x),None); b=next((x for x in (corps(p,n) for p in v5) if x),None)
    print(f"### {n}\n  V3.30 : {a}\n  5.9.0 : {b}")
