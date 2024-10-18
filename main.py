from tokenizer import main as tk
from parser import main as ps
from evaluator import main as ev

while True:
    i = input('> ')
    if i == '/': break
    elif i: print(ev(ps(tk(i))))
    else: print()