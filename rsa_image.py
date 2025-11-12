# -*- coding: utf-8 -*-
"""
Script utilitaire pour générer des images à partir d'un chiffrement RSA
utilisant les fonctions définies dans `RSA.py`.

Génère :
 - `cipher_pixels.png` : représentation en niveaux de gris des nombres chiffrés
   (chaque nombre est réduit modulo 256 pour obtenir un octet/pixel).
 - `cipher_report.png` : image contenant le message clair et la liste des nombres
   chiffrés (format texte), utile pour inspection.

Usage :
    python3 rsa_image.py

Ce script crée des clés temporaires, chiffre un message d'exemple et produit
les deux images dans le répertoire courant.
"""

from math import ceil, sqrt
from PIL import Image, ImageDraw, ImageFont
from RSA import choixCle, clePublique, chiffrerTexte

# --- Configuration ---
PLAINTEXT = "Bonjour, ceci est un test du chiffrement RSA en image !"
PIXEL_IMAGE_PATH = "cipher_pixels.png"
REPORT_IMAGE_PATH = "cipher_report.png"
# largeur souhaitée pour l'image de pixels (None -> carré automatique)
DESIRED_WIDTH = None


def make_pixel_image_from_cipher(cipher_list, out_path, width=None):
    """Crée une image en niveaux de gris où chaque pixel = chiffre % 256.

    - cipher_list : liste d'entiers
    - width : si None, on prend la largeur qui rend l'image la plus carrée
    """
    # Convertir en valeurs 0..255
    pixels = [c % 256 for c in cipher_list]
    n = len(pixels)
    if n == 0:
        raise ValueError("La liste chiffrée est vide")

    if width is None:
        width = int(ceil(sqrt(n)))
    height = int(ceil(n / width))

    # Padding
    total = width * height
    if total > n:
        pixels += [0] * (total - n)

    img = Image.new("L", (width, height))
    img.putdata(pixels)
    img.save(out_path)
    return out_path


def make_report_image(plaintext, cipher_list, out_path, width=1200, margin=20):
    """Crée une image contenant le texte clair et le texte chiffré.
    Le texte chiffré est présenté sur plusieurs lignes si nécessaire.
    """
    # Préparer le texte
    header = "Message clair :"
    body_plain = plaintext

    header2 = "Message chiffré (liste de nombres) :"
    # Représenter la liste chiffrée sous forme de lignes de 10 nombres
    nums_per_line = 8
    lines = []
    for i in range(0, len(cipher_list), nums_per_line):
        chunk = cipher_list[i:i+nums_per_line]
        lines.append(" ".join(str(x) for x in chunk))
    body_cipher = "\n".join(lines)

    # Choisir une police basique
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except Exception:
        font = ImageFont.load_default()

    # Estimer la taille de l'image en utilisant textbbox (compatible Pillow)
    tmp = Image.new("RGB", (width, 10), color=(255,255,255))
    draw_tmp = ImageDraw.Draw(tmp)
    def text_height(draw_obj, text, font):
        bbox = draw_obj.textbbox((0, 0), text, font=font)
        return bbox[3] - bbox[1]

    y = margin
    x = margin
    # mesurer et accumuler hauteur
    y += text_height(draw_tmp, header, font) + 6
    y += text_height(draw_tmp, body_plain, font) + 12
    y += text_height(draw_tmp, header2, font) + 6

    # mesurer chaque ligne du cipher
    for line in lines:
        y += text_height(draw_tmp, line, font) + 4

    height = max(y + margin, 200)

    img = Image.new("RGB", (width, height), color=(255,255,255))
    draw = ImageDraw.Draw(img)
    y = margin
    draw.text((x, y), header, fill=(0,0,0), font=font)
    y += text_height(draw, header, font) + 6
    draw.text((x, y), body_plain, fill=(0,0,0), font=font)
    y += text_height(draw, body_plain, font) + 12
    draw.text((x, y), header2, fill=(0,0,0), font=font)
    y += text_height(draw, header2, font) + 6

    for line in lines:
        draw.text((x, y), line, fill=(0,0,0), font=font)
        y += text_height(draw, line, font) + 4

    img.save(out_path)
    return out_path


def main():
    # Générer des clés (petits nombres pour la démonstration rapide)
    e, p, q = choixCle(100, 100)
    cle_pub = clePublique(p, q, e)

    print("Clé publique utilisée :", cle_pub)
    print("Clé privée (générée mais non affichée ici)")

    # Chiffrer le message
    cipher = chiffrerTexte(PLAINTEXT, cle_pub)
    if cipher is None:
        print("Erreur lors du chiffrement")
        return

    print("Message chiffré ({} nombres)".format(len(cipher)))

    # Créer l'image de pixels
    w = DESIRED_WIDTH
    try:
        pimg = make_pixel_image_from_cipher(cipher, PIXEL_IMAGE_PATH, width=w)
        print("Image de pixels sauvegardée ->", pimg)
    except Exception as exc:
        print("Erreur création image de pixels:", exc)

    # Créer l'image rapport
    try:
        rimg = make_report_image(PLAINTEXT, cipher, REPORT_IMAGE_PATH)
        print("Image rapport sauvegardée ->", rimg)
    except Exception as exc:
        print("Erreur création image rapport:", exc)


if __name__ == "__main__":
    main()
