import feedparser
import arrow
import json
import sys
import os
import re

from discord_webhook import DiscordWebhook, DiscordEmbed
from loguru import logger as log
from ics import Calendar, Event
from dotenv import load_dotenv
from pathlib import Path

class ctfhookup:
	log.add(sys.stdin, format="{time} {level} {message}", filter="my_module", level="INFO")
	env_path = f"{Path('.')}/.env"
	load_dotenv(dotenv_path=env_path)

	def __init__(self):
		self.env = os.environ
		self.rss_url = self.env.get('CTFTIME_UPCOMMING_RSS')
		self.discord_hook_url = self.env.get('DISCORD_WEBHOOK_URL')
		self.slack_hook_url = self.env.get('SLACK_WEBHOOK_URL')
		self.discord_hook = DiscordWebhook(self.discord_hook_url, username="CTFHookup")
		self.rss = feedparser.parse(self.rss_url)['entries']
		self.spacer = "¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°º¤ø,¸"
		self.calendar_name = "ctftime_upcomming.ics"
		self.events = {}

	def __str__(self):
		return ", ".join([i for i in dir(ctfhookup) if not i.startswith('_')])

	def __repr__(self):
		return f"{self.__class__.__name__}({self.webhook_url})"

	def _time_machine(days:int, date:str) -> str:
		pass

	def _diff_time(self, end_time:str, start_time:str) -> str:
		"""
		Calculate the difference between two dates

		Args:
			end_time (str): [stop time]
			start_time (str): [start time]

		Returns:
			[str]: [return the diff]
		"""
		return str(arrow.get(end_time) - arrow.get(start_time))

	def _convert_to_readable(self, _input_time:str, timezone:str='Europe/Oslo') -> str:
		"""
		Using regex to convert timestamp to YYYY-MM-DD HH:MM:SS

		Args:
			_input_time (str): [description]
			timezone (str, optional): [convert UTC time to any timezone]. Defaults to 'Europe/Oslo'.

		Returns:
			str: [norwegian time]
		"""
		tida = (re.findall(r'\d{2}', _input_time))
		return arrow \
		.get(f"{tida[0]}{tida[1]}-{tida[2]}-{tida[3]} {tida[4]}:{tida[5]}:{tida[6]}") \
		.to(timezone).for_json()

	def _load_json(self) -> dict:
		"""
		Load Json from ./json/parsed_events.json

		Returns:
			dict: [json dict]
		"""
		log.debug('Loading from Json')
		with open('./json/parsed_events.json', 'r') as fp:
			return (json.load(fp))

	def _write_json(self, _data:dict):
		"""
		Write Parsed data to ./json/parsed_events.json

		Args:
			_data (dict): [json data to write]
		"""
		log.debug('Writing to Json')
		with open('./json/parsed_events.json', 'w') as fp:
			json.dump(_data, fp, indent=4)

	def _webhook(self):
		if "https://discordapp.com/api/webhooks/" in self.discord_hook_url:
			self._discord_webhook_embed()

		elif "slack" in self.slack_hook_url:
			self._slack_webhook_()

	def _discord_webhook_embed(self):
		embed = DiscordEmbed(title="data['title']", description="CTF {data['name']} Organized by {data['organizer_name']}", color=424242)
		embed.set_author(name='Author Name', url="http://data['organizer_url']/", icon_url='https://i.imgur.com/drtH5C0.jpg')
		embed.set_footer(text='CTFHookup')
		embed.set_timestamp()
		embed.add_embed_field(name='Format', value='data["format"]')
		#embed.add_embed_field(name='Point Weigth', value="data['weight']")
		#embed.add_embed_field(name='Restrictions', value="data['restricts']")
		#embed.add_embed_field(name='Location', value="data['location']")
		#embed.add_embed_field(name='Onsite', value="data['onsite']")
		#embed.add_embed_field(name='Voting', value="data['can_haz_vote']")
		#embed.add_embed_field(name='Start', value="data['start_date']")
		#embed.add_embed_field(name='Stop', value="data['finish_date']")

		self.discord_hook.add_embed(embed)
		response = self.discord_hook.execute()

	def _slack_webhook_(self, webhook_url):
		return ("slackern")

	def push_upcomming(self, alert_time:int):
		self._webhook()

	def generate_calendar(self, location:str):
		"""
		Generates the calendar from parsed json data.

		Args:
			location ([str]): [Path where to store the calendar]
		"""
		self._get_rss_entries()
		c = Calendar()
		log.info('Generating Calendar')
		for _id, data in (self._load_json().items()):
			e = Event()
			e.name = data['title']
			e.begin = data['start_date']
			e.duration = ({"days":data['days'], "hours":data['hours'], "minutes":data['minutes'], "seconds":data['seconds']})
			e.description = f"{self.spacer} \
\nCTF {data['name']} Organized by {data['organizer_name']} \
\n{data['organizer_url']} \
\n\nFormat: {data['format']} \
\nPoint Weigth: {data['weight']} \
\nRestrictions: {data['restricts']} \
\nLocation: {data['location']} \
\nOnsite: {data['onsite']} \
\nVoting: {data['can_haz_vote']} \
\nStart: {data['start_date']} \
\nStop: {data['finish_date']} \
\n{self.spacer}"
			c.events.add(e)


			with open(f"{location}{self.calendar_name}", 'w') as f:
				f.writelines(c)
		log.info('Finished Generating CTF calendar')

	def _get_rss_entries(self) -> object:
		"""
		Gets all entries from the Ctftime feed.
		And generates a json struct with event_id as keys.

		Returns:
			[object]: [json dict object]
		"""
		for ctf in self.rss:
			title = str(ctf['title'])
			event_id = int(ctf['link'].split('/')[-1])
			event_url = (ctf['link'])
			event_name = (ctf['ctf_name'])
			event_format = (ctf['format_text'])
			event_logo_url = (ctf['logo_url'])
			event_weight = float(ctf['weight'])
			event_restricts = (ctf['restrictions'])
			event_location = (ctf['location'])
			event_onsite = bool(ctf['onsite'])
			event_start_date = self._convert_to_readable(ctf['start_date'])
			event_finish_date = self._convert_to_readable(ctf['finish_date'])
			event_duration = self._diff_time(event_finish_date, event_start_date)
			event_organizer_url = (ctf['href'])
			event_organizer_name = (ctf['organizers'].split('"')[5])
			event_can_haz_vote = bool(ctf['public_votable'])

			# Splitting time/date so i can easily pass it into the calendar Libary
			if "day" in (event_duration):
				event_days = int(event_duration.split(' ')[0])
			else:
				event_days = 0

			if ":" in event_duration:
				event_time = event_duration.split(' ')[-1].split(':')
				event_hours = int(event_time[0])
				event_minutes = int(event_time[1])
				event_seconds = int(event_time[2])
			else:
				event_hours = 0
				event_minutes = 0
				event_seconds = 0

			self.events[event_id] = {'title': title,
			'name': event_name,
			'format': event_format,
			'logo_url': event_logo_url,
			'weight': event_weight,
			'restricts': event_restricts,
			'location': event_location,
			'onsite': event_onsite,
			'start_date': event_start_date,
			'finish_date': event_finish_date,
			'duration':event_duration,
			'days':event_days,
			'hours':event_hours,
			'minutes':event_minutes,
			'seconds':event_seconds,
			'organizer_url': event_organizer_url,
			'organizer_name': event_organizer_name,
			'can_haz_vote': event_can_haz_vote}

		return self._write_json(self.events)