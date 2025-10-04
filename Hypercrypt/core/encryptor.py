# core/encryptor.py
import numpy as np
from core.chaotic_system import HyperchaoticSystem6D
from core.bit_mixer import BitMixer
from core.sbox_generator import SBoxGenerator
from numpy.random import default_rng

class ImageEncryptor:
    def __init__(self, params):
        """
        params : dictionnaire contenant :
          - a, b, c, d, e, f : coefficients
          - x0, y0, z0, u0, v0, w0 : conditions initiales
          - h : pas de temps (facultatif)
          - seed : valeur entière pour la quantization (facultatif)
        """
        self.params = params
        self.seed = params.get("quant_seed", params.get("seed", None))
        self.system = HyperchaoticSystem6D(**{k: v for k, v in params.items() if k != "quant_seed"})
        self.rng = default_rng(self.seed)

    def _quantize_chaotic_bytes(self, chaotic_bytes):
        if self.seed is None:
            return chaotic_bytes
        # Exemple simple : remplace 20% des valeurs par du bruit aléatoire
        chaotic_bytes = chaotic_bytes.copy()
        total = len(chaotic_bytes)
        indices = self.rng.choice(total, size=total // 5, replace=False)
        chaotic_bytes[indices] = self.rng.integers(0, 256, size=len(indices), dtype=np.uint8)
        return chaotic_bytes

    def _regenerate_sboxes(self, chaotic_bytes):
        sbox1 = SBoxGenerator.generate_sbox(chaotic_bytes[:8])
        sbox2 = SBoxGenerator.generate_sbox(chaotic_bytes[8:16])
        inv1 = SBoxGenerator.invert_sbox(sbox1)
        inv2 = SBoxGenerator.invert_sbox(sbox2)
        return sbox1, sbox2, inv1, inv2

    def encrypt(self, image):
        h, w, c = image.shape
        assert c == 3, "Image RGB requise"

        # Étape 1 : génération du chaos
        required_bytes = h * w * 3 * 3  # 3 valeurs par pixel
        chaotic_bytes = self.system.generate_byte_sequence((required_bytes // 6) + 10)
        chaotic_bytes = np.array(chaotic_bytes[:required_bytes], dtype=np.uint8)
        chaotic_bytes = self._quantize_chaotic_bytes(chaotic_bytes)

        # Étape 2 : Bit-level mixing
        mixed_image = BitMixer.mix_image(image, chaotic_bytes)

        # Étape 3 : Génération des S-box
        sbox1, sbox2, _, _ = self._regenerate_sboxes(chaotic_bytes)

        # Étape 4 : Substitution via S-box
        encrypted = np.zeros_like(mixed_image, dtype=np.uint8)
        for i in range(h):
            for j in range(w):
                for k in range(3):  # R, G, B
                    val = mixed_image[i, j, k]
                    left, right = BitMixer.split_byte(val)
                    left = sbox2[left]
                    right = sbox1[right]
                    encrypted[i, j, k] = BitMixer.combine_halves(left, right)

        return encrypted, {"sbox1": sbox1, "sbox2": sbox2}

    def decrypt(self, encrypted_image, sbox1=None, sbox2=None, auto_recompute=False):
        h, w, c = encrypted_image.shape
        assert c == 3

        required_bytes = h * w * 3 * 3
        chaotic_bytes = self.system.generate_byte_sequence((required_bytes // 6) + 10)
        chaotic_bytes = np.array(chaotic_bytes[:required_bytes], dtype=np.uint8)
        chaotic_bytes = self._quantize_chaotic_bytes(chaotic_bytes)

        if auto_recompute:
            sbox1, sbox2, inv1, inv2 = self._regenerate_sboxes(chaotic_bytes)
        else:
            if sbox1 is None or sbox2 is None:
                raise ValueError("S-boxes nécessaires pour le déchiffrement.")
            inv1 = SBoxGenerator.invert_sbox(sbox1)
            inv2 = SBoxGenerator.invert_sbox(sbox2)

        # Étape 2 : Inverser substitution
        substituted = np.zeros_like(encrypted_image, dtype=np.uint8)
        for i in range(h):
            for j in range(w):
                for k in range(3):
                    val = encrypted_image[i, j, k]
                    left, right = BitMixer.split_byte(val)
                    left = inv2[left]
                    right = inv1[right]
                    substituted[i, j, k] = BitMixer.combine_halves(left, right)

        # Étape 3 : Inverser le bit-level mixing
        original = BitMixer.unmix_image(substituted, chaotic_bytes) # Reversible

        return original
