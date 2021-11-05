import json


user_books = {}
book_users = {}
book_info = {}
rubrics_books = {}
ontology = {}


def open_dataset_file(filename):
    print(f"Loading {filename}")
    return open(DATASET_LOCATION + filename, encoding='utf-8')


def read_csv_file(filename, process_row):
    with open_dataset_file(filename) as fin:
        for line in fin.readlines()[1:]:
            row = line.split(';')
            process_row(row)


def read_user_books():
    def process_row(row):
        user_id = int(row[0])
        book_id = int(row[1])
        if validate_book_id(book_id):
            if user_id not in user_books:
                user_books[user_id] = []
            user_books[user_id].append(book_id)
            if book_id not in book_users:
                book_users[book_id] = []
            book_users[book_id].append(user_id)
    for i in range(0, 3):
        read_csv_file(f'user_books_{i + 1}.csv', process_row)


def read_book_info():
    def process_row(row):
        book_id = int(row[0])
        author = row[1]
        title = row[2]
        if author != '' and title != '':
            book_info[book_id] = {
                'book_id': book_id,
                'author': author,
                'title': title,
            }
    for i in range(0, 2):
        read_csv_file(f'book_info_{i + 1}.csv', process_row)


def read_book_rubrics():
    def process_row(row):
        book_id = int(row[0])
        rubrics = row[1]
        if book_id in book_info:
            book_info[book_id]['rubrics'] = rubrics
    for i in range(0, 2):
        read_csv_file(f'book_rubrics_{i + 1}.csv', process_row)


def read_ontology():
    global ontology
    def dfs(node):
        for key, child in node.items():
            rubrics_books[key] = {}
            dfs(child)
    with open_dataset_file('ontology.json') as fin:
        ontology = json.load(fin)
        dfs(ontology)



def validate_book_id(book_id):
    if book_id not in book_info:
        return False
    book = book_info[book_id]
    if 'rubrics' not in book:
        return False
    if book['rubrics'] not in rubrics_books:
        return False
    if book_id not in rubrics_books[book['rubrics']]:
        rubrics_books[book['rubrics']][book_id] = book
    return True


def load(dataset_location):
    global DATASET_LOCATION
    DATASET_LOCATION = dataset_location
    read_book_info()
    read_ontology()
    read_book_rubrics()
    read_user_books()
    print('Dataset is loaded!')
