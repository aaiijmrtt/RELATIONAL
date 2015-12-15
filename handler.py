import loader

def create(arguments, tables):
	attributes = [attribute[0] for attribute in arguments[1] if attribute != ',']
	values = [value[0] for value in arguments[4] if value != ',']
	newtable = dict()
	for value, attribute in zip(values, attributes):
		newtable[attribute] = [value]
	return newtable

def select(arguments, tables):
	joins = ['&'] + [join for join in arguments[1] if join in ['&', '|']]
	conditions = [[condition[0], condition[1], condition[2]] for condition in arguments[1] if condition not in ['&', '|']]
	table = handle(arguments[4], tables)
	keys = [key for key in table]
	newtable = {key: [] for key in keys}
	for i in range(len(table[keys[0]])):
		superflag = True
		for join, condition in zip(joins, conditions):
			if condition[1] == '>':
				flag = table[condition[0]][i] > condition[2]
			elif condition[1] == '<':
				flag = table[condition[0]][i] < condition[2]
			elif condition[1] == '!=':
				flag = table[condition[0]][i] != condition[2]
			elif condition[1] == '>=':
				flag = table[condition[0]][i] >= condition[2]
			elif condition[1] == '<=':
				flag = table[condition[0]][i] <= condition[2]
			else:
				flag = table[condition[0]][i] == condition[2]
			if join == '&':
				superflag = superflag and flag
			else:
				superflag = superflag or flag
		if superflag:
			for key in keys:
				newtable[key].append(table[key][i])
	return newtable

def project(arguments, tables):
	attributes = [attribute[0] for attribute in arguments[1] if attribute != ',']
	table = handle(arguments[4], tables)
	newtable = dict()
	for attribute in table:
		if attribute in attributes:
			newtable[attribute] = table[attribute]
	return newtable

def rename(arguments, tables):
	newname = arguments[1][0][0]
	oldnames = [condition[0] for condition in arguments[1] if condition not in ['&', '|']]
	newnames = [condition[2] for condition in arguments[1] if condition not in ['&', '|']]
	table = handle(arguments[4], tables)
	newtable = dict()
	for key in table:
		flag = True
		for i in range(len(oldnames)):
			if key == oldnames[i]:
				newtable[newnames[i]] = table[key]
				flag = False
				break
		if flag:
			newtable[key] = table[key]
	return newtable

def union(arguments, tables):
	table1 = handle(arguments[1], tables)
	table2 = handle(arguments[4], tables)
	newtable = dict()
	for attribute in table1:
		newtable[attribute] = table1[attribute] + table2[attribute]
	return newtable

def difference(arguments, tables):
	table1 = handle(arguments[1], tables)
	table2 = handle(arguments[4], tables)
	keys = [key for key in table1]
	newtable = {key: [] for key in keys}
	for i in range(len(table1[keys[0]])):
		superflag = True
		for j in range(len(table2[keys[0]])):
			flag = True
			for key in keys:
				flag = flag and (table1[key][i] == table2[key][j])
			if flag:
				superflag = False
				break
		if superflag:
			for key in keys:
				newtable[key].append(table1[key][i])
	return newtable

def product(arguments, tables):
	table1 = handle(arguments[1], tables)
	table2 = handle(arguments[4], tables)
	keys1 = [key for key in table1]
	keys2 = [key for key in table2]
	length1 = len(table1[keys1[0]])
	length2 = len(table2[keys2[0]])
	newtable = {key1 + '1': [] for key1 in keys1}
	newtable.update({key2 + '2': [] for key2 in keys2})
	for key1 in keys1:
		newtable[key1 + '1'] += table1[key1] * length2
	for key2 in keys2:
		for index in range(length2):
			for i in range(length1):
				newtable[key2 + '2'].append(table2[key2][index])
	return newtable

def assign(arguments, tables):
	newname = arguments[1][0]
	table = handle(arguments[4], tables)
	loader.database[newname] = table
	return table

statements = {
	'τ': create,
	'σ': select,
	'Π': project,
	'ρ': rename,
	'μ': union,
	'δ': difference,
	'χ': product,
	'α': assign
}

def handle(arguments, tables):
	if arguments[0] in statements:
		return statements[arguments[0]](arguments[1: ], tables)
	elif arguments[0] in tables:
		return tables[arguments[0]]
	else:
		return arguments
