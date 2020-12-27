from cryptography.fernet import Fernet


class Crypt:

    def __init__(self):
        pass

    def write_key(self, keyfile):
        """
        Generates a key and save it into a file
        """
        key = Fernet.generate_key()
        with open(keyfile, "wb") as key_file:
            key_file.write(key)

    def load_key(self, keyfile):
        """
        Loads the key from the current directory named `key.key`
        """
        return open(keyfile, "rb").read()

    def encrypt(self, filename, key):
        """
        Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        try:
            f = Fernet(key)
            with open(filename, "rb") as file:
                # read all file data
                file_data = file.read()
            # encrypt data
            encrypted_data = f.encrypt(file_data)
            # write the encrypted file
            with open(filename, "wb") as file:
                file.write(encrypted_data)

        except RuntimeError as error:
            raise
        finally:
            if not file.closed:
                file.close()

    def decrypt(self, filename, key):
        """
        Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        try:
            f = Fernet(key)
            with open(filename, "rb") as file:
                # read the encrypted data
                encrypted_data = file.read()
            # decrypt data
            decrypted_data = f.decrypt(encrypted_data)
            # write the original file
            with open(filename, "wb") as file:
                file.write(decrypted_data)

        except RuntimeError as error:
            raise
        finally:
            if not file.closed:
                file.close()
