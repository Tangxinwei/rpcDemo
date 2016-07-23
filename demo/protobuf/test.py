import sys
sys.path.append('../../3rdpart')

import test_pb2
person = test_pb2.Person()
person.name = 'test'
person.no = 1
newPerson = person.p.add()
newPerson.name = 'newPerson'
newPerson.no = 2
personString = person.SerializeToString()

print personString

newPerson = test_pb2.Person()
newPerson.ParseFromString(personString)

print newPerson.name, newPerson.no, newPerson.p[0].name