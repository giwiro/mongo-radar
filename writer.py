
def write_log(text):
    with open("loot.log", "a+") as file:
        file.write(text)
