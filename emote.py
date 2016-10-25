
import sys, random, json, os
from halibot import HalModule

class Emote(HalModule):

	def init(self):
		# Emotes are of type <string, string[]>
		self.emotes = {}
		self.path = self.config.get('emotes-path')

		self.log.info('using emotes path: ' + self.path)

		if self.path is not None:
			try:
				if not os.path.isfile(self.path):
					with open(self.path, 'w+') as f:
						json.dump(self.emotes, f)

				else:
					with open(self.path, 'r') as f:
						self.emotes = json.loads(f.read())

			except (ValueError):
				self.log.error('Couldn\'t parse JSON: ', file=sys.stderr)
			except (IOError, OSError):
				self.log.error('Couldn\'t open emotes file: ', file=sys.stderr)


	def emote(self, pattern=""):
		if pattern not in self.emotes:
			return 'Emote not found :('
		else:
			return random.choice(self.emotes[pattern])

	def emoteadd(self, emote):
		args = emote.split(' ', 1)

		if args[0] not in self.emotes:
			self.emotes[args[0]] = [args[1]]
		else:
			self.emotes[args[0]].append(args[1])

		with open(self.path, 'w') as f:
			json.dump(self.emotes, f)

		return 'Emote "' + args[0] + '" added :)'

	def emotedel(self, emote):
		if emote == 'lenny':
			return 'One cannot simply delete Lenny ( ͡° ͜ʖ ͡°)'
		elif emote in self.emotes:
			del self.emotes[emote]

			with open(self.path, 'w') as f:
				json.dump(self.emotes, f)

			return 'You strike down the legendary "' + emote + '" with your mighty sword.'
		else:
			return 'You swing your sword but strike only the wind.'

	def receive(self, msg):
		ls = msg.body.split(' ')
		cmd = ls[0] if len(ls) > 0 else ''
		arg = ' '.join(ls[1:]).strip() if len(ls) > 1 else ''

		if cmd == '!lenny':
			self.reply(msg, body='( ͡° ͜ʖ ͡°)')
		elif cmd == '!emoteadd':
			self.reply(msg, body=self.emoteadd(arg))
		elif cmd == '!emotedel':
			self.reply(msg, body=self.emotedel(arg))
		elif cmd == '!emote':
			self.reply(msg, body=self.emote(pattern=arg))

