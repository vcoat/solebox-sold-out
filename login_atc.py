from requet import Requet, Log
import re
import time
import sys

link = 'https://www.solebox.com/en_FR/p/carhartt_wip-s%2Fs_motown_orderform_t-shirt_-dusty_fuchsia-01770005.html'

"""
Pas de difficulté majeures ici.
Je ne me suis pas attardé sur comment recupérer le pid complet, ainsi que
l'optionId dans la requete post.
Les tailles sont récupérable dans le code source de la page d'un produit avec l'element data-sizes.
Le nombre de requetes ainsi que le temps pourraient largement etre diminués, je n'ai pas fait de tests poussés.
"""

# ========================================== #
#			ENTREZ LES INFOS ICI			 #
# ========================================== #

email = "monemail@hotmail.fr"
password = "monmotdepasse"

print(r'''   _____       _      _
  / ____|     | |    | |
 | (___   ___ | | ___| |__   _____  __
  \___ \ / _ \| |/ _ \ '_ \ / _ \ \/ /
  ____) | (_) | |  __/ |_) | (_) >  <
 |_____/ \___/|_|\___|_.__/ \___/_/\_\

	  Logging in + Add to Cart

 /!\ Verifiez les infos dans le fichier
  	login_atc.py  /!\
 ''')

input("Appuyez sur une touche pour commencer")

solebox = Requet(True, 'www.solebox.com')

solebox.useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'
solebox.debug = False

print('\033[94m' + "\n\nConnexion au site www.solebox.com...")

solebox.requet('/en_FR',
	headers={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'TE': 'Trailers'
	}
)


time.sleep(5)


response = solebox.requet('/en_FR/login',
	headers={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Referer': 'https://www.solebox.com/en_FR',
		'Upgrade-Insecure-Requests': '1'
	}
)

csrf_token = re.search(r'(name=\"csrf_token\" value=\")(.+)(=\"/>)',response).group(2)


requetbody = "dwfrm_profile_customer_email=" + email + "&dwfrm_profile_login_password=" + password + "&csrf_token=" + csrf_token + "%3D"

time.sleep(7)




post_response = solebox.requet('/en_FR/authentication?rurl=1&format=ajax',
    method="post",
	headers={
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'X-Requested-With': 'XMLHttpRequest',
		'Origin': 'https://www.solebox.com',
		'Connection':'keep-alive',
		'Referer': 'https://www.solebox.com/en_FR/registration?rurl=1',
		'TE': 'Trailers'
	},
    body=requetbody
)

if("User / Email unknown or wrong password" in post_response):
    print('\033[91m' + "Identifiants incorrect. Verifiez les informations")
    sys.exit()


time.sleep(7)

print('\033[94m' + "\n\nRecherche de l'article...")

response = solebox.requet('/en_FR/p/carhartt_wip-s%2Fs_motown_orderform_t-shirt_-dusty_fuchsia-01770005.html',
	headers={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
	}
)


time.sleep(10)


#"pid=0177000500000002&options=[{\\optionId:\\5903\\,\\selectedValueId\\:\M\\}]&quantity=1"
atcrequetbody = "pid=0177000500000002&options=[{\"optionId\":\"5903\",\"selectedValueId\":\"M\"}]&quantity=1"

print('\033[94m' + "Ajout de l'article au panier...")
time.sleep(20)

atc_post_response = solebox.requet('/en_FR/add-product?format=ajax',
    method="post",
	headers={
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'X-Requested-With': 'XMLHttpRequest',
		'Origin': 'https://www.solebox.com',
		'Connection':'keep-alive',
		'Referer': link,
		'TE': 'Trailers'
	},
    body=atcrequetbody
)

if("Product added to cart" in atc_post_response):
    print('\033[92m' + "\n\nProduit ajouté au panier !");
else:
    print('\033[91m' + "Impossible d'ajouter le produit au panier. Vérifiez le pid.")
