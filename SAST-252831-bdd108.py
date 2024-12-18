from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'vulnerable_app.db'
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        c.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")
        conn.commit()
        conn.close()
        print("База данных успешно создана и инициализирована.")
    else:
        print("База данных уже существует. Пропускаем инициализацию.")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Безопасный способ обработки формы контакта
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Просто выводим сообщение о получении формы
        return f'''
            <style>
                body {{ background-image: url('/static/bg3.jpg'); background-size: cover; }}
            </style>
            <h2>Спасибо за сообщение, {name}!</h2>
        '''
    return '''
        <style>
            body { background-image: url('/static/bg3.jpg'); background-size: cover; }
        </style>
        <form method="post">
            Имя: <input type="text" name="name"><br>
            Email: <input type="email" name="email"><br>
            Сообщение: <textarea name="message"></textarea><br>
            <input type="submit" value="Отправить">
        </form>
    '''
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Выполнение SQL запроса: {query}") 
        c.execute(query)
        result = c.fetchone()
        conn.close()

        if result:
            return "Добро пожаловать, " + result['username'] + "!"
        else:
            return "Неверное имя пользователя или пароль!"
    return '''
        <style>
            body { background-image: url('/static/bg2.jpg'); background-size: cover; }
        </style>
        <form method="post">
            Имя пользователя: <input type="text" name="username"><br>
            Пароль: <input type="password" name="password"><br>
            <input type="submit" value="Войти">
        </form>
    '''

@app.route('/about')
def about():
    return '''
        <style>
            body { background-image: url('/static/bg4.jpg'); background-size: cover; }
        </style>
        <h2>О компании</h2>
        <p>Мы - инновационная компания, занимающаяся разработкой веб-приложений.</p>
    '''

@app.route('/welcome')
def welcome():
    name = request.args.get('name', '')
    return render_template_string('''
        <style>
            body { background-image: url('/static/bg5.jpg'); background-size: cover; }
        </style>
        <h1>Добро пожаловать, %s!</h1>
    ''' % name)

@app.route('/blog')
def blog():
    return '''
        <style>
            body { background-image: url('/static/bg6.jpg'); background-size: cover; }
        </style>
        <h2>Наш блог</h2>
        <p>Добро пожаловать в наш блог, где мы делимся последними новостями и обновлениями.</p>
    '''

@app.route('/read')
def read():
    filename = request.args.get('doc', 'default.txt')
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return render_template_string('''
            <style>
                body { background-image: url('/static/bg7.jpg'); background-size: cover; }
            </style>
            <pre>%s</pre>
        ''' % content)
    except Exception as e:
        return f"Ошибка при открытии файла: {e}"

@app.route('/')
def home():
    return '''
        <style>
            body { background-image: url('/static/bg8.jpg'); background-size: cover; }
        </style>
        <h1>Добро пожаловать в веб-приложение</h1>
        <ul>
            <li><a href="/auth">Авторизация</a></li>
            <li><a href="/welcome?name=User">Приветствие</a></li>
            <li><a href="/read?doc=default.txt">Чтение документа</a></li>
            <li><a href="/contact">Контактная форма</a></li>
            <li><a href="/about">О компании</a></li>
            <li><a href="/blog">Блог</a></li>
        </ul>
    '''

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
