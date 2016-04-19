import gflags
gflags.DEFINE_integer('gInt', default = 0, help = 'test integer')
gflags.DEFINE_string('gString', default = 'not defined', help = 'test string')
gflags.FLAGS(['test.py', '--gInt', '1', '--gString', 'sfs'])
#import sys
#gflags.FLAGS(sys.argv)
print gflags.FLAGS.gInt
print gflags.FLAGS.gString

