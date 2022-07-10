import argparse
import madmom
import midiutil

def setup() -> argparse.Namespace:

    """ Setup and parse the command line arguments. Exit with errors.
    """

    parser = argparse.ArgumentParser("Create a MIDI tempo track from an audio file.")
    parser.add_argument("input_file", nargs="+", type=str, metavar="input_file")

    return parser.parse_args()

def main():

    """ Main logic
    """
    
    # get command line args (or error out)
    args = setup()
    
    # itterate over file names passed on the command line
    for f in args.input_file:

        print("Input: {}".format(f))

        # using the madmom python library (https://github.com/CPJKU/madmom) to do
        # downbeat detection. See the README there for details about how this works

        proc = madmom.features.DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)
        act = madmom.features.RNNDownBeatProcessor()(f)
        downbeats = proc(act)

        print("Creating MIDI tempo file...")

        # create a new MIDI file with 1 track. Name the track "Tempo Track"
        mf = midiutil.MIDIFile(1)
        mf.addTrackName(time=0, track=0, trackName="Tempo Track")

        # the items contained in downbeats are in the form of:
        # 
        # [time_in_sec, bar_position]
        #
        # we're going to add an audible click everytime we get to a 
        # bar_position of 1. We are also going to compute the tempo of
        # the track since the last click we added to keep things lined
        # up
        #

        last_bar_top_index = 0

        for i in range(1, len(downbeats)):
            time_stamp, bar_position = downbeats[i]

            if bar_position != 1:
                continue

            last_bar_top_timestamp, _ = downbeats[last_bar_top_index]
            bar_duration = time_stamp - last_bar_top_timestamp

            bar_tempo = ((i - last_bar_top_index)/bar_duration) * 60

            mf.addTempo(track=0, time=last_bar_top_index, tempo=bar_tempo)
            mf.addNote(track=0, channel=9, pitch=56, time=i,  duration=1, volume=255)

            last_bar_top_index = i

        # write the MIDI file
        with open (f + ".tempo.mid", "wb") as of:
            mf.writeFile(of)

if __name__ == "__main__":
    main()
