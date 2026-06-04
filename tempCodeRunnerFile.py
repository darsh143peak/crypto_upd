
    print("Access allowed")

    # -------- extract --------

    aes_text = steg.extract("data/output.png")

    text = aes.decrypt(aes_text)

    print("Secret:", text)


