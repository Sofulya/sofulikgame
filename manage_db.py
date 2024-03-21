import sqlite3


class SuperGameDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_databases(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id_user INTEGER PRIMARY KEY,
                                    login TEXT,
                                    password TEXT
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS game (
                                    id_game INTEGER PRIMARY KEY,
                                    score INTEGER,
                                    id_user INTEGER,
                                    FOREIGN KEY (id_user) REFERENCES users(id_user)
                                )''')
        self.conn.commit()

    def insert_user(self, login, password):
        self.cursor.execute('''INSERT INTO users (login, password) VALUES (?, ?)''', (login, password))
        self.conn.commit()

    def insert_game(self, score, id_user):
        self.cursor.execute('''INSERT INTO game (score, id_user) VALUES (?, ?)''',
                            (score, id_user,))
        self.conn.commit()

    def get_user_by_login(self, login, password):
        self.cursor.execute('''SELECT * FROM users WHERE login = ? AND password = ?''', (login, password,))
        user = self.cursor.fetchone()
        return user

    def get_user_id_by_login(self, login, password):
        self.cursor.execute('''SELECT id_user FROM users WHERE login = ? AND password = ?''', (login, password,))
        user = self.cursor.fetchone()
        if user:
            return user[0]
        else:
            return None

    def get_user_by_id(self, user_id):
        self.cursor.execute('''SELECT login FROM users WHERE id = ?''', (user_id,))
        user = self.cursor.fetchone()
        return user

    def get_game_by_id(self, id_game):
        self.cursor.execute('''SELECT * FROM game WHERE id_game = ?''', (id_game,))
        game = self.cursor.fetchone()
        return game

    def delete_user(self, id_user):
        self.cursor.execute('''DELETE FROM users WHERE id_user = ?''', (id_user,))
        self.conn.commit()

    def delete_game(self, id_game):
        self.cursor.execute('''DELETE FROM game WHERE id_game = ?''', (id_game,))
        self.conn.commit()

    def get_top_users(self, limit=3):
        self.cursor.execute('''SELECT users.login, MAX(game.score) AS score
                               FROM users
                               INNER JOIN game ON users.id_user = game.id_user
                               GROUP BY users.id_user
                               ORDER BY score DESC
                               LIMIT ?''', (limit,))
        top_users = self.cursor.fetchall()
        return top_users

    def close_connection(self):
        self.conn.close()

