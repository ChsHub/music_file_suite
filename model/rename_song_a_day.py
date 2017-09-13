# -*- coding: utf8 -*-




# file name: "song_name (song_nr.mp3"


def extract_title(x):
    f = x.replace(".mp3", "").split(' (')
    f.pop()
    s = ' ('.join(f)
    return s.replace("_", "")


def extract_track_nr(x, dictionary={'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}):
    x = x.replace(".mp3", "")
    spl_list = x.split('(#', 2)

    if len(spl_list) > 1:
        track_nr = ''
        for s in spl_list[-1]:
            if s in dictionary:
                track_nr += s
        if track_nr is not '':
            return int(track_nr)
    return 0


def set_title(x, cur_dir, new_dir):
    # if '.mp3' not in x:
    #    os.rename(x, x+'.mp3')
    #    x = x+'.mp3'

    title = extract_title(x)
    track_nr = extract_track_nr(x)

    audio_file = eyed3.load(x)

    if audio_file is None:
        info("FAIL: Audio File is none")
        return
    # if 'Jonathan Mann' in x:
    #    info('FAIL: Already renamed')
    #    return
    if track_nr is 0:
        info("FAIL: No Track Nr found")
        return

    # create new tag
    if audio_file.tag is None:
        audio_file.tag = eyed3.id3.Tag()
        audio_file.tag.file_info = eyed3.id3.FileInfo(x)

    audio_file.tag.title = title
    audio_file.tag.track_num = track_nr
    artist_name = u"Jonathan Mann"
    audio_file.tag.artist = artist_name
    audio_file.tag.album_artist = artist_name
    audio_file.tag.album = u"Song A Day"  # album
    audio_file.tag.save()
    os.rename(cur_dir + '/' + x,
              new_dir + '/' + artist_name + ' - ' + title + ' (Song A Day ' + str(track_nr) + ').mp3')
    info("DONE: " + x)
    return


def title_corr(x):
    audio_file = eyed3.load(x)
    if audio_file is not None:
        new_title = audio_file.tag.title
        new_title = new_title.replace('artist_name - ', '')
        audio_file.tag.title = new_title
        audio_file.tag.save()


def rename_titles():
    cur_dir = u'D:/Downloads/Jonathan Mann/mp3'
    new_dir = u'D:/Downloads/Jonathan Mann/finished'
    os.chdir(cur_dir)
    files = os.listdir(u'.')
    # call set_tiles for every file
    # files = [os.rename(x, x.replace(u'♫', '')) for x in files if ".mp3" in x]
    # files = [title_corr(x) for x in files  if ".mp3" in x]
    for x in files:
        if ".mp3" in x:
            set_title(x, cur_dir, new_dir)
            # files = [ ]
            # info(files)


rename_titles()
