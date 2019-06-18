from flask import Flask
from flask import jsonify
from boto3.dynamodb.conditions import Key, Attr
import boto3
import datetime
import decimal

#TODO: Return latest temperature reading when two items are returned from DB
#TODO: Decide on a response format

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Temperature')

@app.route("/current")
def fetchCurrentTemp():
    currentTime = datetime.datetime.now()
    window = currentTime - datetime.timedelta(minutes=15) # 15 minutes ago

    response = table.scan(
        FilterExpression=Attr('Datetime')
        .between(window.strftime("%Y-%m-%d %H:%M"), currentTime.strftime("%Y-%m-%d %H:%M"))
    )
    response = replace_decimals(response)

    return jsonify(response['Items'])

# Stolen with love from garnaat
def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj
