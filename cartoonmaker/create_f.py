from pydub import AudioSegment as AS
import sox
import sys
import os


def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })

    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def increase_volume(name_a):
    song1 = AS.from_file(name_a, format="wav")
    song1 += 5
    song_final = speed_change(song1, 1.5)
    song_final.export(name_a[:-5:] + 'f.wav', format="wav")
    print("increase volume")


cbn = sox.Combiner()

cbn.pitch(4.0)

cbn.convert(samplerate=44100)
try:
    if(len(sys.argv) > 1):
        name_a = sys.argv[1]
        name_v = sys.argv[2]
        uid = sys.argv[3]
    else:
        name_a = input()
        name_v = input()
        uid = input()
    tmp = name_a
    os.system("ffmpeg -i " + name_a + ' ' + name_a[:-4:] + '.wav')
    os.system("rm " + name_a)
    name_a = name_a[:-4:] + '.wav'
    cbn.build([name_a, 'empty.wav'], name_a[:-4:] + '1.wav', 'concatenate')
    increase_volume(name_a[:-4:] + '1.wav')
    # os.system("rm " + name_a)
    os.system('rm ' + name_a[:-4:] + '1.wav')
except Exception as err:
    print("Something's wrong with arguments:\n" + str(err))

# t = input()
######################### main ############################3
audio_name = name_a[:-4:] + 'f.wav'
video_name = name_v

os.system("ffmpeg  -i " + video_name + " " + video_name[:-4:] + '.avi')
# ffmpeg -i test.avi 2>&1 | grep "Duration"
os.system("rm " + video_name)
video_name = video_name[:-4:] + '.avi'

os.system("ffmpeg -i " + uid + "gifka.avi 2>&1 | grep Duration | awk '{print $2}' | tr -d , >> duration.txt")
f = open("duration.txt", 'r')
s = f.read()
print(s)
s = s.split(',')
# s = s[0].split()[1]
s = s[0].split(':')[-1]
video_length = float(s)
f.close()
os.system("rm duration.txt")


os.system("ffmpeg -i " + uid + "voice.wav 2>&1 | grep Duration | awk '{print $2}' | tr -d , >> dur.txt")
f = open("dur.txt", 'r')
l = f.read()
print(l)
# l = l[0].split()[1]
l = l[0].split(':')[-1]
print("AUDIO")
print(l)
audio_length = float(l)
f.close()
os.system("rm dur.txt")

print(audio_length, video_length, sep='\n')
times = audio_length / video_length
if times > 1:
    if int(times) == times:
        pass
    else:
        if abs(times - int(times)) > 0.6:
            times = int(times) + 1
        else:
            times = int(times)
else:
    times = 1
os.system("cat " + (video_name + ' ') * times + "| ffmpeg -f avi -i - video" + "_out_" + video_name[:-4:] +".avi > /dev/null")
os.system("ffmpeg -i " + audio_name + " -i " + "video_out_" + video_name[:-4:] + ".avi " + "" + uid + "FINAL.avi > /dev/null")
os.system("rm " "video_out_" + video_name[:-4:] + ".avi")
os.system("rm " + audio_name)
os.system("rm " + video_name)
os.system("rm " + tmp[:-4:] + '.wav')
print(video_length, audio_length)