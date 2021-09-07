import pandas, datetime
from os import listdir


files = ['csv/'+i for i in listdir('csv')]

for f in files:
    df = pandas.read_csv(f, encoding='utf-16')

    dd = []
    for d in df['<DTYYYYMMDD>']:
        ds = str(d)
        dfs = f'{ds[0:4]}-{ds[4:6]}-{ds[6:8]}'
        dd.append(str(datetime.date.fromisoformat(dfs)))

    df['<DTYYYYMMDD>'] = dd

    df.to_csv('c'+f, encoding='utf-16')
