from subprocess import call
import os

path = os.path.dirname(os.path.realpath(__file__)) 
call(["python", path + "/parse_contributions.py"])
os.system("git commit -am \"new content\"")
call(["git", "push"])
