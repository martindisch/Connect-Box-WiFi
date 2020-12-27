from connectboxcontrol.util import crypto
import unittest


class TestCrypto(unittest.TestCase):

    def test_derive_key(self):
        password = "password"
        salt = "2edf72e93aba5da5"
        key = crypto.derive_key(password, bytes.fromhex(salt))
        self.assertEqual(key.hex(), "7eb126d09f6371c51099baedee1b02d0")

    def test_ccm_encrypt(self):
        key = bytes.fromhex("7eb126d09f6371c51099baedee1b02d0")
        iv = bytes.fromhex("f3ddf82f06873979")
        plain_text = "The quick brown fox jumps over the lazy dog"
        authenticated_data = "encryptData"
        blob = crypto.ccm_encrypt(key, iv, plain_text, authenticated_data)
        self.assertEqual(blob, "67f629812e12cc616af57f6867fe0f3500c0790270139c75f56553718fd48463316737f55e077a720701533614d9666dcb6e970fcccc368e6e9446")


if __name__ == '__main__':
    unittest.main()
