from settings import Setting

setting = Setting(None)
# for l in Setting.TILEMAP:
#     print(l)
for i in range(52):
    print(i, Setting.TILEMAP[i])