from pyc4 import c4

incoder = c4.Encoder()
incoder.write(u'foo')
id = incoder.id()

print id.string()
id2 = c4.identify(u'bar')
print id2.string()

id3, err = c4.parse(id2.string())
if err:
  print "error: ", err
  exit

if id3:
  print id3.string()
