#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ConfigParser import NoOptionError, SafeConfigParser
from Getch import getch
from soco.compat import quote_url
from soco.data_structures import DidlItem, DidlResource
from soco.music_services import MusicService
from soco.music_services.accounts import Account
from threading import Thread, Timer
import soco
import sys
import time


SPOTIFY_SERVICE_TYPE = '2311'


reload(sys)
sys.setdefaultencoding('utf-8')

parser = SafeConfigParser()
parser.read('config.txt')

spotify_accounts = Account.get_accounts_for_service(SPOTIFY_SERVICE_TYPE)
spotify_account = None
if(len(spotify_accounts) == 1):
    spotify_account = spotify_accounts[0]
elif(len(spotify_accounts) > 1):
    spotify_account = next(a for a in Account.get_accounts_for_service(SPOTIFY_SERVICE_TYPE)
        if a.nickname == parser.get('spotify', 'account_nickname'))

spotify = MusicService('Spotify', account=spotify_account)

room = None
sys.stdout.write("Looking for your Sonos player..")
while(room is None):
    sys.stdout.write('.')
    sys.stdout.flush()
    try:
        rooms = soco.discover()
        room = next(x for x in list(rooms)
            if x.player_name == parser.get('sonos', 'room_name'))
        print("\nFound room: %s" % room.player_name)
    except StopIteration as si:
        time.sleep(1)


def _get_queable_item(spotify_uri):
    encoded_spotify_uri = quote_url(spotify_uri)
    didl_item_id = '0fffffff{0}'.format(encoded_spotify_uri)
    uri = spotify.sonos_uri_from_id(encoded_spotify_uri)
    res = [DidlResource(uri=uri, protocol_info="DUMMY")]
    return DidlItem(title="DUMMY",
        # This is ignored. Sonos gets the title from the item_id
        parent_id="DUMMY",  # Ditto
        item_id=didl_item_id,
        desc=spotify.desc,
        resources=res)


def _resume_line_in_playback(volume):
    print('Executing _resume_line_in_playback...')
    room.switch_to_line_in()
    room.volume = volume
    room.play()


restoration_thread = Timer(1, time.sleep, [0])
while(True):
    key = getch()
    print(key)
    if(key == '0'):
        print("Stop playback")
        room.stop()
    elif(key == 'q'):
        print("Quitting")
        quit()
    else:
        try:
            spotify_uri = parser.get('songs', key)
            track = _get_queable_item(spotify_uri)

            was_playing_line_in = room.is_playing_line_in
            if(was_playing_line_in):
                old_volume = room.volume

            room.stop()
            room.volume = parser.get('sonos', 'volume')
            room.play_mode = parser.get('sonos', 'play_mode')
            room.clear_queue()
            room.add_to_queue(track)
            room.play_from_queue(0)
            
            track_info = room.get_current_track_info()
            title = track_info.get('title')
            print("Playing: %s" % title)
            
            duration_array = track_info.get('duration').split(':')
            duration = int(duration_array[0]) * 60 * 60
            duration = duration + int(duration_array[1]) * 60
            duration = duration + int(duration_array[2])

            if(was_playing_line_in is True or restoration_thread.is_alive() is True):
                if(restoration_thread.is_alive() is True):
                    print("Canceling old restoration_thread")
                    restoration_thread.cancel()
                    was_playing_line_in = True
                    
                print("Starting restoration_thread. Waiting %s seconds" % duration)
                restoration_thread = Timer(duration, _resume_line_in_playback, [old_volume])
                restoration_thread.start()
                
        except NoOptionError as no_option_exception:
            print(no_option_exception)
        except Exception as e:
            print(e)
