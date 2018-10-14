from flask import Flask, render_template
from flask_ask import Ask, statement, question
import logging
from country import Country
from constants import AppConstants

app = Flask(__name__)
app.config['ASK_APPLICATION_ID'] = AppConstants.ALEXA_SKILL_ID

ask = Ask(app, '/')
countryObj = Country()

@app.route('/')
def index():
    return 'welcome to Country Info.'

@ask.launch
def launched():
    text = render_template('welcome')
    return question(text)

@ask.intent('AMAZON.HelpIntent')
def help():
    text = render_template('help')
    return question(text)

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop():
    text = render_template('cancel')
    return statement(text)

@ask.intent('countryinfo')
def country_info(country):
    info = countryObj.info(country)
    text = render_template('country_not_found')

    if isinstance(info, dict):
        return statement(text)
    
    if len(info):
        info = info[0]
        language = []
        currency = []
        [language.append(lang['name']) for lang in info['languages']]
        [currency.append(curr['name']) for curr in info['currencies']]
        print(language)
        currencies = ", ".join(currency)
        languages = ", ".join(language)
        text = """{name} is a country in {subregion} of {region}, 
        with the total area of {area} square kilometers and 
        population exceeding {population}. {capital} is the capital of {name}.
        {languages} is the most widely spoken languages in {name}. 
        {currencies} is the currency of {name}.
        """.format(
            name=info['name'],
            subregion=info['subregion'],
            region=info['region'],
            area=info['area'],
            population=info['population'],
            capital=info['capital'],
            languages=languages,
            currencies=currencies
        )
        return statement(text).simple_card(
            title=info['name'],
            content="Located in {}".format(info['subregion'])
        )

    return statement(text)

if __name__ == '__main__':
    app.run(debug=True)
