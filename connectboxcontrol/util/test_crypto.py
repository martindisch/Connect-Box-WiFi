from connectboxcontrol.util import crypto
import unittest


class TestCrypto(unittest.TestCase):

    def test_derive_key(self):
        password = "password"
        salt = "2edf72e93aba5da5"
        key = crypto.derive_key(password, bytes.fromhex(salt))
        self.assertEqual(key.hex(), "7eb126d09f6371c51099baedee1b02d0")


if __name__ == '__main__':
    unittest.main()
