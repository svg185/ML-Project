import os, subprocess, platform
class LocalMCPServer:
    def __init__(self,sandbox):
        self.sandbox=os.path.abspath(sandbox); os.makedirs(self.sandbox,exist_ok=True)
        self.tools={'create_folder':self.create_folder,'list_files':self.list_files,'search_files':self.search_files,'open_application':self.open_application,'delete_file':self.delete_file}
    def create_folder(self,name):
        safe=os.path.basename(name).strip()
        if not safe or safe in ('.','..'): return {'ok':False,'message':'Invalid folder name.'}
        p=os.path.join(self.sandbox,safe); os.makedirs(p,exist_ok=True); return {'ok':True,'message':f'Folder created: {p}'}
    def list_files(self):
        x=os.listdir(self.sandbox); return {'ok':True,'items':x,'message':f'{len(x)} item(s) in sandbox.'}
    def search_files(self,query):
        q=query.lower().strip(); out=[]
        for base,_,names in os.walk(self.sandbox):
            for n in names:
                if q in n.lower(): out.append(os.path.join(base,n))
        return {'ok':True,'items':out,'message':f'{len(out)} match(es).'}
    def open_application(self,app):
        if app not in {'calculator','notepad','chrome'}: return {'ok':False,'message':'Application is not allowlisted.'}
        if platform.system()!='Windows': return {'ok':False,'message':'Demo application launch is enabled only on Windows.'}
        try:
            if app=='calculator': subprocess.Popen(['calc.exe'])
            elif app=='notepad': subprocess.Popen(['notepad.exe'])
            else: subprocess.Popen(['cmd','/c','start','','chrome'])
            return {'ok':True,'message':f'Launched {app}.'}
        except Exception as e: return {'ok':False,'message':f'Launch failed: {e}'}
    def delete_file(self,name):
        safe=os.path.basename(name); p=os.path.join(self.sandbox,safe)
        if not os.path.isfile(p): return {'ok':False,'message':'File not found in sandbox. Nothing deleted.'}
        os.remove(p); return {'ok':True,'message':f'Deleted sandbox file: {safe}'}
    def invoke(self,tool,args): return self.tools[tool](**args)
