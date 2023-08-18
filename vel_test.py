

a = 5
b = 0

a_set = 10
b_set = 0

print("초기 좌표 값:",a)
print("설정한 좌표 값:",a_set)
print("-------------------------------")

while True:
    if a_set > a:
        print("올라가나요")
        vel = abs(a - a_set)
        print("vel 값:", vel)
        a = a + vel
        print("움직인 좌표 값1:", a)
    elif a_set < a:
        print("내려가나요")
        vel = abs(a - a_set)
        print("vel 값:", vel)
        a = a - vel
        print("움직인 좌표 값2:", a)
    elif a_set == a:
        print("end")
        break
