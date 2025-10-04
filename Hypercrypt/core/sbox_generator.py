import random
import numpy as np  # ← nécessaire pour la somme protégée

class SBoxGenerator:
    @staticmethod
    def generate_sbox(seed_bytes):
        """
        Génère une S-box dynamique (valeurs de 0 à 15 mélangées),
        à partir d'une liste d'octets pour introduire le chaos.
        """
        base = list(range(16))
        # Conversion en seed compatible + protection contre l’overflow
        seed_value = int(np.sum(seed_bytes, dtype=np.uint64))
        random.seed(seed_value)
        random.shuffle(base)
        return base

    @staticmethod
    def invert_sbox(sbox):
        """
        Génère la table inverse d'une S-box.
        """
        inverse = [0] * len(sbox)
        for i, val in enumerate(sbox):
            inverse[val] = i
        return inverse
