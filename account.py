
import importlib

def read(model, fp):
    call = importlib.import_module('read_%s' % model)
    return call(fp)


