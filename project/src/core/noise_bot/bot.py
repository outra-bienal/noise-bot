import random
import shlex
import subprocess

import requests

from django.conf import settings
from django.core.files.base import ContentFile
from src.core.noise_bot.jpglitch import random_glitch


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


class BotError(Exception):
    pass


class BienalBot:

    glitch_functions = [
        random_glitch
    ]

    def run_char_rnn(self, cmd):
        try:
            return subprocess.check_output(
                shlex.split(cmd),
                cwd=settings.CHAR_RNN_DIR
            ).strip().decode('utf-8', errors='replace')
        except subprocess.CalledProcessError as exc:
            ret_code = exc.returncode
            ret_out = exc.output
            msg = "Erro com o comando: \n\t{}\n\nRet code {} - Out {}".format(cmd, ret_code, ret_out)
            raise BotError(msg)


    def clean_text(self, text, start, end):
        words = text.split()[start:end]
        words[0] = words[0].title()
        return ' '.join(words)

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
        line = self.run_char_rnn(cmd)
        return self.clean_text(line, 1, -1)

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
        line = self.run_char_rnn(cmd).replace(text, '')
        return self.clean_text(line, 0, -1)

    def glitch_image(self, image_url):
        resp = requests.get(image_url)
        if not resp.ok:
            raise Exception('Error {} for "{}" not found'.format(resp.status, image_url))

        func = random.choice(self.glitch_functions)
        stream = func(resp.content)
        content_file = ContentFile(stream.read())
        content_file.name = 'reply.png'

        return content_file
