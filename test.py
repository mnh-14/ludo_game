from settings import Setting
import random

# setting = Setting(None)
# # for l in Setting.TILEMAP:
# #     print(l)
# for i in range(52):
#     print(i, Setting.TILEMAP[i])

# ch = [1,2,3,4,5,6]
# six = 0
# for _ in range(1000):
#     c = random.choice(ch)
#     if c == 6: six += 1
#     print(c, end="          ")

# print("six: ", six)
player_count = 2
six_dist = [0 for _ in range(player_count)]
records = []
options = [1,2,3,4,5,6,1,2,3,6,4,5,6,1,2,3,4,5,6,6]
curr_player = 0
same_six_count = 0

i=0
while True:
    if i==2100: break
    pick = random.choice(options)
    if pick == 6:
        same_six_count += 1
        if same_six_count >= 3: continue
        six_dist[curr_player] += 1
        if i % 30 == 0:
            records.append(six_dist.copy())
        i += 1
        continue
    same_six_count = 0
    curr_player = (curr_player+1)%player_count
    if i % 30 == 0:
        records.append(six_dist.copy())
    i+=1



for i in range(len(records)):
    print(str(i*30)+"th move: ", records[i])
    


