# security/utils.py
def ip_key(ip):
    return f"ip:{ip}"

def user_key(user_id):
    return f"user:{user_id}"

def api_key(path):
    return f"api:{path}"

def combo(*parts):
    return "rl:".join(parts)
