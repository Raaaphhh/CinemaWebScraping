from scraper import CineScraper

url = "https://cinecentre.fr/FR/9/cinema-cinecentre-dreux.html"
scraper = CineScraper(url)

films = scraper.get_film()

print("Choisis un film pour voir ses horaires :")
for i, film in enumerate(films, start=1):
    print(f"{i}. {film['titre']}")

choix = int(input("Numéro du film choisi : "))
film_choisi = films[choix - 1]

url_film = scraper.get_CreateNewUrl(film_choisi["code"], film_choisi["titre"])
scraper.get_GetHorraire(url_film)