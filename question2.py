#Note: when using this exisits function, user have to put the variable in between two apostrophe
v=1
c=3
f=5

def exists(v):
    if v in locals() or v in globals():
        return True
    else:
        return False
print(exists('v'))
print(exists('c'))
print(exists('t'))

#output
# True
# True
# False
