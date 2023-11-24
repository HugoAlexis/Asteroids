def order(item):
    return item[1]

scores = open("Scores.txt", "r")

datas = []

for line in scores:
    score = line.split('|')
    datas.append([score[0], int(score[1])])

datas.sort(key=order, reverse=True)
for i in datas:
    print(i)
