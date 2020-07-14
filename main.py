#!/usr/bin/env python3
import argparse

from ctfhookup import ctfhookup

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CTFtime Ical and Webhooks')
	parser.add_argument('--calendar', action='store_true', help="Generates ical file for all upcomming ctf evetns")
	parser.add_argument('--location', type=str, help="where do you want calendar to apeear", default="./ics/")

	parser.add_argument('--webhook', action='store_true', help="enables webhook mode, and will start pushing events that are upcomming.")
	parser.add_argument('--days', type=int, help="how many days should it notice about ctf", default=7)
	args = parser.parse_args()

	if args.calendar:
		ctfhookup().generate_calendar(args.location)
	elif args.webhook:
		ctfhookup().push_upcomming(args.days)