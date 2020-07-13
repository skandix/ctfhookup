import feedparser
import datetime
import codecs
import arrow
import json
import re

from ics import Calendar, Event

class ctfhookup:
	def __init__(self, webhook_url):
		self.rss_url = "https://ctftime.org/event/list/upcoming/rss/"
		self.webhook_url = webhook_url
		self.rss = feedparser.parse(self.rss_url)['entries']
		self.events = {}

	def __str__(self):
		return ", ".join([i for i in dir(ctfhookup) if not i.startswith('_')])

	def __repr__(self):
		return f"{self.__class__.__name__}({self.webhook_url})"

	def push_upcomming(self):
		print ("Pushing new kkool event")
		self._webhook()

	def _webhook(self):
		""" check if webhook is discord or slack """
		if "discord" in self.webhook_url:
			self._discord_webhook_embed(self.webhook_url)

		elif "slack" in self.webhook_url:
			self._slack_webhook_(self.webhook_url)

	def _discord_webhook_embed(self, webhook_url):
		""" push a certain embedd to the discord webhook """
		return ("discoord")

	def _slack_webhook_(self, webhook_url):
		""" aner ikke hvordan slack og webhooks funker... """
		return ("slack")

	def generate_calendar(self):
		self.get_rss_entries()
		c = Calendar()
		for _id, data in (self._load_json().items()):
			print (data['duration'])
			"""
			e = Event()
			e.name = data['title']
			e.begin = data['start_date']
			e.duration = data['duration']

			e.description = f"CTF {data['name']} Organized by {data['organizer_name']} \n{data['organizer_url']}\nFormat: {data['format']}\nPoint Weigth: {data['weight']}\nRestrictions: {data['restricts']}\n"
			c.events.add(e)
			print(c)

			with open('./ical/ctftime_upcomming.ics', 'w') as f:
				f.writelines(c)
			"""

	def _diff_time(self, end_time:str, start_time:str):
		diff  = str(arrow.get(end_time) - arrow.get(start_time))
		return diff
		#"if "days" in diff:
		#	return (f"{(int(diff.split('days')[0])*24)}")
		#elif "day" in diff:
		#	return (f"24")
		#else:
		#	return (diff.split(':')[0])

	def _convert_to_readable(self, timebomb:str, timezone:str='Europe/Oslo') -> str:
		"""
		_convert_to_readable convert from ctftime time format to a more readable timeformat and then convert it to a certain timezone

		Args:
			timebomb (str): [time to convert]
			timezone (str, optional): [convert to a specific Timezone]. Defaults to 'Europe/Oslo'.

		Returns:
			str: [human readable norwegian time]
		"""
		human = (re.findall(r'\d{2}', timebomb)) # yay Regex <3
		return arrow.get(f"{human[0]}{human[1]}-{human[2]}-{human[3]} {human[4]}:{human[5]}:{human[6]}").to(timezone).for_json()

	def _load_json(self) -> dict:
		with open('./json/parsed_events.json', 'r') as fp:
			return (json.load(fp))

	def _write_json(self, _data:dict):
		""" store parsed events to a local json file """
		with open('./json/parsed_events.json', 'w') as fp:
			json.dump(_data, fp, indent=4)

	def get_rss_entries(self):
		""" ugly af, men som halvor skulle sagt det.. 'Funkææær'  """
		for ctf in self.rss:
			event_id = (ctf['link'].split('/')[-1])
			self.events[event_id] = {}

			title = str(ctf['title'])
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
			'organizer_url': event_organizer_url,
			'organizer_name': event_organizer_name,
			'can_haz_vote': event_can_haz_vote}

		return self._write_json(self.events)