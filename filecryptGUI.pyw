from TK import *
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import filedialog
from crypto import Crypt
import os

global keyfilename


def opfid(init_dir, title, ftypes): # File to encrypt/decrypt select dialog
    file_name = filedialog.askopenfilename(initialdir=init_dir, title=title, filetypes=ftypes)
    fileNameVar.set(file_name)


def opfld(init_dir, title): # Key folder select dialog
    folder_name = filedialog.askdirectory(initialdir=init_dir, title=title)
    keyPathVar.set(folder_name)


def run(): # Run encrypt/decrypt function
    # Get widget values
    k = keyPathVar.get()
    f = fileNameVar.get()
    g = genKeyVar.get()
    o = optSelVar.get()

    keyfile = os.path.join(k, keyfilename)

    # Clear status label
    status_text = st.ScrolledText(mainWin, width=46, height=5)
    status_text.place(x=5, y=120)

    try:
        # Make sure file paths are not empty

        if k == "":
            raise Exception("Missing key file path argument.")
        elif not os.path.exists(keyfile) and g == 0:
            raise Exception(f"File Not Found: {keyfile}")
        if f == "":
            raise Exception("Missing file argument.")
        elif not os.path.exists(f):
            raise Exception(f"File Not Found: {f}")
        else:
            c = Crypt()

            # Check if generate key flag is set
            # and does not already exist
            if g == 1 and o == 0:
                if not os.path.exists(keyfile):
                    status_text.insert(tk.INSERT, f"Writing key file: {keyfile}\n")
                    c.write_key(keyfile)
                else:
                    status_text.insert(tk.INSERT, f"Key file already exists: {keyfile}\n")

            # load the key
            status_text.insert(tk.INSERT, f"Loading key file: {keyfile}\n")
            key = c.load_key(keyfile)

            # If option is 0 then encrypt else decrypt
            if o == 0:
                status_text.insert(tk.INSERT, f"Encrypting file: {f}\n")
                c.encrypt(f, key)
            elif o == 1:
                status_text.insert(tk.INSERT, f"Decrypting file: {f}\n")
                c.decrypt(f, key)
            else:
                raise Exception("An unexpected error occurred. - ")

            status_text.insert(tk.INSERT, "Finished.")

    except OSError as error:
        if error.errno == 2:
            status_text.insert(tk.INSERT, "File not found error. - " + str(error) + "\n")
        else:
            status_text.insert(tk.INSERT, "OS error. - " + str(error) + "\n")
#    except FileNotFoundError as error:
#        status_text.insert(tk.INSERT, "File not found error. - " + str(error) + "\n")
    except RuntimeError as error:
        status_text.insert(tk.INSERT, "Unexpected error. - " + str(error) + "\n")
    except Exception as error:
        status_text.insert(tk.INSERT, str(error) + "\n")
    except:
        status_text.insert(tk.INSERT, "Unhandled error. This may occur if you try to decrypt an un-encrypted file\n")


if __name__ == "__main__":

    mainWin = Root("FileCrypt")

    keyfilename = "key.key"

    # Variables to hold widget values
    genKeyVar = IntVar()
    optSelVar = IntVar()
    statusVar = StringVar()
    fileNameVar = StringVar()
    keyPathVar = StringVar()

    # Generate new key file
    Checkbutton(mainWin, text="Generate Key file", variable=genKeyVar).place(x=5, y=0)

    # Path to key file. Opens Directory select dialog on button click
    Label(mainWin, text="Key Path/File:").place(x=5, y=30)
    ent1 = Entry(mainWin, textvariable=keyPathVar, width=54).place(x=85, y=30)
    bimg1 = ImageTk.PhotoImage(Image.open("folder.png").resize((15, 15), 2))
    # Removed initial directory value as it causes an Access Denied error message
    # on windows machine when the dialog opens
    p1 = "" # os.path.join(os.environ['USERPROFILE'], 'My Documents')
    tt1 = "Select a Folder"
    btn1 = Button(mainWin, image=bimg1, command=lambda: opfld(p1, tt1), height=15, width=15, padx=2, pady=2).place(x=418, y=30)

    # File to encrypt/decrypt.  Opens File select dialog on button click
    Label(mainWin, text="Filename:").place(x=26, y=60)
    ent2 = Entry(mainWin, textvariable=fileNameVar, width=54).place(x=85, y=60)
    bimg2 = ImageTk.PhotoImage(Image.open("folder.png").resize((15, 15), 2))
    # Removed initial directory value as it causes an Access Denied error message
    # on windows machine when the dialog opens
    p2 = "" # os.path.join(os.environ['USERPROFILE'], 'My Documents')
    ty2 = ""
    tt2 = "Select a File"
    btn2 = Button(mainWin, image=bimg2, command=lambda: opfid(p2, tt2, ty2), height=15, width=15, padx=2, pady=2).place(x=418, y=60)

    # Encrypt or Decrypt file
    Radiobutton(mainWin, text="Encrypt", variable=optSelVar, value=0).place(x=5, y=90)
    Radiobutton(mainWin, text="Decrypt", variable=optSelVar, value=1).place(x=100, y=90)

    # Run encrypt/decrypt function on click
    run_ = Button(mainWin, text="Run", command=run).place(x=360, y=88)
    close_ = Button(mainWin, text="Close", command=mainWin.destroy).place(x=400, y=88)

    mainWin.mainloop()
