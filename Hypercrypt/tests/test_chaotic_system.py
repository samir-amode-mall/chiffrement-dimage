# tests/test_chaotic_system.py

import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.chaotic_system import HyperchaoticSystem6D



def test_generate_sequence_plot():
    # Initialisation avec des paramètres arbitraires
    system = HyperchaoticSystem6D(
        a=36, b=3, c=28, d=0.5, e=2.1, f=1.1,
        x0=0.1, y0=0.2, z0=0.3, u0=0.4, v0=0.5, w0=0.6
    )

    # Génère 1000 points
    seq = system.generate_sequence(1000)

    # Vérification : la forme du tableau
    assert seq.shape == (1000, 6), "La séquence n’a pas la bonne dimension."

    # Tracé de x vs y pour visualiser la dynamique chaotique
    x_vals = seq[:, 0]
    y_vals = seq[:, 1]

    plt.plot(x_vals, y_vals, lw=0.5)
    plt.title("Projection chaotique : x vs y")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

def test_generate_byte_sequence():
    system = HyperchaoticSystem6D(
        a=36, b=3, c=28, d=0.5, e=2.1, f=1.1,
        x0=0.01, y0=0.02, z0=0.03, u0=0.04, v0=0.05, w0=0.06,
        h=0.001
    )
    byte_seq = system.generate_byte_sequence(100)

    # Test de la longueur attendue (100 * 6)
    assert len(byte_seq) == 600, "La séquence d’octets ne fait pas la bonne longueur."

    # Test que tous les éléments sont bien dans [0, 255]
    assert all(0 <= b <= 255 for b in byte_seq), "Octet en dehors de l’intervalle [0, 255]"

    print("✅ test_generate_byte_sequence passed")



if __name__ == "__main__":
    test_generate_sequence_plot()
    test_generate_byte_sequence()
