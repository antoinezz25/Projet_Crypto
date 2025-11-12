import random

mehdi_publique = (6603, 49087)
mehdi_privee = (42467, 49087)

antoine_publique = (6983, 18281)
antoine_privee = (647, 18281)

baptiste_publique = (30509, 36863)
baptiste_privee = (21029, 36863)

def pgcd(a, b):
    """Calcule le Plus Grand Commun Diviseur de a et b"""
    while b != 0:
        a, b = b, a % b
    return a

def euclide(a, b):
    """Algorithme d'Euclide étendu"""
    if b == 0:
        return (a, 1, 0)
    else:
        q = a // b
        r = a % b
        pgcd_val, u, v = euclide(b, r)
        return (pgcd_val, v, u - q * v)

def inverseModulaire(e, m):
    # Vérifier que e et m sont premiers entre eux
    if pgcd(e, m) != 1:
        return None
    r, u, v = euclide(e, m)
    # L'inverse modulaire est u modulo m
    return u % m

def estPremier(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def premierAleatoire(inf, lg):
    L = []
    for i in range(inf, lg + 1):
        L.append(i)
    random.shuffle(L)
    while len(L) > 0:
        p = L.pop()
        if estPremier(p):
            return p

def premierAleatoireAvec(n):
    L = []
    for i in range(2, n - 1):
        L.append(i)
    random.shuffle(L)
    while len(L) > 0:
        p = L.pop()
        if pgcd(p, n) == 1:
            return p
    return None

def expoModulaire(a, n, m):
    if n == 0:
        return 1
    if n % 2 == 0:
        temp = expoModulaire(a, n // 2, m)
        return (temp * temp) % m
    else:
        temp = expoModulaire(a, n - 1, m)
        return (a * temp) % m

def expoModulaire2(x, e, n):
    if e == 0:
        return 1
    f = expoModulaire2(x, e // 2, n)
    if e % 2 == 0:
        return (f * f) % n
    else:
        return (x * f * f) % n

def choixCle(inf, lg):
    p = premierAleatoire(inf, inf + lg)
    q = premierAleatoire(p + 1, p + lg + 1)
    m = (p - 1) * (q - 1)
    e = premierAleatoireAvec(m)
    return e, p, q

def clePublique(p, q, e):
    n = p * q
    return (e, n)

def clePrivee(p, q, e):
    n = p * q
    m = (p - 1) * (q - 1)
    d = inverseModulaire(e, m)
    return (d, n)

def codageRSA(m, cle):
    if m < 0 or m >= cle[1]:
        return None
    return expoModulaire(m, cle[0], cle[1])

def decodageRSA(c, cle):
    if c < 0 or c >= cle[1]:
        return None
    return expoModulaire(c, cle[0], cle[1])


# ===== FONCTIONS POUR CHIFFRER/DECHIFFRER DU TEXTE =====

def chiffrerTexte(texte, cle_publique):
    """Chiffre un texte complet avec RSA"""
    texte_chiffre = []
    for char in texte:
        code = ord(char)
        chiffre = codageRSA(code, cle_publique)
        if chiffre is None:
            print(f"Erreur: caractere '{char}' trop grand pour la cle")
            return None
        texte_chiffre.append(chiffre)
    return texte_chiffre

def dechiffrerTexte(texte_chiffre, cle_privee):
    """Dechiffre un texte chiffre avec RSA"""
    texte_clair = ""
    for chiffre in texte_chiffre:
        code = decodageRSA(chiffre, cle_privee)
        if code is None:
            print("Erreur de dechiffrement")
            return None
        texte_clair += chr(code)
    return texte_clair


# ===== FONCTIONS POUR CHIFFRER/DECHIFFRER DES FICHIERS =====

def chiffrerFichier(fichier_entree, fichier_sortie, cle_publique):
    """Chiffre un fichier texte"""
    try:
        with open(fichier_entree, 'r', encoding='utf-8') as f:
            contenu = f.read()
        print(f"Fichier lu: {len(contenu)} caracteres")
        print("Chiffrement en cours...")
        contenu_chiffre = chiffrerTexte(contenu, cle_publique)
        if contenu_chiffre is None:
            return False
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            f.write(str(contenu_chiffre))
        print(f"Fichier chiffre sauvegarde dans: {fichier_sortie}")
        return True
    except FileNotFoundError:
        print(f"Fichier '{fichier_entree}' non trouve!")
        return False
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def dechiffrerFichier(fichier_entree, fichier_sortie, cle_privee):
    """Dechiffre un fichier"""
    try:
        with open(fichier_entree, 'r', encoding='utf-8') as f:
            contenu = f.read()
        contenu_chiffre = eval(contenu)
        print(f"Fichier lu: {len(contenu_chiffre)} nombres chiffrees")
        print("Dechiffrement en cours...")
        contenu_clair = dechiffrerTexte(contenu_chiffre, cle_privee)
        if contenu_clair is None:
            return False
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            f.write(contenu_clair)
        print(f"Fichier dechiffre sauvegarde dans: {fichier_sortie}")
        return True
    except FileNotFoundError:
        print(f"Fichier '{fichier_entree}' non trouve!")
        return False
    except Exception as e:
        print(f"Erreur: {e}")
        return False


# ===== PROGRAMME PRINCIPAL =====

if __name__ == "__main__":
    print("=" * 60)
    print(" " * 15 + "MESSAGERIE CHIFFREE RSA")
    print("=" * 60)
    print()

    print("Qui es-tu?")
    print("1. Antoine")
    print("2. Baptiste")
    print("3. Mehdi")

    choix_user = input("\nTon choix (1-3): ").strip()

    if choix_user == "1":
        mon_nom = "Antoine"
        ma_cle_pub = antoine_publique
        ma_cle_priv = antoine_privee
    elif choix_user == "2":
        mon_nom = "Baptiste"
        ma_cle_pub = baptiste_publique
        ma_cle_priv = baptiste_privee
    elif choix_user == "3":
        mon_nom = "Mehdi"
        ma_cle_pub = mehdi_publique
        ma_cle_priv = mehdi_privee
    else:
        print("Choix invalide!")
        raise SystemExit(1)

    print(f"\nConnecte en tant que: {mon_nom}")
    print(f"Ta cle publique: {ma_cle_pub}")
    print(f"Ta cle privee: {ma_cle_priv}")
    print()

    print("=" * 60)
    print("Mode interactif:")
    print("-" * 60)

    while True:
        print(f"\n[{mon_nom}] Que veux-tu faire?")
        print("1. Chiffrer un message (pour envoyer)")
        print("2. Dechiffrer un message (recu)")
        print("3. Afficher les cles publiques")
        print("4. Changer d'utilisateur")
        print("5. Quitter")

        choix = input("\nVotre choix (1-5): ").strip()

        if choix == "1":
            print("\n" + "-" * 60)
            print("CHIFFRER UN MESSAGE")
            print("-" * 60)
            print("\nA qui veux-tu envoyer?")

            destinataires = []
            if mon_nom != "Antoine":
                print("1. Antoine")
                destinataires.append(("Antoine", antoine_publique))
            if mon_nom != "Baptiste":
                print(f"{len(destinataires) + 1}. Baptiste")
                destinataires.append(("Baptiste", baptiste_publique))
            if mon_nom != "Mehdi":
                print(f"{len(destinataires) + 1}. Mehdi")
                destinataires.append(("Mehdi", mehdi_publique))

            choix_dest = input("\nChoix: ").strip()
            try:
                idx = int(choix_dest) - 1
                if 0 <= idx < len(destinataires):
                    nom_dest, cle_pub_dest = destinataires[idx]
                    msg = input(f"\nTon message pour {nom_dest}: ")
                    print(f"\nChiffrement avec la cle publique de {nom_dest}...")
                    chiffre = chiffrerTexte(msg, cle_pub_dest)
                    if chiffre:
                        print("\nMESSAGE CHIFFRE (copie et envoie sur Discord):")
                        print("-" * 60)
                        print(chiffre)
                        print("-" * 60)
                else:
                    print("Choix invalide!")
            except Exception:
                print("Erreur!")

        elif choix == "2":
            print("\n" + "-" * 60)
            print("DECHIFFRER UN MESSAGE")
            print("-" * 60)
            print("\nColle le message chiffre (la liste de nombres):")
            try:
                nombres = input("> ").strip()
                chiffre = eval(nombres)
                print("\nDechiffrement avec ta cle privee...")
                dechiffre = dechiffrerTexte(chiffre, ma_cle_priv)
                if dechiffre:
                    print("\nMESSAGE DECHIFFRE:")
                    print("-" * 60)
                    print(f"'{dechiffre}'")
                    print("-" * 60)
            except Exception as e:
                print(f"Erreur: {e}")

        elif choix == "3":
            print("\n" + "-" * 60)
            print("CLES PUBLIQUES")
            print("-" * 60)
            print(f"Antoine  : {antoine_publique}")
            print(f"Baptiste : {baptiste_publique}")
            print(f"Mehdi    : {mehdi_publique}")

        elif choix == "4":
            print("\n" + "-" * 60)
            print("CHANGER D'UTILISATEUR")
            print("-" * 60)
            print("Qui veux-tu etre maintenant?")
            print("1. Antoine")
            print("2. Baptiste")
            print("3. Mehdi")
            choix_nouveau = input("\nTon choix (1-3): ").strip()
            if choix_nouveau == "1":
                mon_nom = "Antoine"
                ma_cle_pub = antoine_publique
                ma_cle_priv = antoine_privee
                print(f"\nTu es maintenant connecte en tant que: {mon_nom}")
                print(f"Ta cle publique: {ma_cle_pub}")
                print(f"Ta cle privee: {ma_cle_priv}")
            elif choix_nouveau == "2":
                mon_nom = "Baptiste"
                ma_cle_pub = baptiste_publique
                ma_cle_priv = baptiste_privee
                print(f"\nTu es maintenant connecte en tant que: {mon_nom}")
                print(f"Ta cle publique: {ma_cle_pub}")
                print(f"Ta cle privee: {ma_cle_priv}")
            elif choix_nouveau == "3":
                mon_nom = "Mehdi"
                ma_cle_pub = mehdi_publique
                ma_cle_priv = mehdi_privee
                print(f"\nTu es maintenant connecte en tant que: {mon_nom}")
                print(f"Ta cle publique: {ma_cle_pub}")
                print(f"Ta cle privee: {ma_cle_priv}")
            else:
                print("Choix invalide!")

        elif choix == "5":
            print(f"\nAu revoir {mon_nom}!")
            break
        else:
            print("\nChoix invalide!")
