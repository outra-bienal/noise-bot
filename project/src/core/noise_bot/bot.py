import random
import shlex
import subprocess

from django.conf import settings


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


class BienalBot:

    def run_char_rnn(self, cmd):
        return subprocess.check_output(
            shlex.split(cmd),
            cwd=settings.CHAR_RNN_DIR
        ).strip().decode('utf-8', errors='replace')

    def speak_random_line(self):
        cmd = ' '.join([
            settings.TORCH_BIN,
            'sample.lua',
            settings.CHAR_RNN_MODEL,
            '-gpuid',
            '-1',
            '-verbose',
            '0',
            '-length',
            '200',
            '-seed',
            str(random.choice(range(0, 10000000))),
            '-temperature',
            str(random.uniform(0.6, 0.8))
        ])
        return self.run_char_rnn(cmd)

    def reply_to(self, text):
        cmd = ' '.join([
            settings.TORCH_BIN,
            'sample.lua',
            settings.CHAR_RNN_MODEL,
            '-gpuid',
            '-1',
            '-verbose',
            '0',
            '-length',
            '200',
            '-primetext',
            '"{}"'.format(text),
            '-temperature',
            str(random.uniform(0.7, 0.9))
        ])
        return self.run_char_rnn(cmd)
