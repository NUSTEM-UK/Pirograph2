# Give me a function to convert camera exposure from milliseconds to fractions of a second

def exposure_to_fraction(exposure):
    return 1 / (1000 / exposure)

print(exposure_to_fraction(1000)) # 1.0
print(exposure_to_fraction(500)) # 0.5
print(exposure_to_fraction(250)) # 0.25
print(exposure_to_fraction(125)) # 0.125
print(exposure_to_fraction(60)) # 0.06

# OK, now can you do that in fractions of second rather than decimal seconds?

from fractions import Fraction

def exposure_to_fraction(exposure):
    # Integer division because fractions, durr.
    return Fraction(1, 1000 // exposure)

print(exposure_to_fraction(1000)) # 1
print(exposure_to_fraction(500)) # 1/2
print(exposure_to_fraction(250)) # 1/4
print(exposure_to_fraction(125)) # 1/8
print(exposure_to_fraction(60)) # 1/16
print(exposure_to_fraction(30)) # 1/33
print(exposure_to_fraction(15)) # 1/66
print(exposure_to_fraction(8)) # 1/125
print(exposure_to_fraction(4)) # 1/250
print(exposure_to_fraction(2)) # 1/500
print(exposure_to_fraction(80)) # 1/12
