#!/home/xiaorui/anaconda3/envs/tf/bin/python3

# https://docs.sympy.org/latest/tutorials/intro-tutorial/simplification.html#apart
# https://www.wolframalpha.com/input?i=log%288589934592*10**%284%2F5%29*exp%2832*y*log%2810%29%2F5%29%2F15625%29

import sympy as sym
from sympy import log,ln

# 定义符号变量和函数
x, y, z = sym.symbols('x y z',real=True)
f = (10*ln(x /512)/log(10) + 52)/64
f2 = ln(x * (32768**2) )

# 求解反函数
f_inv = sym.solve(sym.Eq(y, f), x)
print("f_inv")
display(f_inv[0])
#f_inv[0]

# 计算 z 值
z_val = f2.subs(x, f_inv[0])
z_val = sym.separatevars(sym.simplify(z_val,inverse=True))
z_val = sym.expand_log(z_val)
z_val = sym.separatevars(z_val)

#print(z_val)
print("F1")
display(f)
print("F2")
display(f2)

print("f2( f1-1 (y))")
print(z_val)
display(z_val)
