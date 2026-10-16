# Essai O10 (reprise 4) : clangd recharge-t-il une base apparue après son démarrage ?
# Usage : python3 -I env-9-r4-essai-clangd.py DIR SECONDES ; DIR contient src/main.c, src/def.c,
# inc/def.h et un cdb/ vide (voir env-9-r4.md §3). Résultat : non, avant une modification du fichier.
import json, subprocess, sys, time, threading, os, shutil
S=sys.argv[1]; mode=sys.argv[2]
p=subprocess.Popen(["/opt/local/bin/clangd-mp-21",f"--compile-commands-dir={S}/cdb","--background-index","--log=error"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
msgs=[];
def rd():
    while True:
        h=b""
        while not h.endswith(b"\r\n\r\n"):
            c=p.stdout.read(1)
            if not c: return
            h+=c
        n=int([l for l in h.split(b"\r\n") if l.lower().startswith(b"content-length")][0].split(b":")[1])
        msgs.append(json.loads(p.stdout.read(n)))
threading.Thread(target=rd,daemon=True).start()
i=[0]
def send(m,params,notif=False):
    d={"jsonrpc":"2.0","method":m,"params":params}
    if not notif: i[0]+=1; d["id"]=i[0]
    b=json.dumps(d).encode(); p.stdin.write(b"Content-Length: %d\r\n\r\n"%len(b)+b); p.stdin.flush(); return d.get("id")
def wait(id,t=20):
    e=time.time()+t
    while time.time()<e:
        for m in msgs:
            if m.get("id")==id: return m
        time.sleep(0.2)
send("initialize",{"processId":None,"rootUri":f"file://{S}","capabilities":{}}); time.sleep(1)
send("initialized",{},True)
uri=f"file://{S}/src/main.c"
send("textDocument/didOpen",{"textDocument":{"uri":uri,"languageId":"c","version":1,"text":open(f"{S}/src/main.c").read()}},True)
time.sleep(3)
def defn():
    r=wait(send("textDocument/definition",{"textDocument":{"uri":uri},"position":{"line":1,"character":24}}))
    return [x["uri"].split("/",3)[-1] for x in (r or {}).get("result") or []]
print("avant base :",defn())
cdb=[{"directory":S,"file":f"{S}/src/{f}","arguments":["cc","-I",f"{S}/inc","-c",f"src/{f}"]} for f in ("main.c","def.c")]
json.dump(cdb,open(f"{S}/cdb/compile_commands.json","w"))
time.sleep(int(mode))
print(f"base écrite, +{mode}s :",defn())
send("textDocument/didChange",{"textDocument":{"uri":uri,"version":2},"contentChanges":[{"text":open(f"{S}/src/main.c").read()+"\n"}]},True); time.sleep(5)
print("après modification du fichier :",defn())
p.kill()
