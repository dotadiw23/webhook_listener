
from flask import Flask, jsonify, request
import datetime
import os

app = Flask(__name__)
separator = "-----------------------------------------------------------------------------------------------"

# Save data in a log file ordered by month_logs/day_logs/hour.log
def save_log(log):
    full_date = datetime.datetime.now().strftime("%c")
    month_date = datetime.datetime.now().strftime("%B-%Y")
    
    # Month folder 
    if not os.path.isdir(".\{}".format(month_date)):
        os.mkdir(month_date)
    
    # Day folder  
    day_date = datetime.datetime.now().strftime("%d-%m-%Y")  
    if not os.path.isdir('.\{}\{}'.format(month_date, day_date)):
        os.mkdir('.\{}\{}'.format(month_date, day_date))
        
    # Save the hourly log
    log_name = "{}.log".format(datetime.datetime.now().strftime("%I_59_%p"))
    if os.path.isfile(".\{}\{}\{}".format(month_date, day_date, log_name)):
        f= open(".\{}\{}\{}".format(month_date, day_date, log_name), 'a')
    else:
        f= open(".\{}\{}\{}".format(month_date, day_date, log_name), 'w')
    f.write(full_date + os.linesep + log + os.linesep)
    f.close()

    
@app.route('/')
def hello_world():
    return jsonify('Hello World')


@app.route('/page_webhook', methods=['POST'])
def recieve_webhook():
    try:
        r = str(request.json)
        print("Log: {}".format(r))
        save_log(r)
        return jsonify('Ok')
    except Exception:
        return jsonify('Invalid request')
    
    
if __name__ == '__main__':
    app.run('', debug=True)