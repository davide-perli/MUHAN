import mate
while True:
    text= input('type: ')
    result, error = mate.run('<stdin>', text)

    if error: print(error.show_as_string())
    else: print(result)
