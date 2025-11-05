import random

mehdi_publique = (6603, 49087)
mehdi_privee = (41363, 49087)

antoine_publique = (6983, 18281)
antoine_privee = (10103, 18281)

baptiste_publique = (30509, 36863)
baptiste_privee = (23309, 36863)

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
    if pgcd(e, m) !=1 :
        return None
    
    r,u,v = euclide(e, m)

     # L'inverse modulaire est u modulo m
    # (u % m garantit que le résultat est dans l'intervalle [0, m-1])
    return u % m

def estPremier(n):
    if n <= 1 :
        return False
    for i in range(2,n):
        if n % i == 0 :
            return False
    return True

def premierAleatoire(inf,lg):
    L = []
    for i in range(inf, lg+1) :
        L.append(i)
    random.shuffle(L)
    while len(L) > 0 :
        p = L.pop()
        if estPremier(p) :
            return p
        
def premierAleatoireAvec(n):
    L = []
    for i in range(2, n-1) :
        L.append(i)
    random.shuffle(L)
    while len(L) > 0 :
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
    
def expoModulaire2(x,e,n):
    if e == 0 :
        return 1
    f = expoModulaire2(x, e//2, n)
    if e % 2 == 0 :
        return (f*f) % n
    else :
        return (x*f*f) % n

def choixCle(inf, lg):
    p = premierAleatoire(inf, inf+lg)
    q = premierAleatoire(p+1, p+lg+1)
    m = (p-1)*(q-1)
    e = premierAleatoireAvec(m)
    return e , p , q

def clePublique(p, q, e):
    n = p * q
    return (e, n)

def clePrivee(p, q, e):
    n = p * q
    m = (p-1)*(q-1)
    d = inverseModulaire(e, m)
    return (d, n)

def codageRSA(m , cle):
    if m < 0 or m >= cle[1]:
        return None
    return expoModulaire(m, cle[0], cle[1])

def decodageRSA(c , cle):
    if c < 0 or c >= cle[1]:
        return None
    return expoModulaire(c, cle[0], cle[1])


# ===== FONCTIONS POUR CHIFFRER/DÉCHIFFRER DU TEXTE =====

def chiffrerTexte(texte, cle_publique):
    """Chiffre un texte complet avec RSA"""
    # Convertir chaque caractère en nombre et le chiffrer
    texte_chiffre = []
    for char in texte:
        code = ord(char)  # Convertir caractère en code ASCII
        chiffre = codageRSA(code, cle_publique)
        if chiffre is None:
            print(f"Erreur: caractère '{char}' trop grand pour la clé")
            return None
        texte_chiffre.append(chiffre)
    return texte_chiffre

def dechiffrerTexte(texte_chiffre, cle_privee):
    """Déchiffre un texte chiffré avec RSA"""
    # Déchiffrer chaque nombre et le reconvertir en caractère
    texte_clair = ""
    for chiffre in texte_chiffre:
        code = decodageRSA(chiffre, cle_privee)
        if code is None:
            print(f"Erreur de déchiffrement")
            return None
        texte_clair += chr(code)  # Convertir code ASCII en caractère
    return texte_clair

# ===== PROGRAMME PRINCIPAL =====

if __name__ == "__main__":
    print("=" * 60)
    print(" " * 15 + "MESSAGERIE CHIFFRÉE RSA")
    print("=" * 60)
    print()
    
    # Choisir qui on est
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
        exit()
    
    print(f"\n✅ Connecté en tant que: {mon_nom}")
    print(f"🔓 Ta clé publique: {ma_cle_pub}")
    print(f"🔐 Ta clé privée: {ma_cle_priv}")
    print()
    
    # Mode interactif
    print("=" * 60)
    print("Mode interactif:")
    print("-" * 60)
    
    while True:
        print(f"\n[{mon_nom}] Que veux-tu faire?")
        print("1. Chiffrer un message (pour envoyer)")
        print("2. Déchiffrer un message (reçu)")
        print("3. Afficher les clés publiques")
        print("4. Quitter")
        
        choix = input("\nVotre choix (1-4): ").strip()
        
        if choix == "1":
            # CHIFFRER pour quelqu'un
            print("\n" + "-" * 60)
            print("CHIFFRER UN MESSAGE")
            print("-" * 60)
            print("\nÀ qui veux-tu envoyer?")
            
            # Afficher les destinataires possibles (sauf soi-même)
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
                    
                    print(f"\n🔒 Chiffrement avec la clé publique de {nom_dest}...")
                    chiffre = chiffrerTexte(msg, cle_pub_dest)
                    
                    if chiffre:
                        print(f"\n✅ MESSAGE CHIFFRÉ (copie et envoie sur Discord):")
                        print("─" * 60)
                        print(chiffre)
                        print("─" * 60)
                else:
                    print("❌ Choix invalide!")
            except:
                print("❌ Erreur!")
        
        elif choix == "2":
            # DÉCHIFFRER avec MA clé privée
            print("\n" + "-" * 60)
            print("DÉCHIFFRER UN MESSAGE")
            print("-" * 60)
            print("\nColle le message chiffré (la liste de nombres):")
            
            try:
                nombres = input("> ").strip()
                chiffre = eval(nombres)  # Convertir la liste
                
                print(f"\n🔓 Déchiffrement avec ta clé privée...")
                dechiffre = dechiffrerTexte(chiffre, ma_cle_priv)
                
                if dechiffre:
                    print(f"\n✅ MESSAGE DÉCHIFFRÉ:")
                    print("─" * 60)
                    print(f"'{dechiffre}'")
                    print("─" * 60)
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        elif choix == "3":
            # AFFICHER LES CLÉS
            print("\n" + "-" * 60)
            print("CLÉS PUBLIQUES")
            print("-" * 60)
            print(f"Antoine  : {antoine_publique}")
            print(f"Baptiste : {baptiste_publique}")
            print(f"Mehdi    : {mehdi_publique}")
        
        elif choix == "4":
            print(f"\n👋 Au revoir {mon_nom}!")
            break
        
        else:
            print("\n❌ Choix invalide!")