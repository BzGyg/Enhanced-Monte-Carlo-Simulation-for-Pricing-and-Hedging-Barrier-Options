from xbbg import blp
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

tenors = [3, 14, 31, 45, 66, 73, 94, 106, 122, 136, 157, 167, 248, 259, 276, 
                   339, 349, 430, 521, 612, 640, 976]
ex = [datetime(2024, 4, 16) + timedelta(days = i) for i in tenors]
expiry = [i.strftime("%m/%d/%y") for i in ex]
x = list(range(445, 565))
pdatas = pd.DataFrame(index = x)

for i in range(len(expiry)):
    data = pd.DataFrame(index = x)
    
    e = expiry[i]
    info = np.array(['SPY {} P{} Equity'.format(e, k) for k in x])
    a = blp.bdh(info, ['Px_Mid', 'IVol_Mid'], '20240416', '20240416')
    b = pd.DataFrame(index = [int(a.columns[i][0][-10:-7]) for i in range(len(a.columns))][::2])

    b[e + ' Px_Mid'] = a.values[0][::2]
    b[e + ' IVol_Mid'] = a.values[0][1::2]
    data[e + ' Px_Mid'] = [np.nan]*len(x)
    data[e + ' IVol_Mid'] = [np.nan]*len(x)
    
    result = data.combine_first(b)
    pdatas[result.columns] = result
    
pdatas = pdatas.dropna(how = 'all')