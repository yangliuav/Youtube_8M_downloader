# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
import progressbar
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

PATH = os.path.dirname(os.path.abspath(__file__)) 
def create_folder(fd):
    '''Check and create folder for path if the folder is not exited.
    Args:
    fd: string, path of the folder
    '''
    if not os.path.exists(fd):
        os.makedirs(fd)

def get_substring(s, begin_str, end_str):
    ''' Get substring by two given strings.
    Args: 
    s: string, orignal uncutted string
    begin_str: string, the string before the substring 
    end_str: string, the string after the substring
    Return：
    substring: the string bewteen the begin_str and end_str
    '''
    str_begin = s.find(begin_str)
    str_end = s.find(end_str)
    return s[str_begin+len(begin_str):str_end]

class Download():
    def __init__(self):
        self.PATH = os.path.dirname(os.path.abspath(__file__))   
        self.p_bar = progressbar.ProgressBar() 
        self.categories_dict = {}
        categories_file_path = os.path.join(self.PATH,"categories.txt")     
        categories_file = open(categories_file_path,"r")  
        categories_list = categories_file.readlines() 
        
        for categories_item in categories_list:
            self.categories    = get_substring(categories_item, '\"\t', ' (')
            categories_id = get_substring(categories_item, ' \"', '\"\t')
            categories_num= get_substring(categories_item, ' (', ')')
            self.categories_dict[self.categories] = [categories_id,categories_num]

    def download(self, categories_name = "Maltese"):
        video_id_list = self.download_id(categories_name)
        if video_id_list != None:
            self.download_vdeo(video_id_list, categories_name)

    def download_id(self, categories_name = "Maltese"):
        if categories_name in self.categories_dict.keys(): 
            print("Label is Found is categories list")
            categories_id = self.categories_dict[categories_name][0]
            categories_num = self.categories_dict[categories_name][1]
        else: 
            print(categories_name + "is not present")
            return None
        categories_file_dir = os.path.join(self.PATH,"ID")     
        create_folder(categories_file_dir)

        video_content = requests.get('https://storage.googleapis.com/data.yt8m.org/2/j/v/'+ categories_id + '.js').text
        find_item = '\"' + categories_id + '\",[\"'
        video_str = get_substring(video_content, find_item, '\"]')
        video_list = list(video_str.split("\",\"")) 
        video_id_list = []
        print("Getting ID list")
        self.p_bar.start(len(video_list))
        p_count = 0
        for video_item in video_list:
            video_id = requests.get('https://storage.googleapis.com/data.yt8m.org/2/j/i/'+ video_item[0:2] + '/' + video_item + '.js').text
            if video_id[0:10] == '<?xml vers': 
                continue
            video_id = get_substring(video_id, "\",\"", '\")')
            video_id_list.append(video_id)

            p_count = p_count + 1
            self.p_bar.update(p_count)

        self.p_bar.finish()
        print("Found Access density items:" + str(len(video_list) - p_count))
        id_path = os.path.join(categories_file_dir,'{}.txt'.format(self.categories)) 
        categories_file_path = os.path.join(self.PATH, categories_file_dir,'{}.txt'.format(categories_name)) 
        with open(categories_file_path, "w") as filehandle:
            for listitem in video_id_list:
                filehandle.write('%s\n' % listitem)

        print("Successfully save ID at" + id_path)
        return video_id_list

    
    def download_vdeo(self, video_id_list, categories_name):
        self.p_bar.start(len(video_id_list))
        p_count = 0
        vedio_dir= os.path.join(self.PATH,'videos') 
        create_folder(vedio_dir)
        vedio_dir= os.path.join(self.PATH,'videos',categories_name) 
        create_folder(vedio_dir)
        for video_id in video_id_list:
            try: 
                YouTube('http://youtube.com/watch?v='+ video_id).streams.first().download(vedio_dir)
            except VideoUnavailable:    
                try: 
                    YouTube('http://youtube.com/watch?v='+ video_id).streams.first().download(vedio_dir)
                except VideoUnavailable:  
                    print(' http://youtube.com/watch?v='+ video_id)

            p_count = p_count + 1
            self.p_bar.update(p_count)

        self.p_bar.finish()


def main():
    labels_path = os.path.join(PATH,"downloadlist.txt") 
    labels_file = open(labels_path,"r+")  
    labels_list = labels_file.readlines()
    print("Load "+ str(len(labels_list))+ " labels")
    download = Download()
    dcount = 1 
    for label in labels_list:
        download.download(label[0:-1])
        dcount = dcount + 1
        print("Download "+ str(dcount) + " of "+ str(len(labels_list)))
if __name__ == "__main__":
    main()

