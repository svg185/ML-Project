import os,json,datetime
from ml_intent import NaiveBayesIntentClassifier,load_dataset
from planner import make_plan
from security import needs_confirmation,validate
from mcp_server import LocalMCPServer
BASE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(BASE,'data','intents.csv'); SANDBOX=os.path.join(BASE,'sandbox'); LOG=os.path.join(BASE,'logs','actions.log')
def log(e):
    os.makedirs(os.path.dirname(LOG),exist_ok=True)
    with open(LOG,'a',encoding='utf-8') as f: f.write(json.dumps({'time':datetime.datetime.now().isoformat(timespec='seconds'),**e})+'\n')
def main():
    os.makedirs(SANDBOX,exist_ok=True)
    demo=os.path.join(SANDBOX,'sample_report.pdf')
    if not os.path.exists(demo): open(demo,'w').write('Demo placeholder file.\n')
    clf=NaiveBayesIntentClassifier(); clf.fit(load_dataset(DATA)); server=LocalMCPServer(SANDBOX)
    print('\n'+'='*72+'\n AI-POWERED LOCAL COMPUTER AUTOMATION — PHASE 1\n ML Intent Classification | MCP-style Tools | Safe Local Demo\n'+'='*72)
    print("Type 'help' for examples or 'exit' to quit.\n")
    while True:
        try: c=input('YOU > ').strip()
        except (EOFError,KeyboardInterrupt): break
        if not c: continue
        if c.lower() in ('exit','quit'): print('AI  > Session ended.'); break
        if c.lower()=='help': print('Examples:\n  create a folder named ML Project\n  list files\n  find pdf files\n  search for report\n  open calculator\n  open notepad\n  delete sample_report.pdf\n'); continue
        intent,conf=clf.predict(c); plan=make_plan(intent,c)
        print(f'\nAI  > Detected intent : {intent}\nAI  > ML confidence   : {conf:.2f}\nAI  > Action plan     : {json.dumps(plan)}')
        ok,msg=validate(plan,server.tools)
        if not ok: print('SAFE> BLOCKED —',msg); log({'command':c,'status':'blocked'}); continue
        for step in plan:
            tool=step['tool']
            if needs_confirmation(tool):
                if input(f"SAFE> '{tool}' requires confirmation. Continue? [y/N]: ").strip().lower()!='y': print('SAFE> Cancelled.'); log({'command':c,'tool':tool,'status':'cancelled'}); continue
            r=server.invoke(tool,step['arguments']); print('TOOL>',tool); print('RESULT>',r['message'])
            for item in r.get('items',[])[:20]: print('  -',item)
            log({'command':c,'intent':intent,'tool':tool,'status':'success' if r['ok'] else 'failed'})
        print()
if __name__=='__main__': main()
