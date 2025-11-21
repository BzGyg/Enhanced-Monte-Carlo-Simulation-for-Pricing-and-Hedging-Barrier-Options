from xbbg import blp
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

tenors = list(range(0, 365*3 + 1))

ex = [datetime(2024, 4, 16) - timedelta(days = i) for i in tenors]
expiry = [i.strftime("%m/%d/%y") for i in ex]
x = list(range(445, 566))
datas = pd.DataFrame(index = x)

for i in range(len(expiry)):
    data = pd.DataFrame(index = x)
    
    e = expiry[i]
    info = np.array(['SPY US 04/16/24 C{} Equity'.format(k) for k in x])
    a = blp.bdh(info, ['Px_Mid', 'IVol_Mid'], e, e)
    b = pd.DataFrame(index = [int(a.columns[i][0][-10:-7]) for i in range(len(a.columns))][::2])
    
    if a.empty:
        continue

    b[e + ' Px_Mid'] = a.values[0][::2]
    b[e + ' IVol_Mid'] = a.values[0][1::2]
    data[e + ' Px_Mid'] = [np.nan]*len(x)
    data[e + ' IVol_Mid'] = [np.nan]*len(x)
    
    result = data.combine_first(b)
    datas[result.columns] = result
    
datas = datas.dropna(how = 'any')