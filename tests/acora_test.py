from acora import AcoraBuilder
builder = AcoraBuilder('hola', 'que', 'que tal', 'hola mundo', 'mundo hola')
ac = builder.build()

result = ac.findall('hola mundo hola que tal que que que que que que que')

# result = ac.filefind('text.txt')
# result = set(kw for kw, pos in ac.filefind('text.txt'))

for kw, pos in result:
	print kw + str(pos)
print '--------------------------------'
# for item in result:
# 	print item

# print result

filtered = set([kw for kw, pos in result])
print filtered