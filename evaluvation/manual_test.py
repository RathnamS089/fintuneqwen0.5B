import argparse, json, pathlib
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
PROMPTS = [
    "Explain closures in JavaScript with an example.",
    "Why does typeof null return \"object\"?",
    "Debug this Array.map bug:\n[1,2,3].map(parseInt) // returns [1, NaN, NaN] why?",
    "Explain async/await in JavaScript.",
    "Explain the event loop in JavaScript.",
    "Write a JS function to group objects by property: groupBy([{a:1},{a:1},{a:2}], 'a')",
    "Fix promise-handling bug:\nfetch(url).then(data=>console.log(data)) // data is Response not JSON",
    "Explain let, const, var differences.",
    "Explain prototype inheritance in JavaScript.",
    "Refactor var+callback to modern ES6+:\nvar self=this; setTimeout(function(){self.do()},100)",
]
def load_model(base, adapter=None):
    tok = AutoTokenizer.from_pretrained(base, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(base, device_map="auto", load_in_4bit=False, trust_remote_code=True)
    if adapter and pathlib.Path(adapter).exists():
        model = PeftModel.from_pretrained(model, adapter)
        print(f"Loaded adapter {adapter}")
    tok.pad_token = tok.eos_token
    return tok, model

def generate(tok, model, prompt, max_new=256):
    inp = tok(f"Instruction: {prompt}\nAnswer:", return_tensors="pt").to(model.device)
    out = model.generate(**inp, max_new_tokens=max_new, temperature=0.7, do_sample=False)
    return tok.decode(out[0], skip_special_tokens=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--out", default="evaluation/results.jsonl")
    args = ap.parse_args()

    tok, model = load_model(args.base, args.adapter)
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out,"w") as f:
        for p in PROMPTS:
            print("\n===", p[:60])
            ans = generate(tok, model, p)
            print(ans[:500])
            f.write(json.dumps({"prompt": p, "output": ans}, ensure_ascii=False)+"\n")
    print(f"Saved -> {args.out}")