import json,pathlib,random
IN=pathlib.Path("../data/clean/stackoverflow_isclean.jsonl")
OUT=pathlib.Path("../data/processed/js_soup_train.jsonl")
OUT.parent.mkdir(parents=True,exist_ok=True)
TEMPLATE_INSTRUCTION="You are a Javascript expert.Answer the question,explain the concept, and provide corrected code if needed"
def to_alpaca(rec):
    title=rec["title"]
    question=rec["question"]
    best=rec["answers"][0]
    answer=best["body"]
    instruction=f"{TEMPLATE_INSTRUCTION}\n\nQuestion:{title}"
    inp=question
    output=answer
    if len(answer) > 0:
        output=output[:4000]
    return{
        "instruction":instruction,
        "input":inp,
        "output":output,
        "tags":rec.get("tags",[]),
        "url":rec.get("url","")
    }
random.seed(42)
records=[]
with open(IN,encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))
    
random.shuffle(records)
alpaca=[to_alpaca(r) for r in records]
with open(OUT,"w",encoding="utf-8") as out:
    for ex in alpaca:
        out.write(json.dumps(ex,ensure_ascii=False)+"\n")
print(f"SOUP dataset:{len(alpaca)} examples ->{OUT}")
print(f"Example:\n",json.dumps(alpaca[0],indent=2)[:800])
