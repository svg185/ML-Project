RISKY={'delete_file','open_application'}
def needs_confirmation(tool): return tool in RISKY
def validate(plan,registry):
    if not plan: return False,'No executable plan generated.'
    for s in plan:
        if s['tool'] not in registry: return False,f"Tool not allowlisted: {s['tool']}"
    return True,'Plan validated.'
