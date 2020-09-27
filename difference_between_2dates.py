import sys

def NumDaysBetween(y1,m1,d1,y2,m2,d2):
    days = 0
    for y in range(y1, y1 + (y2-y1)):
        if (y < y2): # if not on current year then fast-forward to y2 and set m1 to January
            for m in range(m1, 12):
                days += NumDaysInMonth(y, m)
            m1 = 1
            m2 += 1
    for m in range (m1, m2):
        days += NumDaysInMonth(y2, m)
    days = days + (d2 - d1)
    return days

def NumDaysInMonth(y, m):
    return 30

print(NumDaysBetween(2010,5,1,2011,5,1))
print(NumDaysBetween(2010,5,1,2011,8,5))
