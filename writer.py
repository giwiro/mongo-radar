def write_log(file: str, text: str):
    with open(file, "a+") as file:
        file.write(text)
