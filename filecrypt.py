from crypto import Crypt
import os

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Encryptor Script")
    parser.add_argument("keyfile", help="Path to key file")
    parser.add_argument("file", help="File to encrypt/decrypt")
    parser.add_argument("-g", "--generate-key", dest="generate_key", action="store_true",
                        help="Whether to generate a new key or use existing")
    parser.add_argument("-e", "--encrypt", action="store_true",
                        help="Whether to encrypt the file, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true",
                        help="Whether to decrypt the file, only -e or -d can be specified.")

    args = parser.parse_args()
    keyfilepath = args.keyfile
    file = args.file
    generate_key = args.generate_key
    keyfilename = "key.key"
    keyfile = os.path.join(keyfilepath, keyfilename)
    c = Crypt()
    try:
        if keyfilepath == "":
            raise Exception("Missing key file path argument.")
        elif not os.path.exists(keyfile) and not generate_key:
            raise Exception(f"File Not Found: {keyfile}")
        if file == "":
            raise Exception("Missing file argument.")
        elif not os.path.exists(file):
            raise Exception(f"File Not Found: {file}")

        if generate_key:
            if not os.path.exists(keyfile):
                print(f"Writing key file: {keyfile}")
                c.write_key(keyfile)
            else:
                print(f"Key file already exists: {keyfile}")

        # load the key
        print(f"Loading key file: {keyfile}")
        key = c.load_key(keyfile)

        encrypt_ = args.encrypt
        decrypt_ = args.decrypt

        if file == "":
            raise Exception("Missing file argument.")
        elif encrypt_ and decrypt_:
            raise Exception("Please specify whether you want to encrypt the file or decrypt it.")
        elif encrypt_:
            print("Encrypting file: " + file)
            c.encrypt(file, key)
        elif decrypt_:
            print("Decrypting file: " + file)
            c.decrypt(file, key)
        else:
            raise Exception("Please specify whether you want to encrypt the file or decrypt it.")

        print("Finished")

    except OSError as error:
        if error.errno == 2:
            print("File not found error. - " + str(error))
        else:
            print("OS error. - " + str(error))
    except FileNotFoundError as error:
        print("File not found error. - " + str(error))
    except RuntimeError as error:
        print(error)
    except Exception as error:
        print(error)
    except:
        print("An un-handled error occurred. Please check args and try again.")

