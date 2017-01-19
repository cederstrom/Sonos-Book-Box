# coding=utf-8
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser
from Getch import getch
import soco


parser = SafeConfigParser()
parser.read('config.txt')
spotify_uri_pattern = 'x-sonos-spotify:{0}?sid=9'

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
            spotify_uri = parser.get('songs', key)
            sonos_uri = spotify_uri_pattern.format(spotify_uri)
            name = parser.get('songs', key + '_name')
            print("Playing: %s" % name)
            tv_rum.volume = 20
            tv_rum.clear_queue()
            tv_rum.play_uri(sonos_uri)
        except NoOptionError as no_option_exception:
            print(no_option_exception)
        except Exception as e:
            print(e)
