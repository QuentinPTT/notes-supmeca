from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def getMarks(username, password):
    with requests.Session() as s:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://scolarite.supmeca.fr/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = {
            'username': username,
            'password': password,
            'j_idt27': '',
        }
        s.post('https://scolarite.supmeca.fr/login', data=data)

        # Naviguer jusqu'à la page souhaitée et extraire les données
        cookies = {
            'JSESSIONID': s.cookies["JSESSIONID"],
        }
        response = requests.get('https://scolarite.supmeca.fr/#', cookies=cookies, headers=headers)
        
        soup = BeautifulSoup(response.text, "html.parser")
        formid = soup.find('input', id='form:idInit').get('value')
        javax = soup.find('input', id='j_id1:javax.faces.ViewState:0').get('value')
        
        data = {
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source': 'form:j_idt52',
            'javax.faces.partial.execute': 'form:j_idt52',
            'javax.faces.partial.render': 'form:sidebar',
            'form:j_idt52': 'form:j_idt52',
            'webscolaapp.Sidebar.ID_SUBMENU': 'submenu_574144',
            'form': 'form',
            'form:largeurDivCenter': '902',
            'form:idInit': formid,
            'form:sauvegarde': '',
            'form:j_idt755_focus': '',
            'form:j_idt755_input': '43758',
            'javax.faces.ViewState': javax,
        }
        response = s.post('https://scolarite.supmeca.fr/faces/MainMenuPage.xhtml', cookies=cookies, headers=headers, data=data)
        soup = BeautifulSoup(response.text, "html.parser")
        
        data2 = {
            'form': 'form',
            'form:largeurDivCenter': '902',
            'form:idInit': formid,
            'form:sauvegarde': '',
            'form:j_idt755_focus': '',
            'form:j_idt755_input': '43758',
            'javax.faces.ViewState': javax,
            'form:sidebar': 'form:sidebar',
            'form:sidebar_menuid': '4_0',
        }
        response = s.post('https://scolarite.supmeca.fr/faces/MainMenuPage.xhtml', cookies=cookies, headers=headers, data=data2)
        soup = BeautifulSoup(response.text, "html.parser")
        
        response = s.get('https://scolarite.supmeca.fr/faces/LearnerNotationListPage.xhtml', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    markData = soup.find('tbody')
    notes=[]
    for tr in markData.children:
        notes.append({
            "date": tr.contents[0].text,
            "anagramme": tr.contents[1].text,
            "titre": tr.contents[2].text,
            "note": tr.contents[3].text,
            "intervenants": tr.contents[6].text  
        })
    return notes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    try: 
        result = getMarks(username, password)
        return render_template('dashboard.html', result=result)
    except:
        return render_template('index.html', result="Mot de passe ou identifiant incorrect")
    


if __name__ == '__main__':
    app.run(debug=True)