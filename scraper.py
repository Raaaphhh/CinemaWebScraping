import requests
import unicodedata
import re
from bs4 import BeautifulSoup

class CineScraper: 
    def __init__ (self, url): 
        self.url = url
        self.soup = self.get_soup()

    #pour gerer les liens gpt me la donné 
    def slugify(self, text):
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
        text = re.sub(r"[^a-zA-Z0-9\s-]", "", text)
        text = re.sub(r"[\s]+", "-", text)
        return text.lower()
        
    def get_soup(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            print(f"Connexion réussie à {self.url}")
            return BeautifulSoup(response.text, "html.parser")
        else:
            raise Exception(f"Erreur HTTP : {response.status_code}")
        
        
    def get_film(self): 
        film = []
        balisesHtml = self.soup.find_all("a", class_ = "btn btn-erakys btn-vignette my-2 my-sm-0 bt--horaire")

        for a in balisesHtml:
            href = a.get("href")
            if href and "fiche-film-cinema" in href: 
                parts = href.split("/")
                code = parts[5] 
                slug = parts[6].replace("html", "")
                titre = slug.replace("-", " ").title()

                film.append({"titre" : titre, "code": code})
        return film
    
    def get_CreateNewUrl(self, code, titre):
        UrlBase = "https://cinecentre.fr/FR/fiche-film-cinema/"
        slug = self.slugify(titre)
        return f"{UrlBase}{code}/{slug}.html"
    
    def get_GetHorraire(self, urlfilm): 
        response = requests.get(urlfilm)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            jours = soup.find_all("span", class_="cache-xs")
            datejour = soup.find_all("span", class_="jour-mob")
            horaires_par_jour = self.get_extraction_horraires(soup)

            for i in range(min(len(jours), len(datejour))):
                nom_jour = jours[i].text.strip().capitalize()
                num_jour = datejour[i].text.strip()
                horaires = horaires_par_jour.get(nom_jour, [])

                print(f"\n📅 {nom_jour} {num_jour} :")
                if horaires:
                    for h in horaires:
                        print(f"   🕒 {h}")
                else:
                    print("   ❌ Aucune séance disponible")
        else:
            raise Exception(f"❌ Erreur HTTP : {response.status_code}")
        
    def get_extraction_horraires(self, soup):
        jours_codes = {
            "0727": "Lundi", ""
            "0728 color-heure": "Mardi",
            "0726": "Mercredi",
            "0723": "Jeudi",
            "0724 color-heure": "Vendredi",
            "0725": "Samedi",
            "0726 color-heure": "Dimanche"
        }

        horaires_par_jour = {}

        for code, nom_jour in jours_codes.items():
            blocs = soup.find_all("div", class_=f"col heure-seance {code}")
            horaires_du_jour = []

            for bloc in blocs:
                horaires = bloc.find_all("div", class_="container-seance")
                for horaire in horaires:
                    horaires_du_jour.append(horaire.text.strip())

            horaires_par_jour[nom_jour] = horaires_du_jour

        return horaires_par_jour