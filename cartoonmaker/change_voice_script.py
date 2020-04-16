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


def increase_volume(name):
    song1 = AS.from_file(name, format="wav")

    song1 += 5
    song_final = speed_change(song1, 1.5)
    song_final.export(name[:-4:] + '_final.wav', format="wav")


cbn = sox.Combiner()

cbn.pitch(4.0)

cbn.convert(samplerate=22000)

try:
  name = sys.argv[1]
  cbn.build([name, 'empty.wav'], name[:-4:] + '_sox_out.wav', 'concatenate')
  increase_volume(name[:-4:] + '_sox_out.wav')
  os.system('del ' + name[:-4:] + '_sox_out.wav')
except Exception as err:
  print("Something's wrong with arguments:\n" + str(err))
