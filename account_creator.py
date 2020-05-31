from requet import Requet, Log
import re
import time



# ========================================== #
#			ENTREZ LES INFOS ICI			 #
# ========================================== #

title = "mr" #or mme
firstName = "Valentin"
lastName = "Coat"
email = "valentincoat@hotmail.fr"
password = "password1234" #use letter + numbers
phone = "0611245689" # dont put '.'
bday = "17.10.1999" # DD.MM.YYYY

"""
Probleme majeur rencontré : la requete POST pour envoyer les infos du compte n'est pas valide.
Le serveur retourne un code 302.
Solutions envisagées : - Le token csrf n'est pas valide (corrigé)
					   - Les headers ne sont pas bons / il manque des headers (corrigé)
					   - Les requetes s'enchainent trop vite (corrigé)
Le probleme venait des tokens csrf, qui ne comportait pas le '=' a la fin et qui
était remplacé par %3D
Le nombre de requetes ainsi que le temps pourraient largement etre diminués, je n'ai pas fait de tests poussés.
"""



print(r'''   _____       _      _
  / ____|     | |    | |
 | (___   ___ | | ___| |__   _____  __
  \___ \ / _ \| |/ _ \ '_ \ / _ \ \/ /
  ____) | (_) | |  __/ |_) | (_) >  <
 |_____/ \___/|_|\___|_.__/ \___/_/\_\

	  Account creator

 /!\ Verifiez les infos dans le fichier
  	account_creator.py  /!\
 ''')

input("Appuyez sur une touche pour commencer")

print('\033[94m' + "\n\nConnexion au site www.solebox.com...")

solebox = Requet(True, 'www.solebox.com')

solebox.useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'

solebox.debug = False

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

solebox.requet('/en_FR/login',
	headers={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Referer': 'https://www.solebox.com/en_FR',
		'Upgrade-Insecure-Requests': '1'
	}

)

time.sleep(5)

print('\033[94m' + "Creation du compte...")

response = solebox.requet('/en_FR/registration?rurl=1',
	headers={
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Referer': 'https://www.solebox.com/en_FR/login',
		'Upgrade-Insecure-Requests': '1',
		'TE': 'Trailers'
	}
)

time.sleep(20) # Pourrait etre plus court

csrf_token = re.search(r'(name=\"csrf_token\" value=\")(.+)(=\"/>)',response).group(2)


requetbody = "dwfrm_profile_register_title=" + title + "&dwfrm_profile_register_firstName=" + firstName + "&dwfrm_profile_register_lastName=" + lastName + "&dwfrm_profile_register_email=" + email + "&dwfrm_profile_register_emailConfirm=" + email + "&dwfrm_profile_register_password=" + password + "&dwfrm_profile_register_passwordConfirm=" + password + "&dwfrm_profile_register_phone=" + phone + "&dwfrm_profile_register_birthday=" + bday + "&dwfrm_profile_register_acceptPolicy=true&csrf_token=" +csrf_token+"%3D"


post_response = solebox.requet('/on/demandware.store/Sites-solebox-Site/en_FR/Account-SubmitRegistration?rurl=1&format=ajax',
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

if("errorMessage" in post_response):
	print('\033[91m' + "La creation du compte a echoué. Vérifiez les informations")
else:
	print('\033[92m' + "\n\nCompte créé ! Verifiez vos e-mails");
