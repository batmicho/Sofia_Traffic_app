from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql
import json
import urllib
import os

from sqldb.OOP.Actions import Actions
from sqldb.OOP.Database import Database
from Checks.Checks import Checks

application = Flask(__name__)

# Set the secret key:
application.secret_key = '\xf4:\xf51%\x8d?w\x8d\xd2\xdd\x84Q\xaci\xcb\xcbF&\x8bnQq\x9e'
# Loaded module checks + file for checking.
allstopsids = 'Checks/busstops.json'
checks = Checks(allstopsids)
# Loaded modules for database conn and actions + file of database.
database = Database('db2-stlite.db')
actions = Actions(database)


@application.route('/')
def index():
    # list of users and we get the first element which is dict.
    user_row = actions.select_usr(sql, 2)
    # list_new only stops from the dict.
    #print user_row
    list_new = [user_row['fav1'], user_row['fav2'],
                user_row['fav3'], user_row['fav4']]
    # filter funct checkes all elements from the list and removes the condition if not met.
    list_new = filter(lambda x: x is not None, list_new)
    #print user_row

    return render_template('base.html', usr_filtered_stops=list_new)


@application.route('/', methods=['POST'])
def check_post():
    session['userSt_id'] = request.form['userStop_id']
    return redirect(url_for('check'))


@application.route('/t', methods=['GET'])
def check():
    # User data input:
    stopId = session['userSt_id']
    # Check if input is correct stop ID:
    newStop = checks.validids(stopId)

    if os.getenv("KDE_FULL_SESSION") == 'true':
      # ---Offline-
        # Local usage.
        json_busdata = open('incomming_bus_data.json').read()
        busdata = json.loads(json_busdata)
       # -/-offline-
    else:
      # --Online--
        url = ('https://api-arrivals.sofiatraffic.bg/api/v1/arrivals/')
        new_stop_search = url + newStop + '/'
        # Get request to the API url returns the page(a json file)which is read and  decoded as json from python
        stop_api_call = urllib.urlopen(new_stop_search)
        raw_data = stop_api_call.read()
        # Tso json:
        busdata = json.loads(raw_data)
  # -/-Online--
    # Into vars to manipulate and display:
    calculated_at = busdata['timestamp_calculated']
    stop_name = busdata['name']
    for lines in busdata['lines']:
        for time in lines['arrivals']:
            times = time
    session.pop('userSt_id', None)

    # Gets all rows from db favids.
    user_row = actions.select_usr(sql, 2)
    # list_new only stops from the dict.
    list_new = [user_row['fav1'], user_row['fav2'],
                user_row['fav3'], user_row['fav4']]
    # filter funct checkes all elements from the list and removes the condition if not met.
    list_new = filter(lambda x: x is not None, list_new)

    return render_template('arrival-info.html', coming_lines=times, stop_id=stopId, busdata=busdata,  calculated_arrival_at=calculated_at, stop_name=stop_name, usr_filtered_stops=list_new)


@application.route('/dobavi', methods=['GET'])
def topstops():

    user_row = actions.select_usr(sql, 2)
    list_new = [user_row['fav1'], user_row['fav2'],
                user_row['fav3'], user_row['fav4']]
    # filter funct checkes all elements from the list and filters any item where the condition is FALSE.
    list_new = filter(lambda x: x is not None, list_new)
    #{'fav1': u'0821', 'fav4': u'1343', 'fav3': u'1109', 'name': u'micho', 'id': 2}
    usr_filtered_stops = {k: v for k, v in user_row.iteritems(
    ) if v is not None and k in ('fav1', 'fav2', 'fav3', 'fav4')}
    stops_list = []
    for k, v in usr_filtered_stops.iteritems():
        stops_list.append({'name': k, 'value': v})
    #[{name: 'fav1', value: '1125'}, {name: 'fav2', value: '1245'}]
    # stop_list e kato goreniq red

    return render_template('add-topids.html', user_name=user_row['name'], user_stops=list_new, stops=stops_list, usr_filtered_stops=list_new)


@application.route('/addfav', methods=['POST'])
def addfav():
    # Form responce with user insert data.
    stopId = request.form['userFav_Stop_id']
    print ("%s" % (stopId))
    # Check if input valid stop-id.
    newStop = checks.validids(stopId)
    # Check if there is favs spots empty and add them to list.
    usr_row = actions.select_usr(sql, 2)
    add_bussid = []

    if usr_row['fav1'] == None:
        print "fav1"
        add_bussid.append('fav1')
    elif usr_row['fav2'] == None:
        print "fav2"
        add_bussid.append('fav2')
    elif usr_row['fav3'] == None:
        print "fav3"
        add_bussid.append('fav3')
    elif usr_row['fav4'] == None:
        print "fav4"
        add_bussid.append('fav4')
    else:
        print "all are not null"
    # Update first added fav slot with new user buss id.
    print add_bussid[0]
    actions.add_fav(2, add_bussid[0], newStop)

    return redirect(url_for('topstops'))


@application.route('/remfav', methods=['POST'])
def remfav():

    removeId = []
    try:
        fav1 = request.form['fav1']
        removeId.append('fav1')
    except:
        fav1 = None
    try:
        fav2 = request.form['fav2']
        removeId.append('fav2')
    except:
        fav2 = None
    try:
        fav3 = request.form['fav3']
        removeId.append('fav3')
    except:
        fav3 = None
    try:
        fav4 = request.form['fav4']
        removeId.append('fav4')
    except:
        fav4 = None

    #print ('del fav1 %s del fav2 %s dev fav3 %s del fav4 %s' % (fav1, fav2, fav3, fav4))
    print removeId[0]

    actions.del_fav(2, removeId[0])

    return redirect(url_for('topstops'))


@application.errorhandler(500)
def page_not_found(e):
    return render_template('500-error.html'), 500


if __name__ == '__main__':
        #application.debug = True
    application.run(host='127.0.0.1')
