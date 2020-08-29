try:
    import uvloop
except ImportError:
    uvloop = None

def install():
    if uvloop is not None:
        uvloop.install()