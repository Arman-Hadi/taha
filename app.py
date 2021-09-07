from flask import Flask, render_template, request, jsonify
import pandas
from os import listdir
from datetime import date


app = Flask(__name__)
DATE = '<DTYYYYMMDD>'

@app.route('/')
def home():
    files = [i.split('.')[0] for i in listdir('csv')]
    context = {
        'files': files,
        'name': 'arman',
    }
    return render_template('home.html', **context)


@app.route('/s/<string:stock>')
def stock(stock):
    files = [i.split('.')[0] for i in listdir('csv')]

    df = pandas.read_csv(f'csv/{stock}.csv', encoding='utf-16')

    context = {
        'len': len(df),
        'from': df[DATE][0],
        'to': df[DATE].iloc[-1],
        'files': files,
        'columns': df.columns[3:],
        'stock': stock,
    }
    return render_template('stock.html', **context)


@app.route('/api/s/<string:stock>')
def api_stock(stock):
    if request.method == 'GET':
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
    else:
        return {'error': 'Method not allowed!'}, 405


if __name__ == '__main__':
    app.run()
