import subprocess
import hashlib

def run(user_input):
    subprocess.run("ls " + user_input, shell=True)

def hash_password(pw):
    return hashlib.md5(pw.encode()).hexdigest()

def calc(expr):
    return eval(expr)