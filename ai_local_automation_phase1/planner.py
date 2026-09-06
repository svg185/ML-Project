import re
def extract_name(c):
    m=re.search(r'(?:named|called)\s+[\'\"]?([^\'\"]+)[\'\"]?$',c,re.I); return m.group(1).strip() if m else 'New Folder'
def extract_search(c):
    m=re.search(r'(?:search for|find|look for)\s+(.+)',c,re.I); return m.group(1).strip() if m else ''
def extract_app(c):
    for a in ('chrome','calculator','notepad'):
        if a in c.lower(): return a
def make_plan(intent,c):
    if intent=='create_folder': return [{'tool':'create_folder','arguments':{'name':extract_name(c)}}]
    if intent=='list_files': return [{'tool':'list_files','arguments':{}}]
    if intent=='search_files': return [{'tool':'search_files','arguments':{'query':extract_search(c)}}]
    if intent=='open_application': return [{'tool':'open_application','arguments':{'app':extract_app(c)}}]
    if intent=='delete_file': return [{'tool':'delete_file','arguments':{'name':extract_search(c) or 'unknown'}}]
    return []
