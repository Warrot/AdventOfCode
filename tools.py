def load_file(file):
    with open(file, 'r') as file:
        for line in file:
            yield line