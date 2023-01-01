from pytube import YouTube
video = YouTube("https://www.youtube.com/watch?v=SVvr3ZjtjI8&ab_channel=NeetCode")
print(video.title)
#print(video.description)
print(video.length)
print(video.streams)
# # Exemple Class Media
# class Media:
#     __init__(self,)