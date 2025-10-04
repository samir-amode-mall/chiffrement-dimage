# tests/test_encryptor.py

import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.encryptor import ImageEncryptor

def test_encrypt_decrypt_pipeline():
    # Génère une image RGB 8x8 avec un motif simple
    image = np.tile([[100, 150, 200]], (8, 8, 1)).astype(np.uint8)

    # Paramètres chaotiques
    params = {
        "a": 36, "b": 3, "c": 28, "d": 0.5, "e": 2.1, "f": 1.1,
        "x0": 0.01, "y0": 0.02, "z0": 0.03,
        "u0": 0.04, "v0": 0.05, "w0": 0.06,
        "h": 0.001
    }

    # Encryption
    encryptor = ImageEncryptor(params)
    encrypted, key_info = encryptor.encrypt(image)

    # Assure que l’image est modifiée
    assert not np.array_equal(image, encrypted), "Erreur : image chiffrée identique à l’originale"

    # Décryption
    decrypted = encryptor.decrypt(encrypted, key_info["sbox1"], key_info["sbox2"])

    # Assure que l’image d’origine est retrouvée parfaitement
    assert np.array_equal(image, decrypted), "Erreur : image déchiffrée différente de l’originale"

    print("✅ test_encrypt_decrypt_pipeline passed")

if __name__ == "__main__":
    test_encrypt_decrypt_pipeline()
