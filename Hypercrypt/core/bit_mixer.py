class BitMixer:
    @staticmethod
    def split_byte(byte):
        """Sépare un octet en deux demi-octets (4 bits)"""
        left = (byte >> 4) & 0x0F
        right = byte & 0x0F
        return left, right

    @staticmethod
    def combine_halves(left, right):
        """Recombine deux demi-octets en un seul octet"""
        return ((left & 0x0F) << 4) | (right & 0x0F)

    @staticmethod
    def mix_pixel_byte(byte, chaos1, chaos2, chaos_swap_flag):
        """Applique le bit-mixing à un seul pixel"""
        left, right = BitMixer.split_byte(byte)

        # Réduire chaos1, chaos2 sur 4 bits
        l_mask = chaos1 & 0x0F
        r_mask = chaos2 & 0x0F

        left ^= l_mask
        right ^= r_mask

        if chaos_swap_flag % 2 == 1:
            left, right = right, left

        return BitMixer.combine_halves(left, right)

    @staticmethod
    def mix_image(image, chaotic_bytes):
        """
        Applique le bit-level mixing à une image RGB (3D numpy array).
        chaotic_bytes : liste de valeurs pseudo-aléatoires (len ≥ image.size * 3)
        """
        import numpy as np

        h, w, c = image.shape
        assert c == 3, "L’image doit être en RGB"
        assert len(chaotic_bytes) >= h * w * 3, "Pas assez de données chaotiques"

        output = np.zeros_like(image, dtype=np.uint8)
        idx = 0

        for i in range(h):
            for j in range(w):
                for k in range(3):  # R, G, B
                    byte = image[i, j, k]
                    chaos1 = chaotic_bytes[idx]
                    chaos2 = chaotic_bytes[idx + 1]
                    swap_flag = chaotic_bytes[idx + 2]
                    output[i, j, k] = BitMixer.mix_pixel_byte(byte, chaos1, chaos2, swap_flag)
                    idx += 3

        return output

    @staticmethod
    def unmix_pixel_byte(byte, chaos1, chaos2, chaos_swap_flag):
        """Inverse du bit-mixing"""
        left, right = BitMixer.split_byte(byte)

        if chaos_swap_flag % 2 == 1:
            left, right = right, left

        # Réduire sur 4 bits
        l_mask = chaos1 & 0x0F
        r_mask = chaos2 & 0x0F

        left ^= l_mask
        right ^= r_mask

        return BitMixer.combine_halves(left, right)

    @staticmethod
    def unmix_image(image, chaotic_bytes):
        import numpy as np

        h, w, c = image.shape
        output = np.zeros_like(image, dtype=np.uint8)
        idx = 0

        for i in range(h):
            for j in range(w):
                for k in range(3):
                    byte = image[i, j, k]
                    chaos1 = chaotic_bytes[idx]
                    chaos2 = chaotic_bytes[idx + 1]
                    swap_flag = chaotic_bytes[idx + 2]
                    output[i, j, k] = BitMixer.unmix_pixel_byte(byte, chaos1, chaos2, swap_flag)
                    idx += 3

        return output

