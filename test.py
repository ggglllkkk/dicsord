import customtkinter as ctk

a="bijour, je m'appelle gromile\n et j'aime les chaussettes"

window=ctk.CTk()

def a():
    texts.insert("end", "dafuq")

texts=ctk.CTkTextbox(window)
texts.pack()
button=ctk.CTkButton(window, text="button", command=a).pack()

window.mainloop()