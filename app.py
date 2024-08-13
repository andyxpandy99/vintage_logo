from flask import Flask, request, render_template, send_file
import pandas as pd
import io
from get_corp_logo import get_wikipedia_url, get_company_logo_url
from get_vintage import get_investment_image_link, get_all_investments_details

app = Flask(__name__)

funds_list = [
    "01 Advisors", "7 Wire Ventures", "83 North", "A*", "Andreessen Horowitz", "Abstract Ventures", 
    "Afore Capital", "AIX Ventures", "Amino Collective", "Amiti", "Amplify", "Audacious Ventures", 
    "Avid Ventures", "Battery", "Bessemer Venture Partners", "Better Tomorrow Ventures", 
    "Bling Capital", "Blue Yard", "Boldstart", "Chalfen Ventures", "Congruent Ventures", "Craft", 
    "Creandum", "CRV", "Cyberstarts", "DCVC", "Designer Fund", "Emerge", "Entree Capital", "F2", 
    "Floodgate", "Founder Collective", "Foundry Group", "General Catalyst", "Glilot Capital Partners", 
    "Golden Ventures", "Grove Ventures", "GSV Ventures", "Hetz Ventures", "Jibe Ventures", 
    "Kleiner Perkins", "Lightspeed", "LocalGlobe", "Ludlow Ventures", "Mango Capital", "Maple Capital", 
    "Mayfield", "Meritech", "Multicoin Capital", "NfX", "PSL", "Pitango", "PointNine", "Pontifax", 
    "Primary", "Redpoint", "Resolute Ventures", "Ribbit Capital", "S Capital", "Scale", "Seedcamp", 
    "Singular", "Spark Capital", "Stage One", "Starting Line", "Synthesis Capital", "System One", 
    "TLV Partners", "True Ventures", "Twelve Below", "Uncork", "Up West", "Versant Ventures", 
    "Vertex Ventures", "Viola", "Visionaries Club", "Zeev Ventures"
]

direct_investments_list = [
    "Activefence", "Alooma", "Anecdotes", "Autotalks", "BigID", "BlueVine", "Capitolis", "Cast", "Celeno", 
    "Cellwize", "Clarizen", "Ctera", "Cyberseason", "Cynet", "Datagen", "Datarails", "Deci", "Deel", "Duda", 
    "Earnix", "Ebury", "Electric", "Enzymotec", "Explorium", "Forescout", "Formlabs", "Gigya", "Guardio", 
    "Guardicore", "Holidu", "HoneyBook", "Hourly", "Hungry Panda", "Innovid", "JFrog", "Klarna", "Logz.io", 
    "Minute Media", "Mirakl", "Modern Health", "Monday.com", "MoonActive", "Moovit", "MyHeritage", "Otonomo", 
    "Utbrain", "Payoneer", "Pecan", "PlainID", "Planck", "Radwin", "Ravello", "Red Bend", "Samanage", 
    "SentinelOne", "Shopic", "Silk", "SilverFort", "SimilarWeb", "Soldo", "SundaySky", "TiS", "Transmit", 
    "TrueAccord", "Tufin", "Ujet", "Valens", "Vast", "Whereby", "Wiliot", "Wilocity", "Wolt", "Yotpo", "Zerto"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    investment_type = ''
    investment_name = ''
    investment_type_csv = ''

    if request.method == 'POST':
        # Handle corporation logo generation
        company_name = request.form.get('company_name')
        if company_name:
            wikipedia_url = get_wikipedia_url(company_name)
            if wikipedia_url:
                logo_url = get_company_logo_url(wikipedia_url)
                if logo_url:
                    return render_template('index.html', company_name=company_name, wikipedia_url=wikipedia_url, logo_url=logo_url, funds_list=funds_list, direct_investments_list=direct_investments_list)
                else:
                    return render_template('index.html', company_name=company_name, error="No logo found.", funds_list=funds_list, direct_investments_list=direct_investments_list)
            else:
                return render_template('index.html', company_name=company_name, error="No Wikipedia page found.", funds_list=funds_list, direct_investments_list=direct_investments_list)
        
        # Handle investment logo generation
        investment_type = request.form.get('investment_type')
        investment_name = request.form.get('investment_name')
        if investment_type and investment_name:
            investment_link, investment_logo_url = get_investment_image_link(investment_name, investment_type)
            if investment_logo_url:
                return render_template('index.html', investment_name=investment_name, investment_type=investment_type, investment_link=investment_link, investment_logo_url=investment_logo_url, funds_list=funds_list, direct_investments_list=direct_investments_list)
            else:
                return render_template('index.html', investment_name=investment_name, investment_type=investment_type, error=investment_link, funds_list=funds_list, direct_investments_list=direct_investments_list)

        # Handle CSV generation
        generate_csv = request.form.get('generate_csv')
        if generate_csv:
            investment_type_csv = request.form.get('investment_type_csv')
            data = get_all_investments_details(investment_type_csv)
            df = pd.DataFrame(data)
            output = io.BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return send_file(output, mimetype='text/csv', as_attachment=True, download_name=f'{investment_type_csv}_investments.csv')

    return render_template('index.html', funds_list=funds_list, direct_investments_list=direct_investments_list, investment_type=investment_type, investment_name=investment_name, investment_type_csv=investment_type_csv)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
