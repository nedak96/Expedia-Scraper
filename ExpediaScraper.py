import urllib
from lxml import html
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from argparse import ArgumentParser

LOAD_TIMEOUT = 60
NUM_FLIGHTS_TO_DISPLAY = 5
NUM_RETURN_FLIGHTS_TO_DISPLAY = 5
SELECT_BUTTON_XPATH = "//li[@data-test-id='offer-listing']//button[@data-test-id='select-button']"
FLIGHTS_XPATH = "//li[@data-test-id='offer-listing']"
DEPARTURE_TIME_XPATH = ".//span[@data-test-id='departure-time']//text()"
ARRIVAL_TIME_XPATH = ".//span[@data-test-id='arrival-time']//text()"
ARRIVES_NEXT_DAY_XPATH = ".//span[@data-test-id='arrives-next-day']//text()"
PRICES_XPATH = ".//span[@data-test-id='listing-price-dollars']//text()"
DURATION_XPATH = ".//span[@data-test-id='duration']//text()"
LEG_KEY_XPATH = ".//div[@data-test-id='listing-summary']"
LEG_KEY_ATTRIBUTE = "data-leg-natural-key"


def get_url(args):
	departure_airport = args.departure_airport
	destination_airport = args.destination_airport
	departure_date = args.departure_date
	return_date = args.return_date
	num_children = args.children
	num_adults = args.adults
	is_round_trip = False

	params = {
		"mode": "search",
		"leg1": "from:"+departure_airport+",to:"+destination_airport+",departure:"+departure_date+"TANYT",
		"passengers": "children:"+str(num_children)+",adults:"+str(num_adults)
	}
	if return_date:
		is_round_trip = True
		params["trip"] = "roundtrip"
		params["leg2"] = "from:"+destination_airport+",to:"+departure_airport+",departure:"+return_date+"TANYT"
		print("Checking round trip flights from " + departure_airport + " to " + destination_airport + " from " + departure_date + " to " + return_date)
	else:
		params["trip"] = "oneway"
		print("Checking one-way flights from " + departure_airport + " to " + destination_airport + " on " + departure_date)

	return "https://www.expedia.com/Flights-Search?" + urllib.urlencode(params), is_round_trip

def get_flights(driver, url, is_round_trip, is_return_flight = False):
	driver.get("about:blank")
	driver.get(url)
	try:
		WebDriverWait(driver, LOAD_TIMEOUT).until(expected_conditions.element_to_be_clickable((By.XPATH, SELECT_BUTTON_XPATH)))
	except TimeoutException:
		print("Timeout Exception: Page didn't loaded successfully")
	page_source = driver.page_source
	doc = html.fromstring(page_source)

	flights = doc.xpath(FLIGHTS_XPATH)
	if is_return_flight:
		flights = flights[:NUM_RETURN_FLIGHTS_TO_DISPLAY]
	else:
		flights = flights[:NUM_FLIGHTS_TO_DISPLAY]

	for flight in flights:
		prices = flight.xpath(PRICES_XPATH)
		if not prices:
			break
		price = prices[0].strip()
		duration = flight.xpath(DURATION_XPATH)[0].strip()
		departure_time = flight.xpath(DEPARTURE_TIME_XPATH)[0].strip()
		arrival_time = flight.xpath(ARRIVAL_TIME_XPATH)[0].strip()
		arrives_next_day = flight.xpath(ARRIVES_NEXT_DAY_XPATH)
		if arrives_next_day:
			arrival_time += arrives_next_day[0].strip()

		if is_return_flight:
			print("   %-11s %-11s %-11s %-11s" % (departure_time, arrival_time, price, duration))
			continue
		print("%-11s %-11s %-11s %-11s" % (departure_time, arrival_time, price, duration))

		if is_round_trip:
			leg_key = flight.xpath(LEG_KEY_XPATH)[0].attrib[LEG_KEY_ATTRIBUTE]
			get_flights(driver, url + "#leg/" + leg_key, is_round_trip, True)

if __name__=="__main__":
	argparser = ArgumentParser()
	argparser.add_argument('departure_airport', help='Departure airport code')
	argparser.add_argument('destination_airport', help='Destination airport code')
	argparser.add_argument('departure_date', help='MM/DD/YYYY')
	argparser.add_argument('return_date', help='MM/DD/YYYY',nargs='?', default="")
	argparser.add_argument('-a', '--adults', help='Number of adults: default 1', default=1)
	argparser.add_argument('-c', '--children', help='Number of adults: default 0', default=0)

	url, is_round_trip = get_url(argparser.parse_args())

	opts = Options()
	opts.set_headless()
	driver = Firefox(options=opts)

	print("Departure   Arrival     Price       Duration   ")
	if is_round_trip:
		print("-> Return Flight Details")

	get_flights(driver, url, is_round_trip)

	driver.close()
