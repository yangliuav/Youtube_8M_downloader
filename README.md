# Youtube-8M Downloader

This repository provides a moudle to download the original videos in [Youtube-8m dataset](https://research.google.com/youtube8m/index.html)

Since the official `youtube-8m dataset` website contains only videos and frame level features in the format of tensorflow protocal buffers. Hence, in this repository I write a tool to download the orignal vedios. 

## Installation

Dependencies for downloading youtube video ids for categories
```
    pip install requests pytube progressbar
```
or 
```
    conda install requests progressbar
    conda install -c everwho pytube
```
## Preparation

1. Open `categories.txt`. 
2. Select the categories and paste them into `downloadlist.txt`. Note, there is only one category for each line and the first letter of each category is Capitalized.
3. Save `downloadlist.txt`.

## Download category videos and ids

```
    python downloader.py
```
The IDs of each category are saved at the folder 'ID'. The file of ID are named as the categories.

The Vedios of each category are saved at the folder 'vedios\YOUR CATEGORY NAME'. By default a video is downloaded in the best possible resolution. 

## Known problems and solutions
### 403 forbidden issues on signed videos
Please see [pytube](https://github.com/nficano/pytube/pull/453/commits/fac934b149bc2d49ea54d566e0639d9b4c2862d2)

## Contact

If you have any questions or suggestions about the code, feel free to create an issue.