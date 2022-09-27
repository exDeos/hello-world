import turtle
import math
# Make the Pentagon
pent_leg_len = 55
turtle.rt(36)
turtle.fd(pent_leg_len)
turtle.rt(72)
turtle.fd(pent_leg_len)
turtle.rt(72)
turtle.fd(pent_leg_len)
turtle.rt(72)
turtle.fd(pent_leg_len)
turtle.rt(72)
turtle.fd(pent_leg_len)
# End the Pentagon

# Make the Triangle
def law_of_cos(a,b,C):
    return math.sqrt(a**2+b**2-2*a*b*math.cos(C))

m = law_of_cos(pent_leg_len,pent_leg_len,math.radians(108))
h = m*math.cos(math.asin(pent_leg_len/2/m))
tri_leg_len = h/math.cos(math.radians(30))
turtle.rt(96)
turtle.fd(tri_leg_len)
turtle.rt(120)
turtle.fd(tri_leg_len)
turtle.rt(120)
turtle.fd(tri_leg_len)
# End the Triangle

# Revel in Glory?
turtle.hideturtle()
