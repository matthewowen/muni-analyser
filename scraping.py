from BeautifulSoup import BeautifulStoneSoup
import sqlite3, requests, time, multiprocessing, boto, os
from settings import AWS_KEY, AWS_SECRET
from urllib import quote

DATABASE = os.path.abspath(os.path.dirname(__file__)) + '/db'


def get_content(URL):
    """
    Pass a URL. Get back some Beautiful Soup.
    """

    req = requests.get(URL, timeout=15)
    soup = BeautifulStoneSoup(req.content, selfClosingTags='stop')
    return soup


def run_cycle():
    """
    Run the lovely cycle of getting times
    """

    def do_stop(stop):
        url = "http://webservices.nextbus.com/service/publicXMLFeed?" \
              "command=predictions&a=sf-muni&r=%s&s=%s" % (stop[1], stop[0])

        soup = get_content(url)

        time_now = time.time()

        vehicles = soup.findAll('prediction')

        for vehicle in vehicles:
            data = {}
            data['trip'] = vehicle['triptag']
            data['time'] = time_now
            data['stop'] = stop[0]
            data['route'] = stop[1]
            data['togo'] = int(vehicle['seconds'])
            item_name = '%s:%s:%s' % (data['time'], data['stop'], data['trip'])

            dom.put_attributes(item_name, data)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('SELECT stop_id, route_tag from routestops where rowid % 4 == 0')

    r = c.fetchall()

    conn = boto.connect_sdb(aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET)
    dom = conn.get_domain('predictions')

    started = time.time()

    processes = []
    for stop in r:
        p = multiprocessing.Process(target=do_stop, args=(stop,))
        p.start()
        processes.append(p)

    for process in processes:
        process.join(60)


# set this up in cron so that this script runs periodically
run_cycle()
