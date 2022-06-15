#!/usr/bin/env python

# youtube-dl https://www.youtube.com/watch?v=r9ZofmOJtm8

import os
import subprocess
import shutil
import requests

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from huepy import *
from bs4 import BeautifulSoup
from pytube import YouTube

def return_good_view(item):
    counter = 0
    for k in range(len(item)-1, 0, -1):
        if item[k] == '.':
            break
        counter += 1


    return item[:len(item)-counter-1:]

def transform(videoname):
    counter = 0
    for k in range(len(videoname)-1, 0, -1):
        if videoname[k] == '-':
            break
        counter += 1

    counter_for_format = 0
    for k in range(len(videoname)-1, 0, -1):
        if videoname[k] == '.':
            break
        counter_for_format += 1

    return videoname[:len(videoname)-counter-1:] + videoname[len(videoname)-counter_for_format-1::]


def download_video(url):
    # os.chdir('/home/starrk/Documents/Learning/new_python_learning/cutting_videos')
    os.chdir(os.getcwd())
    soup = BeautifulSoup(requests.get(url).text, 'html')

    print(os.system('pwd'))

    another_listdir = []
    for k in os.listdir('static/videos'):
        another_listdir.append(return_good_view(k))

    givenName = soup.find('title').text.split('- YouTube')[0].strip()

    print('{} in {} == {}'.format(
        givenName,
        another_listdir,
        givenName in another_listdir))

    if givenName in another_listdir:
        videoname = os.listdir('static/videos')[0]
        counter = 0
        for k in range(len(videoname)-1, 0, -1):
            if videoname[k] == '.': break
            counter += 1
        try:
            givenName = videoname.split('____')[0] + '____' + str(int(videoname.split('____')[1].split('.')[0])+1) + '.' + videoname.split('____')[1].split('.')[1]
        except:
            givenName += '____1' + videoname[len(videoname)-counter-1::]

        os.chdir('another_folder')
        # output = subprocess.Popen(['youtube-dl', '{}'.format(url)], stderr=subprocess.PIPE).communicate()[0] # downdloading highest format of video

        videoname = os.listdir()[0]

        os.rename(videoname, givenName)
        os.chdir('../')

        return givenName


    try:
        os.mkdir('another_folder')
    except:
        shutil.rmtree('another_folder')


    print(orange('='*8))



    os.chdir('another_folder')
    output = subprocess.Popen(['youtube-dl', '{}'.format(url)], stderr=subprocess.PIPE).communicate()[0] # downdloading highest format of video
    videoname = os.listdir()[0]

    another_name = transform(videoname)
    os.rename(videoname, another_name)
    os.chdir('../')


    return another_name


# https://www.youtube.com/watch?v=r9ZofmOJtm8

def cut_video(name, time_code_start, time_code_end):
    os.chdir('/home/starrk/Documents/Learning/new_python_learning/cutting_videos')
    another_listdir = []
    for k in os.listdir('static/videos'):
        another_listdir.append(return_good_view(k))

    videosize = VideoFileClip('another_folder/{}'.format(name)).duration
    if time_code_end > videosize:
        raise Exception("Конец обработки видео больше, чем нужно. Попробуйте еще раз \nVideoduration = {}".format(videosize))


    os.chdir('another_folder')

    ffmpeg_extract_subclip('{}'.format(name), time_code_start, time_code_end, targetname='another_{}'.format(name))
    os.remove(name)
    os.rename('another_'+name, name)

    os.chdir('../')
    print(red(name))

    # os.system("mv another_folder/'{}' static/videos/".format(name))
    subprocess.Popen(['mv', 'another_folder/{}'.format(name), 'static/videos'])

    print(red('================='))


def prepare_second(item): 
    return int(item.split(':')[0].strip())*60 + int(item.split(':')[1])

def main(correct_name = False):
    os.chdir('/home/starrk/Documents/Learning/new_python_learning/cutting_videos')
    print("Можно вводить в таком формате: 3:26, 6:33")
    video_url = input("Введите ссылку: ")
    time_code_start = prepare_second(input("Введите откуда обрезать: "))
    time_code_end = prepare_second(input("Введите докуда обрезать: "))

    if time_code_start > time_code_end: main()



    videoname = download_video(video_url)

    # os.chdir('../')
    # print(red(os.system('pwd')))

    try:
        if videoname in os.listdir('another_folder'):
            cut_video(videoname, time_code_start, time_code_end)

        print(videoname)
        cut_video(videoname, time_code_start, time_code_end)

    except:
        main()

if __name__ == '__main__':
    main()
