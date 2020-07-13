import feedparser
import codecs
import json

class ctfhookup:
	def __init__(self):
		self.rss_url = "https://ctftime.org/event/list/upcoming/rss/"
		self.rss = feedparser.parse(self.rss_url)['entries']
		self.avaliable_formats = ['Attack-Defense', 'Jeopardy', 'mixed']
		self.avaliable_restrictions = ['Open', 'Prequalified', 'Academic']
		self.past_events = []
		self.events = {}

	def __str__(self):
		return ", ".join([i+"()" for i in dir(ctfhookup) if not i.startswith('_')])

	def __repr__(self):
		pass

	def new_event(self):
		"""  """
		pass

	def _webhook(self):
		""" check if webhook is discord or slack """
		pass

	def _store_locally(self, _events):
		""" store parsed events to a local json file """
		with codecs.open('./json/parsed_events.json', 'w+', encoding='utf-8') as outfile:
			json.dump(_events, outfile, indent=4, ensure_ascii=False)
		pass

	def discord_embed(self):
		pass

	def get_rss_entries(self):
		""" ugly af, men som halvor skulle sagt det.. 'Funkææær'  """
		for ctf in self.rss:
			
			event_id = ctf['link'].split('/')[-1] #str 

			self.events[event_id] = {} # init dicts

			title = ctf['title']	#str text
			event_url = (ctf['link'])	#str text
			event_name = (ctf['ctf_name'])
			event_format = (ctf['format_text'])	# str (text)
			event_logo_url = (ctf['logo_url'])	#str (url)
			event_weight = (ctf['weight'])	#float
			event_restricts = (ctf['restrictions']) #str
			event_location = (ctf['location']) #str text
			event_onsite = (ctf['onsite']) #bool
			event_start_date = (ctf['start_date'])	#str (unix time)
			event_finish_date = (ctf['finish_date'])	#str (unix time)
			event_organizer_url = (ctf['href'])	#str (url)
			event_organizer_name = (ctf['organizers'].split('"')[5]) #str text	
			event_can_haz_vote = (ctf['public_votable']) # bool
			
			self.events[event_id] = {"title": title,
								"name": event_name,
								"format": event_format,
								"logo_url": event_logo_url,
								"weight": event_weight,
								"restricts": event_restricts,
								"location": event_location,
								"onsite": event_onsite,
								"start_date": event_start_date,
								"finish_date": event_finish_date,
								"organizer_url": event_organizer_url,
								"organizer_name": event_organizer_name,
								"can_haz_vote": event_can_haz_vote}

		self._store_locally(self.events)