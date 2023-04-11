# https://www.wolframalpha.com/input?i=log%288589934592*10**%284%2F5%29*exp%2832*y*log%2810%29%2F5%29%2F15625%29
import sympy as sym
from sympy import log

# 定义符号变量和函数
x, y, z = sym.symbols('x y z')
f = (10*log(x /512)/log(10) + 52)/64
f2 = log(x * (32768**2) )

# 求解反函数
f_inv = sym.solve(sym.Eq(y, f), x)
#f_inv[0]

# 计算 z 值
z_val = f2.subs(x, f_inv[0])
z_val = sym.simplify(z_val)
print(z_val)
z_val

#print(z_val)
