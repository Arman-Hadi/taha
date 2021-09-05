from flask import Flask, render_template
import pandas
from os import listdir


app = Flask(__name__)

@app.route('/')
def home():
    files = [(i.split('.')[0], 'csv/'+i) for i in listdir('csv')]
    context = {
        'files': files,
        'name': 'arman',
    }
    return render_template('home.html', **context)


@app.route('/s/<string:stock>')
def stock(stock):
    files = [(i.split('.')[0], 'csv/'+i) for i in listdir('csv')]

    offset = -50
    df = pandas.read_csv(f'csv/{stock}.csv', encoding='utf-16')
    row = df['<DTYYYYMMDD>'][offset:].tolist()
    price = df['<OPEN>'][offset:].tolist()

    context = {
        'row': row,
        'price': price,
        'files': files,
    }
    return render_template('stock.html', **context)


if __name__ == '__main__':
    app.run()
