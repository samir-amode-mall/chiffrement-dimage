import numpy as np

class HyperchaoticSystem6D:
    def __init__(self, a, b, c, d, e, f, x0, y0, z0, u0, v0, w0, h=0.001):
        # Coefficients (clé du système)
        self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f
        # Conditions initiales (clé aussi)
        self.state = np.array([x0, y0, z0, u0, v0, w0], dtype=np.float64)
        self.h = h  # pas de temps

    def _derivatives(self, state):
        x1, x2, x3, x4, x5, x6 = state
        a, b, c, d, e, f = self.a, self.b, self.c, self.d, self.e, self.f

        dx1 = (a * x2 - b * x3) * x6
        dx2 = (b * x3 - c * x4) * x1
        dx3 = (c * x4 - d * x5) * x2
        dx4 = (d * x5 - e * x6) * x3
        dx5 = (e * x6 - f * x1) * x4
        dx6 = (f * x1 - a * x2) * x5

        return np.array([dx1, dx2, dx3, dx4, dx5, dx6])

    def _rk4_step(self, state):
        h = self.h
        k1 = self._derivatives(state)
        k2 = self._derivatives(state + 0.5 * h * k1)
        k3 = self._derivatives(state + 0.5 * h * k2)
        k4 = self._derivatives(state + h * k3)
        next_state = state + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        # Clamp les valeurs extrêmes
        next_state = np.clip(next_state, -1e6, 1e6)

        # Vérifie si NaN ou inf
        if not np.all(np.isfinite(next_state)):
            raise ValueError("Overflow or NaN detected in hyperchaotic system")

        return next_state

    def generate_sequence(self, length):
        sequence = []
        state = self.state.copy()
        for _ in range(length):
            state = self._rk4_step(state)
            sequence.append(state.copy())
        return np.array(sequence)  # shape (length, 6)

    def generate_byte_sequence(self, length):
        """
        Génére une séquence de valeurs dans [0, 255] à partir des 6 dimensions.
        """
        raw_seq = self.generate_sequence(length)
        byte_seq = []

        for state in raw_seq:
            # On utilise chaque dimension pour générer un entier dans [0, 255]
            for val in state:
                # Transforme les float en entiers 8 bits via normalisation
                norm = (np.tanh(val) + 1) / 2  # mappe vers [0, 1]
                byte = int(norm * 255) % 256
                byte_seq.append(byte)

        return byte_seq  # Liste de (length * 6) entiers entre 0 et 255
