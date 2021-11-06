import json


global user_books
global book_users
global book_info
global ontology
global rubrics_books

#246322

def init_global_fields(dataset):
    global user_books
    global book_users
    global book_info
    global ontology
    global rubrics_books
    user_books = dataset.user_books
    book_users = dataset.book_users
    book_info = dataset.book_info
    rubrics_books = dataset.rubrics_books
    ontology = dataset.ontology


#Возвращает конечный ответ
def get_response(user_id, dataset):
    init_global_fields(dataset)
    history = get_history(user_id)
    recommendations = get_recommendations(history, 5, user_id)
    return {
        'history': history,
        'recommendations': recommendations,
    }

#получить историю пользователя
def get_history(user_id):
    if user_id not in user_books:
        return []
    else:
        return [book_info[book_id] for book_id in user_books[user_id]]


#Метод расчёта рекомендаций
def get_recommendations(history, count, user_id):
    if len(history) == 0:
        return get_most_popular_books()[:count] #Если пользователь ничего не читал - вызываем холодный старт
    else:
        nodes, graph = get_ontology_nodes(history, count) # считаем веса в графе онтологии
        nodes = nodes[:5]
        table = [
            [(0, 5)],
            [(0, 3), (1, 2)],
            [(0, 2), (1, 2), (2, 1)],
            [(0, 2), (1, 1), (2, 1), (3, 1)],
            [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],
        ]
        answer = []
        reseve = []
        row = table[len(nodes) - 1]
        for node_index, node_count in row:
            rubrics = nodes[node_index]['rubrics']
            history_of_interest = get_history_of_interest(history, graph, rubrics, 15 / len(table[len(nodes) - 1])) #выделяем из истории вектор, соответствующий выбранным рубрикам
            best = get_best_books_for_rubrics(history_of_interest, rubrics, user_id)
            for book in best[:node_count]:
                answer.append(book)
            for additional in best[node_count:node_count+count]:
                reseve.append(additional)
        for additional in reseve: #Если в какой-то из рубрик не набралось нужного числа книг - добираем до квоты из других рекомендованных рубрик
            if len(answer) < count:
                answer.append(additional)
        return answer
            

def get_most_popular_books():
    return [
        book_info[book_id] for book_id in sorted(
            list(book_users.keys()), 
            reverse=True, 
            key=lambda book_id: len(book_users[book_id])
        )
    ]


def get_ontology_nodes(history, count): #Наложение интересов на граф онтологии ( подробно в документации)
    graph = build_ontology_graph()
    stats = {}
    for book in history:
        if book['rubrics'] not in stats:
            stats['rubrics'] = 0
        stats['rubrics'] += 1
        graph[book['rubrics']]['count'] = min(graph[book['rubrics']]['count'] + 1, len(history) / count)
    def apply_activations(node):
        node['activation'] += node['count'] * node['weight']
        for child in node['children']:
            apply_activations(child)
            node['activation'] += child['activation'] * node['weight'] / len(node['children'])
    for node in graph.values():
        if node['parent'] is None:
            apply_activations(node)
    return sorted(
        filter(lambda node: node['activation'] > 0, graph.values()), 
        key=lambda node: node['activation'], reverse=True
    ), graph


def build_ontology_graph(): #построение графа онтологии
    graph = {}
    def dfs(node, root=None):
        for key in node.keys():
            graph[key] = {
                'rubrics': key,
                'parent': root,
                'weight': 1.0,
                'children': [],
                'count': 0,
                'activation': 0,
            }
            if root is not None:
                root['children'].append(graph[key])
        for key, child in node.items():
            dfs(child, graph[key])
    dfs(ontology)
    def put_weights(node):
        for child in node['children']:
            child['weight'] = node['weight'] / 2
            put_weights(child)
    for node in graph.values():
        if node['parent'] is None:
            put_weights(node)
    return graph


def get_history_of_interest(history, graph, rubrics, count): #выделение целевого вектора из истории
    def dfs(node):
        for child in node['children']:
            if child['rubrics'] == rubrics:
                return True
            return dfs(child)
    def go_up(node):
        if node is None:
            return None
        if node['rubrics'] == rubrics:
            return True
        return go_up(node['parent'])
    def correlates(book):
        node = graph[book['rubrics']]
        return dfs(node) or go_up(node)
    answer = []
    for book in history:
        if correlates(book):
            answer.append(book)
            count -= 1
            if count <= 0:
                break
    return answer

#Выделяем ркомендованные книги по каждой рубрике
#На вход подаётся история пользователя, его id и целевая рубрика
def get_best_books_for_rubrics(history, rubrics, user_from_id):
    my_ids = {} #сохраняем сюда книги, которые пользователь уже брал
    for book in history:
        my_ids[book['book_id']] = True
    book_weights = {}
    for book_from in history:
        for user_to_id in book_users[book_from['book_id']]: #ищем по пользователям, кто брал такую же книгу
            if user_to_id != user_from_id:
                for book_to_id in user_books[user_to_id]:
                    book_to = book_info[book_to_id]
                    if book_to['rubrics'] != rubrics:
                        continue
                    if book_to['book_id'] in my_ids:
                        continue
                    if book_to_id not in book_weights:
                        book_weights[book_to_id] = 0
                    book_weights[book_to_id] += 1 #увеличиваем веса книг, взятых другим пользователем по рубрике
    book_by_titles = {}
    for book_id in book_weights.keys():
        book = book_info[book_id]
        if book['title'] in book_by_titles:
            continue
        book_by_titles[book['title']] = book
    return sorted(
        book_by_titles.values(), 
        key=lambda book: book_weights[book['book_id']],
        reverse=True
    ) #возвращаем полученный список книг, начиная с самых часто встречающихся
