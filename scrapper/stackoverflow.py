import time,json,html,pathlib,requests
from tqdm import tqdm

API_ROOT="https://api.stackexchange.com/2.3"
SITE="stackoverflow"
TAG="javascript"
PAGE_SIZE=50
TARGET=1000
OUT=pathlib.Path("../data/raw/stackoverflow_js.jsonl")
OUT.parent.mkdir(parents=True,exist_ok=True)

FILTER="withbody"

def api_get(url,params,retries=3):
    for attempt in range(retries):
        r=requests.get(url,params=params,timeout=30)
        data=r.json()
        if "backoff" in data:
            wait=int(data["backoff"])+1
            print(f"[backoff] sleeping {wait}s")
            time.sleep(wait)
        if r.status_code==429 or "error_id" in data and data.get('error_id')==502:
            time.sleep(2**(attempt+1))
            continue
        r.raise_for_status()
        if "error_id" in data:
            raise RuntimeError(f"API error {data}")
        return data
    raise RuntimeError("Max retries exceeded")

def collect():
    seen=set()
    if OUT.exists():
        with open(OUT) as f:
            for line in f:
                try:
                     seen.add(json.loads(line)["question_id"])
                except :pass
            print(f"Resuming:{len(seen)} already saved")
            
    collected=len(seen)
    page=1
    has_more=True
    pbar=tqdm(total=TARGET,initial=collected)
    with open(OUT,"a",encoding="utf-8") as out_f:
        while has_more and collected<TARGET:
            params={
                "site":SITE,
                "tagged":TAG,
                "sort":"votes",
                "order":"desc",
                "pagesize":PAGE_SIZE,
                "page":page,
                "filter":FILTER,
                "answers":1
            }
            data=api_get(f"{API_ROOT}/questions",params)
            items=data.get("items",[])
            if not items:
                break
            q_ids=[str(q["question_id"]) for q in items if q["question_id"] not in seen]
            ans_map={}
            if q_ids:
                for i in range(0,len(q_ids),20):
                    chunk=";".join(q_ids[i:i+20])
                    ans_data=api_get(f'{API_ROOT}/questions/{chunk}/answers',{"site": SITE, "sort": "votes", "order": "desc", "filter": FILTER, "pagesize": 100})
                    for a in ans_data.get("items",[]):
                        ans_map.setdefault(a["question_id"],[]).append({
                            "body":a.get("body",""),
                            "score":a.get("score",0),
                            "is_accepted":a.get("is_accepted",False)
                        })
                    time.sleep(0.2)
                    
            for q in items:
                q_id=q["question_id"]
                if q_id in seen:
                    continue
                ans=ans_map.get(q_id,[])
                if not ans:
                    continue
                ans.sort(key=lambda x:(x["is_accepted"],x["score"]),reverse=True)
                record={
                    "question_id":q_id,
                    "title":html.unescape(q.get("title","")),
                    "question": q.get("body",""),
                    "answers": ans,
                    "tags": q.get("tags", []),
                    "score": q.get("score",0),
                    "url": q.get("link", f"https://stackoverflow.com/q/{q_id}"),
                    "is_answered": q.get("is_answered", False),
                    "answer_count": q.get("answer_count",0),
                }
                out_f.write(json.dumps(record,ensure_ascii=False)+"\n")
                out_f.flush()
                seen.add(q_id)
                collected += 1
                pbar.update(1)
                if collected>=TARGET:
                    break
            has_more = data.get("has_more", False)
            if data.get("quota_remaining", 9999) < 10:
                print("Quota low, stopping")
                break
            page+=1
            time.sleep(0.5)
    pbar.close()
    print(f"Done:{collected} saved to {OUT}")

if __name__=="__main__":
    collect()