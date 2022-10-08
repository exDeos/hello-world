# simple example of a class with default param settings, to reduce redundancy

class ABC():
    def __init__(self, params=['dont','stop','believing']):
        self.expression= ' '.join(params)

NewObject= ABC()
NewerObject= ABC(['unless','we','get','a','little','crazy','!!'])

print('\n'.join(["At first you said:",NewObject.expression]))
print()
print('\n'.join(["But then you said:",NewerObject.expression]))

# it's a bit tacky to make 10 objects of class ABC
# but then prep them all the same within owned code,
#  when just creating default values makes a little more sense
#  if you know you're going to be relying on the defaults often
#  (e.g. using offset methods more often than absolute placement)
