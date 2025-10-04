import numpy as np
from scipy.stats import entropy as scipy_entropy

class ImageMetrics:
    @staticmethod
    def npcr(img1, img2):
        diff = np.not_equal(img1, img2)
        return 100.0 * np.sum(diff) / diff.size

    @staticmethod
    def uaci(img1, img2):
        diff = np.abs(img1.astype(np.int16) - img2.astype(np.int16))
        return 100.0 * np.sum(diff) / (img1.size * 255)

    @staticmethod
    def entropy(img):
        entropies = []
        for channel in range(3):  # R, G, B
            hist, _ = np.histogram(img[:, :, channel], bins=256, range=(0, 256), density=True)
            hist = hist[hist > 0]
            entropies.append(scipy_entropy(hist, base=2))
        return entropies  # [R, G, B]
