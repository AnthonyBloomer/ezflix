import subprocess


def cmd_exists(cmd):
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def peerflix(magnet_link, media_player, media_type):
    is_audio = '-a' if media_type == 'music' else ''
    print('Playing...')
    subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" %s --%s' % (magnet_link, is_audio, media_player)])