class GameManager:
    def __init__(self):
        self.rooms = {}

    def game_start(self, room):
        game = Game(room.get_teams())
        self.rooms[room.id] = game
        return game

    def get_game(self, room):
        return self.rooms[room.id]

game_manager = GameManager()

class Game:
    def __init__(self, teams):
        self.words = Game.generate_words()
        self.teams = self.create_teams(teams)

    def create_teams(self, teams):
        return [Team(team['id'], self.words, team['users']) for team in teams]

    def get_team(self, user_id):
        for team in self.teams:
            for user in team.users:
                if user['id'] == user_id:
                    return team

    def get_status(self):
        status = {}
        for i in range(len(self.teams)):
            status[f'team_{i+1}'] = self.teams[i].to_dict()
        return status

    @staticmethod
    def generate_words():
        import random
        with open('words.txt') as f:
            words = f.read().splitlines()    
        random.shuffle(words)
        print(f'# the words are {words[:10]}')
        words = [Word(word).colorize([0, 1]) for word in words]
        return words

class Team:
    def __init__(self, team_id, words, users):
        self.id = team_id
        self.current_word_idx = 0
        self.users = users
        self.colors = [user['color'] for user in self.users]
        self.score = 0
        self.words = words
        self.current_word = Word(self.words[self.current_word_idx].value)
        self.current_word.colors = [
            self.colors[color_idx] for color_idx in self.words[self.current_word_idx].colors
        ]

    def show_next_word(self):
        self.score += 1
        self.current_word_idx += 1
        if self.current_word_idx == len(self.words):
            self.current_word_idx = 0
        self.current_word = Word(self.words[self.current_word_idx].value)
        self.current_word.colors = [
            self.colors[color_idx] for color_idx in self.words[self.current_word_idx].colors
        ]
        return self.current_word

    def get_current_word(self):
        return self.current_word
    
    def validate_word(self, word):
        if word['current_idx'] == self.current_word.current_idx + 1:
            self.current_word.current_idx += 1
        elif word['current_idx'] == 0:
            self.current_word.current_idx = 0
        return self.current_word.to_dict()

    def to_dict(self):
        return {
            'id': self.id,
            'current_word': self.current_word.to_dict(),
            'users': [user for user in self.users],
            'score': self.score
        }


class Word:
    def __init__(self, value):
        self.value = value
        self.colors = None
        self.current_idx = 0

    def colorize(self, colors):
        import random
        self.current_idx = 0
        self.colors = [random.choice(colors) for _ in range(len(self.value))]
        return self

    def to_dict(self):
        return {
            'value': self.value,
            'colors': self.colors,
            'current_idx': self.current_idx
        }



