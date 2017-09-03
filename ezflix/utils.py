import subprocess


def cmd_exists(cmd):
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def peerflix(magnet_link, media_player, media_type, subtitles, remove, file_path):
    is_audio = '-a' if media_type == 'music' else ''
    subtitles = "--subtitles '%s'" % file_path if subtitles and file_path is not None else ''
    remove = '--remove' if remove else ''
    cmd = 'peerflix "%s" %s --%s %s %s' % (magnet_link, is_audio, media_player, subtitles, remove)
    print("Executing " + cmd)
    subprocess.Popen(['/bin/bash', '-c', cmd])
