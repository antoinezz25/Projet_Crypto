import random

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


print(estPremier(15))
print(estPremier(17))

premierAleatoire(10, 50)
print(premierAleatoire(10, 50))