# tests/test_bit_mixer.py

import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.bit_mixer import BitMixer
from core.chaotic_system import HyperchaoticSystem6D

def test_bit_mixing_on_image():
    # Image RGB 4x4 pixels remplie avec une valeur constante (ex: 120)
    image = np.full((4, 4, 3), 120, dtype=np.uint8)

    # Génère une séquence chaotique suffisante
    system = HyperchaoticSystem6D(
        a=36, b=3, c=28, d=0.5, e=2.1, f=1.1,
        x0=0.01, y0=0.02, z0=0.03, u0=0.04, v0=0.05, w0=0.06,
        h=0.001
    )
    # Chaque pixel RGB demande 3 chaos (R, G, B) × 3 bytes = 9 octets
    required_bytes = image.shape[0] * image.shape[1] * 3 * 3  # h × w × c × 3
    chaotic_bytes = system.generate_byte_sequence(length=(required_bytes // 6) + 1)

    # Applique le bit mixing
    mixed_image = BitMixer.mix_image(image, chaotic_bytes)

    # Vérifications
    assert mixed_image.shape == image.shape, "Erreur : dimensions modifiées"
    assert mixed_image.dtype == np.uint8, "Erreur : mauvais type de pixel"

    # S’assurer que l’image a changé (au moins un pixel)
    assert not np.array_equal(image, mixed_image), "L’image n’a pas été modifiée"

    print("✅ test_bit_mixing_on_image passed")

if __name__ == "__main__":
    test_bit_mixing_on_image()
