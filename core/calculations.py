from core.graph import Switch#, get_sccs

ON = 1
OFF = 0


def calculate_benes(alpha, beta, n):
	"""
	Calculate the probability of an ordered set alpha to get to the ordered set beta
	with n being the current size of the net
	"""
	if not alpha:
		return 1.0

	if n == 2:
		return 0.5

	sccs = get_sccs(alpha, beta, n)
	return calculate_all(alpha, beta, sccs, n)


def get_sccs(alpha, beta, n):
	# return [[[Switch(0, 4, True), Switch(2, 6, False), Switch(1, 5, True)]],
	# 						  [[Switch(3, 7, True), Switch(3, 7, False)]]]
	return [[[Switch(0, 4, True), Switch(2, 6, False), Switch(1, 5, True)]]]


def calculate_all(alpha, beta, sccs, n):
	"""
	Traverse all possible permutations of switches/SCCs, and recursively calculate the probability
	 n
	B
	 (alpha->beta)
	"""
	benes_sum = 0
	half_n = n / 2
	denom = 1.0 / (2 ** get_num_of_switches(sccs))

	for perm in range(2 ** len(sccs)):
		# Get the states of all the *relevant* switches
		top_switches = calculate_switches(sccs, perm)
		alpha_left = []
		alpha_right = []
		beta_left = []
		beta_right = []

		for i in range(len(alpha)):
			src = alpha[i]
			dest = beta[i]

			switch_state = top_switches[get_lower(src, half_n)]
			update_alphas_and_betas(src, dest, switch_state, alpha_left, beta_left, alpha_right, beta_right, half_n)

		alpha_right = [get_lower(val, half_n) for val in alpha_right]
		beta_right = [get_lower(val, half_n) for val in beta_right]

		benes_sum += calculate_benes(alpha_left, beta_left, half_n) * calculate_benes(alpha_right, beta_right, half_n)

	return denom * benes_sum


def get_num_of_switches(sccs):
	num_of_switches = 0
	for j in range(len(sccs)):
		scc = sccs[j]
		for sub_scc in scc:
			num_of_switches += len(sub_scc)

	return num_of_switches


def update_alphas_and_betas(src, dest, switch_state, alpha_left, beta_left, alpha_right, beta_right, half_n):
	"""
	Depending on the state of the switch and the source value, add to/from values to either the
	left or the right side, for the recursion
	"""
	if switch_state == ON:
		if src < half_n:
			alpha_right.append(src + half_n)
			beta_right.append(get_upper(dest, half_n))
		else:
			alpha_left.append(src - half_n)
			beta_left.append(get_lower(dest, half_n))
	else:
		if src < half_n:
			alpha_left.append(src)
			beta_left.append(get_lower(dest, half_n))
		else:
			alpha_right.append(src)
			beta_right.append(get_upper(dest, half_n))


def get_upper(val, half_n):
	return val if val > half_n else val + half_n


def get_lower(val, half_n):
	return val if val < half_n else val - half_n


def calculate_switches(sccs, perm):
	"""
	Create maps from top switches to their current state, dependant on
	the SCCs and the current permutation
	"""
	# Create an empty lists for the top/bottom switches
	top_switches = dict()

	for j in range(len(sccs)):
		scc = sccs[j]

		# Get the j'th bit
		c = 1 << j

		# If the j'th bit in i is up, this scc should start from an on switch
		starting_state = ON if bin(perm & c)[2] == '1' else OFF

		# Iterate over
		for sub_scc in scc:
			for switch in sub_scc:
				# Update the value of the switch
				if switch.top:
					top_switches[switch.left] = starting_state
			# Flip the state, because we've passed a dotted edge
			starting_state = ON if starting_state == OFF else OFF

	return top_switches


if __name__ == '__main__':
	print calculate_benes((1, 4), (2, 6), 8)