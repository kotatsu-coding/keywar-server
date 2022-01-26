class GameManager:
    def __init__(self):
        self.rooms = {}

    def game_start(self, room):
        game = Game(room.users)
        self.rooms[room.id] = game
        return game

    def get_game(self, room):
        return self.rooms[room.id]

game_manager = GameManager()

class Game:
    def __init__(self, users):
        self.words = Game.generate_words()
        self.teams = self.create_teams(users)

    def create_teams(self, users):
        team_1 = Team(self.words, users[:2])
        team_2 = Team(self.words, users[2:])
        return [team_1, team_2]

    def get_team(self, user_id):
        for team in self.teams:
            for user in team.users:
                if user['id'] == user_id:
                    return team

    def get_status(self):
        return {
            'team_1': self.teams[0].to_dict(),
            'team_2': self.teams[1].to_dict()
        }

    @staticmethod
    def generate_words():
        import random
        with open('words.txt') as f:
            words = f.read().splitlines()    
        random.shuffle(words)
        print(f'# the words are {words[:10]}')
        return words

class Team:
    def __init__(self, words, users):
        self.current_word_idx = 0
        self.users = [user.to_dict() for user in users]
        self.colors = [user['color'] for user in self.users]
        self.score = 0
        self.words = words
        self.current_word = Word(self.words[self.current_word_idx]).colorize(self.colors)

    def stroke_key(self, key, color):
        self.current_word.stroke_key(key, color)
        if self.current_word.current_idx == len(self.current_word.value):
            self.current_word = self.show_next_word()
        return self.current_word.to_dict()

    def show_next_word(self):
        self.score += 1
        self.current_word_idx += 1
        if self.current_word_idx == len(self.words):
            self.current_word_idx = 0
        self.current_word = Word(self.words[self.current_word_idx]).colorize(self.colors)
        return self.current_word

    def get_current_word(self):
        return self.current_word
    
    def to_dict(self):
        return {
            'current_word': self.current_word.to_dict(),
            'users': [user for user in self.users],
            'score': self.score
        }


class Word:
    def __init__(self, value):
        self.value = value
        self.colors = None
        self.current_idx = 0
        self.sequence = []

    def colorize(self, colors):
        import random
        self.current_idx = 0
        self.colors = [random.choice(colors) for _ in range(len(self.value))]
        return self

    def stroke_key(self, key, color):
        self.sequence.append((color, key))
        if key == self.value[self.current_idx] \
            and self.colors[self.current_idx] == color:
            self.current_idx += 1
        else:
            self.current_idx = 0

        return self.to_dict()

    def to_dict(self):
        return {
            'value': self.value,
            'colors': self.colors,
            'current_idx': self.current_idx,
            'sequence': self.sequence
        }



