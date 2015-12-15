import loader, parser, handler

print()

print('DATABASE')
print(loader.database)
print()

print('INSERT')
print(handler.handle(parser.parse('α{t1}[τ[a1,a2](1,2)]'), loader.database))
print(handler.handle(parser.parse('α{t2}[t1]'), loader.database))
print(handler.handle(parser.parse('α{t1}[μ{t1}{τ[a1,a2](1,3)}]'), loader.database))
print()

print('DATABASE')
print(loader.database)
print()

print('PROJECT')
print(handler.handle(parser.parse('Π[a1](t1)'), loader.database))
print(handler.handle(parser.parse('Π[a1](Π[a1,a2](t1))'), loader.database))
print()

print('SELECT')
print(handler.handle(parser.parse('σ[a1=1](t1)'), loader.database))
print(handler.handle(parser.parse('σ[a2=3](t1)'), loader.database))
print(handler.handle(parser.parse('σ[a1=1|a2=3](t1)'), loader.database))
print(handler.handle(parser.parse('σ[a2=3&a2=3](t1)'), loader.database))
print()

print('NESTED')
print(handler.handle(parser.parse('σ[a1=1](Π[a1](t1))'), loader.database))
print(handler.handle(parser.parse('σ[a1=2](Π[a1](t1))'), loader.database))
print(handler.handle(parser.parse('Π[a1](σ[a1=1](t1))'), loader.database))
print(handler.handle(parser.parse('Π[a1](σ[a1=2](t1))'), loader.database))
print()

print('UNION')
print(handler.handle(parser.parse('μ{t1}{τ[a1,a2](2,3)}'), loader.database))
print(handler.handle(parser.parse('μ{t1}{t2}'), loader.database))
print(handler.handle(parser.parse('μ{t1}{σ[a1=1](t1)}'), loader.database))
print()

print('DIFFERENCE')
print(handler.handle(parser.parse('δ{t1}{τ[a1,a2](2,3)}'), loader.database))
print(handler.handle(parser.parse('δ{t1}{t2}'), loader.database))
print()

print('PRODUCT')
print(handler.handle(parser.parse('χ{t1}{τ[a1,a2](2,3)}'), loader.database))
print(handler.handle(parser.parse('χ{t1}{t2}'), loader.database))
print()

print('RENAME')
print(handler.handle(parser.parse('ρ[a1=a3](τ[a1,a2](2,3))'), loader.database))
print(handler.handle(parser.parse('ρ[a1=a3](t1)'), loader.database))
print()

'''
$ python3 sample.py 

DATABASE
{}

INSERT
{'a1': ['1'], 'a2': ['2']}
{'a1': ['1'], 'a2': ['2']}
{'a1': ['1', '1'], 'a2': ['2', '3']}

DATABASE
{'t2': {'a1': ['1'], 'a2': ['2']}, 't1': {'a1': ['1', '1'], 'a2': ['2', '3']}}

PROJECT
{'a1': ['1', '1']}
{'a1': ['1', '1']}

SELECT
{'a1': ['1', '1'], 'a2': ['2', '3']}
{'a1': ['1'], 'a2': ['3']}
{'a1': ['1', '1'], 'a2': ['2', '3']}
{'a1': ['1'], 'a2': ['3']}

NESTED
{'a1': ['1', '1']}
{'a1': []}
{'a1': ['1', '1']}
{'a1': []}

UNION
{'a1': ['1', '1', '2'], 'a2': ['2', '3', '3']}
{'a1': ['1', '1', '1'], 'a2': ['2', '3', '2']}
{'a1': ['1', '1', '1', '1'], 'a2': ['2', '3', '2', '3']}

DIFFERENCE
{'a1': ['1', '1'], 'a2': ['2', '3']}
{'a1': ['1'], 'a2': ['3']}

PRODUCT
{'a11': ['1', '1'], 'a12': ['2', '2'], 'a21': ['2', '3'], 'a22': ['3', '3']}
{'a11': ['1', '1'], 'a12': ['1', '1'], 'a21': ['2', '3'], 'a22': ['2', '2']}

RENAME
{'a2': ['3'], 'a3': ['2']}
{'a2': ['2', '3'], 'a3': ['1', '1']}

'''
