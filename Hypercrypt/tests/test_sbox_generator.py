# tests/test_sbox_generator.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.sbox_generator import SBoxGenerator

def test_sbox_generation_and_inversion():
    chaos = [12, 34, 56, 78, 90, 123, 45, 67]

    # Génération de la S-box et de son inverse
    sbox = SBoxGenerator.generate_sbox(chaos)
    inverse = SBoxGenerator.invert_sbox(sbox)

    # Vérification 1 : sbox est une permutation de 0 à 15
    assert sorted(sbox) == list(range(16)), "S-box invalide : pas une permutation complète"

    # Vérification 2 : sbox[inverse[i]] == i pour tout i
    for i in range(16):
        assert sbox[inverse[i]] == i, f"Inverse incorrect pour i={i}"

    print("✅ test_sbox_generation_and_inversion passed")

if __name__ == "__main__":
    test_sbox_generation_and_inversion()
