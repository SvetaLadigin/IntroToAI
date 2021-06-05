import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

f = open('statistics.txt', 'r')
time= []
tile = []
agent = []
score = []
depth = []
avg_depth = []
avg_score = []
data = {}
for line in f:
    params = line.split()
    print(params)
    time.append(int(params[0]))
    agent.append(params[1])
    tile.append(int(params[2]))
    score.append(int(params[3]))
    depth.append(int(params[4]))
data['time'] = time
data['agent'] = agent
data['tile'] = tile
data['score'] = score
data['depth'] = depth
new_data = pd.DataFrame.from_dict(data)
avg_depth = new_data.groupby('time').depth.mean()
print(avg_depth)
avg_score = new_data.groupby('time').score.mean()
# new_data.to_numpy()
# gra = plt.plot(new_data['time'], new_data['depth'])
# print(gra)
# gra.show()
graph = avg_depth.plot(xlabel='time', ylabel='depth', style='r')
plt.savefig('time_depth.png')
plt.show()

graph2 = avg_score.plot(xlabel='time', ylabel='score', style='g')
plt.savefig('time_score.png')
plt.show()
