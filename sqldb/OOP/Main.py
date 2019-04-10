from Database import Database
from Actions import Actions

database = Database("/home/pineapple/Projects/SofiaTrafic.py/current-state/sqldb/db2-stlite.db")
actions = Actions(database)

actions.create_tables()

# actions.add_favs('micho', '0821', '0534', '1109', '1343')
# actions.add_favs('micho1', '0222', '0221', '0223', '0224')
# actions.add_favs('micho2', '0222', '0221', '0223', '0224')

# actions.del_fav(1, 'fav1')

#actions.add_fav(1, 'fav3', 1109)
