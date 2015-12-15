import pyparsing

operators = pyparsing.Or([
	pyparsing.Literal("="),
	pyparsing.Literal(">"),
	pyparsing.Literal("<"),
	pyparsing.Literal("!="),
	pyparsing.Literal(">="),
	pyparsing.Literal("<=")
])

identifiers = pyparsing.Word(pyparsing.alphanums)

expressions = pyparsing.Group(identifiers)

equations = pyparsing.Group(
	pyparsing.And([
		identifiers,
		operators,
		identifiers
	])
)

expressionconjunctions = pyparsing.Literal(",")

compoundexpressions = pyparsing.Group(
	pyparsing.And([
		expressions,
		pyparsing.Optional(
			pyparsing.OneOrMore(
				pyparsing.And([
					expressionconjunctions,
					expressions
				])
			)
		)
	])
)

equationconjunctions = pyparsing.Or([
	pyparsing.Literal("&"),
	pyparsing.Literal("|")
])

compoundequations = pyparsing.Group(
	pyparsing.And([
		equations,
		pyparsing.Optional(
			pyparsing.OneOrMore(
				pyparsing.And([
					equationconjunctions,
					equations
				])
			)
		)
	])
)

create = pyparsing.Forward()
select = pyparsing.Forward()
project = pyparsing.Forward()
rename = pyparsing.Forward()
union = pyparsing.Forward()
difference = pyparsing.Forward()
product = pyparsing.Forward()
assign = pyparsing.Forward()

literal = pyparsing.Or([
	create,
	select,
	project,
	rename,
	union,
	difference,
	product
])

create <<= pyparsing.And([
	pyparsing.Literal("τ"),
	pyparsing.Literal("["),
	compoundexpressions,
	pyparsing.Literal("]"),
	pyparsing.Literal("("),
	compoundexpressions,
	pyparsing.Literal(")")
])

select <<= pyparsing.And([
	pyparsing.Literal("σ"),
	pyparsing.Literal("["),
	compoundequations,
	pyparsing.Literal("]"),
	pyparsing.Literal("("),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal(")")
])

project <<= pyparsing.And([
	pyparsing.Literal("Π"),
	pyparsing.Literal("["),
	compoundexpressions,
	pyparsing.Literal("]"),
	pyparsing.Literal("("),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal(")")
])

rename <<= pyparsing.And([
	pyparsing.Literal("ρ"),
	pyparsing.Literal("["),
	compoundequations,
	pyparsing.Literal("]"),
	pyparsing.Literal("("),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal(")")
])

union <<= pyparsing.And([
	pyparsing.Literal("μ"),
	pyparsing.Literal("{"),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal("}"),
	pyparsing.Literal("{"),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal("}")
])

difference <<= pyparsing.And([
	pyparsing.Literal("δ"),
	pyparsing.Literal("{"),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal("}"),
	pyparsing.Literal("{"),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal("}")
])

product <<= pyparsing.And([
	pyparsing.Literal("χ"),
	pyparsing.Literal("{"),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal("}"),
	pyparsing.Literal("{"),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal("}")
])

assign <<= pyparsing.And([
	pyparsing.Literal("α"),
	pyparsing.Literal("{"),
	pyparsing.Group(
		identifiers
	),
	pyparsing.Literal("}"),
	pyparsing.Literal("["),
	pyparsing.Group(
		pyparsing.Or([
			literal,
			identifiers
		])
	),
	pyparsing.Literal("]")
])

statement = pyparsing.Or([
	literal,
	assign
])

def parse(string):
	return statement.parseString(string).asList()
