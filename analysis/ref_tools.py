import pandas as pd

def l_avgifnonnone(l):
    if l is None:
        return None
    else:
        l = [e for e in l if not pd.isna(e)]
        if len(l)==0:
            return None
        return sum(l)/len(l)
