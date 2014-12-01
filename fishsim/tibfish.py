from random import *
from pylab import *

def fishing_nextlvl(skill):
	if skill >= 10:
		return 20*1.1**(skill-10)
	else:
		return 0

def fishing_chance(skill):
	if skill>= 10:
		rate = 0.1 + 0.4*(skill-10)/67
		if rate>0.5:
			return 0.5
		else:
			return rate
	else:
		return 0

def fishing_try(skill):
	randvar = random()
	if randvar < fishing_chance(skill):
		return True
	else:
		return False

nruns = 1000
startskill = 10
expmul = 1

printflag = True
mode = 'fishes'

if mode == 'fishes':
	fishwanted = 1000
	tryarr = zeros(nruns)
	skillarr = zeros(nruns)
	skillarr_exact = zeros(nruns)

if mode == 'tries':
	trieswanted = 1000
	fisharr = zeros(nruns)

itrun = -1
while itrun < nruns-1:
	itrun += 1

	fishskill = startskill

	fishgot = 0
	lvltries = 0
	totaltries = 0

	needtries = floor(fishing_nextlvl(fishskill)/expmul)

	while True:
	
		if fishing_try(fishskill):
			fishgot += 1
	
		lvltries += 1
		totaltries += 1
		
		if lvltries >= needtries:
			fishskill += 1
			lvltries = 0
			needtries = floor(fishing_nextlvl(fishskill)/expmul)

		if mode == 'fishes':
			if fishgot >= fishwanted:
				break
		if mode == 'tries':
			if totaltries >= trieswanted:
				break

	fishskill_exact = fishskill + lvltries/needtries

	if printflag:
		print("  Tries  |  Skill  |  Fishes  ")
		print("  "+str(totaltries)+"  |  "+str(fishskill)+"  |  "+str(fishgot)+"  ")

	if mode == 'fishes':
		tryarr[itrun] = totaltries
		skillarr[itrun] = fishskill
		skillarr_exact[itrun] = fishskill_exact
	if mode == 'tries':
		fisharr[itrun] = fishgot

#print tryarr
#print skillarr

if mode == 'fishes':
	figure(1)
	bin_size = 1; min_edge = min(tryarr)-0.5; max_edge = max(tryarr)+0.5
	N = (max_edge-min_edge)/bin_size;
	n, bins, patches = hist(tryarr, bins=np.linspace(min_edge, max_edge, N+1))
	xlim([min_edge, max_edge])

	figure(2)
	bin_size = 0.01; min_edge = 0.01* (min(floor(100*skillarr_exact))-0.5); max_edge = 0.01*(max(floor(100*skillarr_exact))+0.5)
	N = (max_edge-min_edge)/bin_size;
	n, bins, patches = hist(skillarr_exact, bins=np.linspace(min_edge, max_edge, N+1))
	xlim([min_edge, max_edge])

	figure(3)
	bin_size = 1; min_edge = min(skillarr)-0.5; max_edge = max(skillarr)+0.5
	print max_edge
	print min_edge
	N = (max_edge-min_edge)/bin_size;
	bin_list = np.linspace(min_edge, max_edge, N+1)
	n, bins, patches = hist(skillarr, bins=bin_list)
	xlim([min_edge, max_edge])

if mode == 'tries':
	figure(1)
	bin_size = 1; min_edge = min(fisharr)-0.5; max_edge = max(fisharr)+0.5
	N = (max_edge-min_edge)/bin_size;
	n, bins, patches = hist(fisharr, bins=np.linspace(min_edge, max_edge, N+1))
	xlim([min_edge, max_edge])

show()
