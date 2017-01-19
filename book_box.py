# coding=utf-8
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser
from Getch import getch
import soco


parser = SafeConfigParser()
parser.read('config.txt')

tv_rum = next(x for x in list(soco.discover()) 
    if x.player_name == parser.get('sonos', 'room_name'))

while(True):
    key = getch()
    print(key)
    if(key == '0'):
        print("Stop playback")
        tv_rum.stop()
    elif(key == 'q'):
        print("Quitting")
        quit()
    else:
        try:
            song_uri = parser.get('songs', key)
            print("Playing %s" % song_uri)
            tv_rum.volume = 20
            tv_rum.clear_queue()
            tv_rum.play_uri(parser.get('songs', key))
        except NoOptionError as no_option_exception:
            print(no_option_exception)
        except Exception as e:
            print(no_option_exception)
