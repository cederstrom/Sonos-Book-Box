# coding=utf-8
from Getch import getch
import soco


PRASTENS_LILLA_KRAKA_URI = 'x-sonos-spotify:spotify%3atrack%3a6FDARjuebXcy08AMLLftRk?sid=9&flags=8224&sn=7'


tv_rum = next(x for x in list(soco.discover()) if x.player_name == 'TV-rum')

while(True):
    key = getch()
    print(key)
    if(key == '0'):
        print("Stop playback")
        tv_rum.stop()
    elif(key == '1'):
        print("Playing Prästens lilla kråka")
        tv_rum.volume = 20
        tv_rum.clear_queue()
        tv_rum.play_uri(PRASTENS_LILLA_KRAKA_URI)
    elif(key == 'q'):
        print("Quitting")
        quit()
