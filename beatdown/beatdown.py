import argparse
import madmom
import midiutil

def setup() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Create a MIDI tempo track from an audio file.")
    parser.add_argument("input_file", nargs="+", type=str, metavar="input_file")

    return parser.parse_args()

def main():

    args = setup()
    
    for f in args.input_file:

        print("Input: {}".format(f))

        proc = madmom.features.DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)
        act = madmom.features.RNNDownBeatProcessor()(f)
        downbeats = proc(act)

        print("Creating MIDI tempo file...")

        mf = midiutil.MIDIFile(1)
        mf.addTrackName(time=0, track=0, trackName="Tempo Track")

        last_pos = 0
        last_index = 0

        for i, item in enumerate(downbeats):

            if item[1] != 1 or i == 0:
                continue

            duration = item[0] - last_pos
            tempo = ((i-last_index)/duration) * 60

            mf.addTempo(track=0, time=i, tempo=tempo)
            mf.addNote(track=0, channel=9, pitch=56, time=i, duration=1, volume=255)

            last_pos = item[0]
            last_index = i

        with open (f + ".tempo.mid", "wb") as of:
            mf.writeFile(of)

if __name__ == "__main__":
    main()
