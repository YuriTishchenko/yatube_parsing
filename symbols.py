if __name__ == '__main__':
    with open('groups.csv', encoding='utf-8') as file:
        content = file.read()
        print(len(content))
