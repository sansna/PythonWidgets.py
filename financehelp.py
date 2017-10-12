#!/bin/python3
# Actually this module is used to solve my problem about how to accumulate
#+ fortune. It tells me first to get as much money as possible in the first
#+ years, and to learn investment in the later years to come, which is
#+ as correct as my instinct told me.

def financehelpyear():
    yearly = int(input("What is yearly?\n"))
    rate = float(input("What is rate?\n"))

    sum = 0.0
    for i in range(1,20):
        sum = (sum+yearly)*(1+rate)
        print("At year "+str(i)+" I can gain "+str(sum)+" money.")

def financehelpmonth():
    monthly=int(input("What is monthly?\n"))
    ratemonth=float(input("What is ratemonth?\n"))

    sum=0.0
    for i in range(0,20):
        for j in range(0,11):
            sum = (sum+monthly)*(1+ratemonth)
        print("At year "+str(i)+" I earned "+str(sum)+" money.")

choice=input("What kind of function would you want? (y/m)\n")
if choice == "y":
    financehelpyear()
elif choice == "m":
    financehelpmonth()
else:
    print("Error input.")
