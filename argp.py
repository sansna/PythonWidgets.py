import argparse

p = argparse.ArgumentParser(conflict_handler='resolve')
# This works
p.add_argument("-h", type=str, default="host", help="sdfsdf")
p.add_argument("-hm", type=str, default="lsdf", help="sdfsdf")

args = p.parse_args()
print args.hm
