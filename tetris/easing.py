import math

def easeOutElastic(x):
    if x > 1:
        return 1;

    c4 = (2 * math.pi) / 3;

    return 0 if x == 0 else 1 if x == 1 else pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1

def easeOutBounce(x):
    n1 = 7.5625
    d1 = 2.75

    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5
        return n1 * (x / d1) * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25
        return n1 * (x / d1) * x + 0.9375
    else:
        x -= 2.625
        return n1 * (x / d1) * x + 0.984375
