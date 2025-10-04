import numpy as np

class QuantumBitGenerator:
    def __init__(self, params):
        self.params = params
        self.h = params.get("h", 0.001)
        self.state = self._initialize_state()

    def _initialize_state(self):
        # Initialisation d'un état quantique complexe 6D : |psi> = [c1, c2, ..., c6]
        c = [complex(self.params[k % 6 + 6], self.params[(k + 1) % 6 + 6]) for k in range(6)]
        psi = np.array(c, dtype=np.complex128)
        psi /= np.linalg.norm(psi)  # normalisation
        return psi

    def _hamiltonian(self):
        # Matrice Hermitienne 6x6 simulée pour interférences quantiques
        rng = np.random.default_rng(seed=int(sum(self.params.values()) * 1e6) % (2**32))
        H = rng.standard_normal((6, 6)) + 1j * rng.standard_normal((6, 6))
        H = (H + H.conj().T) / 2  # rendre hermitien
        return H

    def _evolve(self, psi, H, steps):
        # Évolution unitaire simulée : psi -> exp(-iHt) |psi>
        dt = self.h
        for _ in range(steps):
            psi = psi - 1j * dt * H @ psi
            psi /= np.linalg.norm(psi)
        return psi

    def generate_bytes(self, n_bytes):
        psi = self.state.copy()
        H = self._hamiltonian()
        output = []

        while len(output) < n_bytes:
            psi = self._evolve(psi, H, steps=5)
            probs = np.abs(psi) ** 2  # probabilités de mesure
            scaled = (probs * 255).astype(int) % 256
            output.extend(scaled.tolist())

        return output[:n_bytes]
