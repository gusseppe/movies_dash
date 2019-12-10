""""
    Configuraciones iniciales para la aplicacion.
"""

mongo_activated = False # Si es True entonces usara mongo, sino, usara json (archivo local).
interval_update = 1 * 86400  # El numero de segundos que esperara la aplicacion para actualizarse.
update_activated = False # Si toda la base de datos se actualizara ahora y posteriormente.
title = 'UC3M project: The best movie for you' # Titulo esquina superior izquierda
number_of_tweets = 50
# sub_title = 'Elige tu pelicula' # Subtitulo
# info_app = 'Applicacion que muestra estadisticas utiles de peliculas en carteleras locales'

team = [ # Equipo involucrado en el proyecto
    {'name': 'Ricardo Lesevic',
     'site': 'wwww.google.com'},
    {'name': 'Julissa Gutierrez',
     'site': 'wwww.google.com'},
    #    {'name': 'Carlos Ninaquispe',
    # 'site': 'wwww.google.com'},
]

# TWITTER CREDENTIALS
consumer_key = 'Mohss6WlaoMRQIR8nyBwvyVJA'
consumer_secret = 'EhPQRFNgKDWZl6T49oFwaZMDSJzCCvcKTICmAh2BIuGpHGU9qf'
access_token = '701455511233961984-RW2KvnBcNbNQaBy7WJ8qVk32j4aF9CL'
access_token_secret = 'Dw0w3U1JdT1e0IFJAtJenZNoYsVaS0RmacHyfCoTxjBuK'

# Tiempo API AEMET
weather_api = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJoYWNrZXJzdmxjQGdtYWlsLmNvbSIsImp0aSI6IjViYjIwMzA3LWQyNmMtNDM5Yi1hN2U2LTlmNmJjMTM1ODcxNiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTczODk3NTQyLCJ1c2VySWQiOiI1YmIyMDMwNy1kMjZjLTQzOWItYTdlNi05ZjZiYzEzNTg3MTYiLCJyb2xlIjoiIn0.b65-UpwrSBLY1P3XoBPw8Fi4OZjk2ee9yCt7g9Y4kzM'

# Constante
number_of_movies = 4 # NO CAMBIAR. Refrescar pagina para obtener nuevas peliculas
