#!/usr/bin/env python3
from ctfhookup import ctfhookup

url = "https://datapor.no/api/webhooks/nanananana/93w4itwgkj0+adsi0sgs-MEQyuhEJrjM-qyowpX5-R7N72H9id-eT2Lo9Jl"

if __name__ == '__main__':
	print (ctfhookup(url).push_upcomming())