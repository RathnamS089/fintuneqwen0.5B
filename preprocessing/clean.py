import json,re,pathlib,hashlib
from bs4 import BeautifulSoup

RAW=pathlib.Path("../data/raw/stackoverflow_js.jsonl")
OUT=pathlib.Path("../data/clean/stackoverflow_isclean.jsonl")
OUT.parent.mkdir(exist_ok=True,parents=True)

def html_to_md(html_str:str)->str:
    if not html_str: return ""
    soup=BeautifulSoup(html_str,"lxml")
    for pre in soup.find_all("pre"):
        code=pre.get_text()
        pre.replace_with(f"\n```javascript\n{code.strip()}\n```\n")
    for code in soup.find_all("code"):
        if code.parent.name=="pre":continue
        code.replace_with(f"`{code.get_text()}`")
    for a in soup.find_all("a"):
        a.replace_with(f"{a.get_text()}({a.get('href','')})")
    text=soup.get_text(separator="\n")
    text=re.sub(r"\n{3,}","\n\n",text)
    text = re.sub(r"\+\+", "+", text)
    return text.strip()

def is_useful(rec)->bool:
    if not rec.get("question"):return False
    if not rec.get("answers"): return False
    if not any(a.get("score",0)>=2 or a.get("is_accepted") for a in rec["answers"]):
        return False
    if len(rec["question"])<30: return False
    if len(rec["answers"][0].get("body",""))<20: return False
    return True

def dedupe_key(rec):
    return hashlib.md5((rec["title"]+rec["question"][:200]).encode()).hexdigest()

seen=set()
kept=0
with open(RAW,encoding="utf-8") as fin, open(OUT,"w",encoding="utf-8") as fout:
    for line in fin:
        try:
            rec=json.loads(line)
        except:continue
        if not is_useful(rec): continue
        k=dedupe_key(rec)
        if k in seen: continue
        seen.add(k)
        rec["question"]=html_to_md(rec["question"])
        for a in rec["answers"]:
            a["body"]=html_to_md(a.get("body",""))
        if not rec["question"] or not rec["answers"][0]["body"]:
            continue
        fout.write(json.dumps(rec,ensure_ascii=False)+"\n")
        kept+=1
print(f"Cleaned:{kept} records -> {OUT}")