import random

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
    print(" " * 15 + "CHIFFREMENT RSA")
    print("=" * 60)
    print()
    
    # 1. Générer les clés
    print("1. Génération des clés RSA...")
    e, p, q = choixCle(100, 100)
    cle_pub = clePublique(p, q, e)
    cle_priv = clePrivee(p, q, e)
    
    print(f"   p = {p}")
    print(f"   q = {q}")
    print(f"   e = {e}")
    print(f"   Clé publique (e, n)  : {cle_pub}")
    print(f"   Clé privée (d, n)    : {cle_priv}")
    print()
    
    
  
    
    print()
    print("=" * 60)
    print()
    
    # Mode interactif
    print("Mode interactif:")
    print("-" * 60)
    
    while True:
        print("\nQue voulez-vous faire?")
        print("1. Chiffrer un nouveau message")
        print("2. Déchiffrer un message")
        print("3. Générer de nouvelles clés")
        print("4. Quitter")
        
        choix = input("\nVotre choix (1-4): ").strip()
        
        if choix == "1":
            msg = input("\nEntrez votre message à chiffrer: ")
            chiffre = chiffrerTexte(msg, cle_pub)
            if chiffre:
                print(f"\nMessage chiffré: {chiffre}")
                print(f"Taille: {len(chiffre)} nombres")
        
        elif choix == "2":
            print("\nEntrez les nombres chiffrés séparés par des espaces:")
            try:
                nombres = input("> ").strip()
                chiffre = [int(x) for x in nombres.split()]
                dechiffre = dechiffrerTexte(chiffre, cle_priv)
                if dechiffre:
                    print(f"\nMessage déchiffré: '{dechiffre}'")
            except:
                print("Erreur: format invalide")
        
        elif choix == "3":
            print("\nGénération de nouvelles clés...")
            e, p, q = choixCle(100, 100)
            cle_pub = clePublique(p, q, e)
            cle_priv = clePrivee(p, q, e)
            print(f"Clé publique : {cle_pub}")
            print(f"Clé privée   : {cle_priv}")
        
        elif choix == "4":
            print("\nAu revoir!")
            break
        
        else:
            print("\nChoix invalide!")