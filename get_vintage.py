import requests
from bs4 import BeautifulSoup

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

def get_investment_image_link(investment_name, investment_type):
    url = "https://www.vintage-ip.com/portfolio/"
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')

    if investment_type == 'fund':
        investments_list = funds_list
        investment_class = 'portfolio-item active'
    else:
        investments_list = direct_investments_list
        investment_class = 'portfolio-item'

    try:
        index = investments_list.index(investment_name)
    except ValueError:
        return f"Investment '{investment_name}' not found in the list.", None

    portfolio_section = soup.find('section', {'class': 'portfolio-section'})
    if not portfolio_section:
        return "Portfolio section not found.", None

    container = portfolio_section.find('div', {'class': 'container'})
    if not container:
        return "Container div not found.", None

    portfolio_wrapper = container.find('ul', {'class': 'portfolio-wrapper'})
    if not portfolio_wrapper:
        return "Portfolio wrapper not found.", None

    investment_items = portfolio_wrapper.find_all('li')
    if not investment_items:
        return "No investment items found.", None

    fund_items = [item for item in investment_items if 'active' in item.get('class', []) and 'portfolio-item' in item.get('class', [])]
    direct_items = [item for item in investment_items if 'portfolio-item' in item.get('class', []) and 'active' not in item.get('class', [])]

    if investment_type == 'fund':
        if index >= len(fund_items):
            return f"Fund '{investment_name}' not found in the portfolio.", None
        investment_item = fund_items[index]
    else:
        if index >= len(direct_items):
            return f"Direct Investment '{investment_name}' not found in the portfolio.", None
        investment_item = direct_items[index]

    investment_link = investment_item.find('a')
    if not investment_link or 'href' not in investment_link.attrs:
        return f"Link for '{investment_name}' not found.", None

    logo_div = investment_item.find('div', {'class': 'portfolio-logo'})
    if not logo_div:
        return f"Logo div for '{investment_name}' not found.", None

    logo_img = logo_div.find('img')
    if not logo_img or 'src' not in logo_img.attrs:
        return f"Logo image for '{investment_name}' not found.", None

    logo_src = logo_img['src']
    if not logo_src.startswith('http'):
        logo_src = f"https://www.vintage-ip.com{logo_src}"
    return investment_link['href'], logo_src

def get_all_investments_details(investment_type):
    investment_list = funds_list if investment_type == 'fund' else direct_investments_list
    data = []
    for investment_name in investment_list:
        investment_link, investment_logo_url = get_investment_image_link(investment_name, investment_type)
        data.append({'URL': investment_link, 'Logo Link': investment_logo_url})
    return data
