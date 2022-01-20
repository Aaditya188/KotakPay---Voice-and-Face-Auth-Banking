from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment')
def payment():
    return render_template('button.html')

@app.route('/paynow')
def paynow():
    return render_template('payment.html')

if __name__ == '__main__':
      app.run(port=8080)