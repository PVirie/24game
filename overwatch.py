
class Job:
	def __init__(self, meta):
		self.meta = meta
		self.neighbors = []
		self.group = None

	def add_neighbor(self, player):
		self.neighbors.append(player)

	def assign_group(self, group):
		self.group = group

class Player:
	def __init__(self, meta):
		self.meta = meta
		self.neighbors = []
		self.group = None

	def add_neighbor(self, job):
		self.neighbors.append(job)

	def assign_group(self, group):
		self.group = group

class Group:
	def __init__(self):
		self.id_to_players = {}
		self.id_to_jobs = {}

	def __len__(self):
		return len(self.id_to_jobs)

	def completed(self):
		return len(self.id_to_jobs) == len(self.id_to_players)

	def add_player(self, p):
		self.id_to_players[p.meta] = (p)
		for n in p.neighbors:
			self.id_to_jobs[n.meta] = n

	def list_players(self):
		return list(self.id_to_players.values())

	def get_candidate(self):
		for _, j in self.id_to_jobs.items():
			for p in j.neighbors:
				if p.meta not in self.id_to_players:
					yield p

	def remove_player(self, p):
		del self.id_to_players[p.meta]

	def list_jobs(self):
		return list(self.id_to_jobs.values())

	def remove_job(self, j):
		del self.id_to_jobs[j.meta]

def make_group(players):
	g = Group()
	for p in players:
		g.add_player(p)
	return g

def minimal_group(p):
	group_players = [p]
	g = make_group(group_players)
	if g.completed():
		return g

	smallest_group = None
	incompleted_group = [g]
	while len(incompleted_group) > 0:
		g = incompleted_group.pop()
		cps = g.list_players() 
		for p in g.get_candidate():
			ng = make_group(cps + [p])
			if not ng.completed():
				incompleted_group.append(ng)
			else:
				if smallest_group == None or len(smallest_group) > len(ng):
					smallest_group = ng
	return smallest_group



def create_graph(table):
	jobs = [Job("job " + str(i)) for i in range(len(table))]
	players = []
	for j, player in enumerate(table):
		p = Player("player " + str(j))
		for i, c in enumerate(player):
			if c > 0.5:
				p.add_neighbor(jobs[i])
				jobs[i].add_neighbor(p)
		players.append(p)
	return players, jobs


def print_group(g):
	print([p.meta for p in g.id_to_players.values()], end=" => ")
	print([j.meta for j in g.id_to_jobs.values()])
	
if __name__ == '__main__':

	players, jobs = create_graph([[1, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [1, 0, 1, 0, 0]])
	groups = []
	for p in players:
		g = minimal_group(p)
		groups.append(g)
	groups.sort(key=lambda g: len(g))
	for g in groups:
		for p in g.list_players():
			if p.group is not None:
				g.remove_player(p)
			else:
				p.assign_group(g)

		for j in g.list_jobs():
			if j.group is not None:
				g.remove_job(j)
			else:
				j.assign_group(g)

		print_group(g)





