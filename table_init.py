import json

borders = []

for i in range(16):
	comb = str(bin(i))[2:].zfill(4)
	borders.append(comb)
widths = ['0','1','NA']
heights = ['2','3','NA']

states = {}
for i in widths:
	for j in heights:
		for k in borders:
			states[str((i,j,k))] = [0,0,0,0]

with open("qvalues.json", "w") as f:
	json.dump(states, f)