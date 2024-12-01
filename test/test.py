import datetime
now = datetime.datetime.now()
minutes_now = now.minute
hours_now = now.hour
now_time = minutes_now + hours_now*100
p1_1 = 830
p1_2 = 1005

p2_1 = 1015
p2_2 = 1150

p3_1 = 1220
p3_2 = 1355

p4_1 = 1425
p4_2 = 1600

p5_1 = 1610
p5_2 = 1745

p6_1 = 1755
p6_2 = 1930

if now_time == p1_1:
    print("o")
print(p1_1)