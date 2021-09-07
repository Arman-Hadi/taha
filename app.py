from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas
from os import listdir
from datetime import date


app = Flask(__name__)
DATE = '<DTYYYYMMDD>'


def get_df_names():
    files = [('csv/'+i, i.split('.')[0]) for i in listdir('csv')]
    res = dict()
    for f in files:
        df = pandas.read_csv(f[0], encoding='utf-16')
        res[f[1]] = df['<TICKER>'][0]
    return res


@app.route('/')
def home():
    files = get_df_names()
    context = {
        'files': files,
    }
    return render_template('home.html', **context)


@app.route('/s/<string:stock>')
def stock(stock):
    files = get_df_names()

    df = pandas.read_csv(f'csv/{stock}.csv', encoding='utf-16')

    context = {
        'len': len(df),
        'from': df[DATE][0],
        'to': df[DATE].iloc[-1],
        'files': files,
        'columns': df.columns[3:],
        'stock': (stock, df['<TICKER>'][0]),
    }
    return render_template('stock.html', **context)


@app.route('/import', methods=['GET', 'POST'])
def import_stock():
    files = get_df_names()
    if request.method == 'GET':
        context = {
            'files': files,
        }
        return render_template('import.html', **context)
    elif request.method == 'POST':
        if 'files' in request.files:
            fn = []
            for f in request.files.getlist('files'):
                fn.append(f.filename)
                f.save(f'csv/{secure_filename(f.filename)}')

            alert = f'{fn} imported successfuly! You can see them in stocks!'
            return redirect(url_for('home')+f'?alert={alert}')
        alert = 'No file!'
        return redirect(url_for('home')+f'?alert={alert}')


@app.route('/api/s/<string:stock>', methods=['GET',])
def api_stock(stock):
    _y = request.args.get('y', None)
    try:
        _from = date.fromisoformat(request.args.get('from', None))
        _to = date.fromisoformat(request.args.get('to', None))
    except:
        return {
            'error': '`from` and `to` must be date like!'}, 400

    if _y and _from and _to:
        df = pandas.read_csv(f'csv/{stock}.csv', encoding='utf-16')
        f, t = 0, 0
        for d in df[DATE]:
            dd = date.fromisoformat(d)
            if _from <= dd and not f:
                f = df[DATE].tolist().index(d)
            if dd <= _to:
                t = df[DATE].tolist().index(d)
        x = df[DATE][f:t+1].tolist()
        y = df[_y][f:t+1].tolist()
        print(x[-1])
        return {'x': x, 'y': y}
    else:
        return {
            'error': '`x`, `y`, `from`, `to` must be assigned!'}, 400


if __name__ == '__main__':
    app.run()
