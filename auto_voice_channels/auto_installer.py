try:
    import uvloop
    uvloop.install()
except ImportError:
    uvloop = None
