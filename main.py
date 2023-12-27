import yfinance as yf
from flask import Flask, jsonify, request
from flask_mail import Mail, Message

app = Flask(__name__)


##### For Get Stock Details #####


def get_stock_details(stock_symbol):
    # Fetch historical data for the stock
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="max")

    # Find the all-time high and low prices
    all_time_high = hist['High'].max()
    all_time_low = hist['Low'].min()

    # Get the most recent data for other details
    latest_data = hist.iloc[-1]
    current_price = latest_data['Close']
    opening_price = latest_data['Open']
    closing_price = latest_data['Close']

    return {
        'All Time High': all_time_high,
        'All Time Low': all_time_low,
        'Current Price': current_price,
        'Opening Price': opening_price,
        'Closing Price': closing_price,
    }


@app.route('/stock/<stock_symbol>', methods=['GET'])
def stock_details(stock_symbol):
    stock_details = get_stock_details(stock_symbol)
    return jsonify(stock_details)

##### For send Email #####


mail = Mail(app)  # instantiate the mail class
# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'baskaran1.earthfokus@gmail.com'
app.config['MAIL_PASSWORD'] = 'naye hezy tvnr lonk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# message object mapped to a particular URL ‘/’


@app.route("/sendEmail", methods=['POST'])
def send_email():
    data = request.get_json()

    recipients = data.get('to_email')
    subject = data.get('subject', 'Hello')
    body = data.get('message')

    msg = Message(
        subject,
        sender='baskaran1.earthfokus@gmail.com',
        recipients=recipients
    )
    msg.body = body
    mail.send(msg)

    response = {
        'status': 'Sent',
        'recipients': recipients
    }
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
