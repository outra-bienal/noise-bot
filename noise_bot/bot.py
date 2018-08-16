import random


class NoiseBot:

    def speak_random_line(self):
        return random.choice([
            'Em 78 Por Segundo Rotações',
            'Vou Seguindo Por Segundo',
            'Vou Servindo Por Segundo',
            'Vou Sorrindo Por Segundo',
            'Devagar',
            'Grave Um Disco Devagar',
            'Grave Um Nome Devagar',
        ])

    def reply_to(self, text):
        text_as_list = list(text)
        random.shuffle(text_as_list)
        return ''.join(text_as_list)
