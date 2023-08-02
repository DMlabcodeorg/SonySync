import argparse
from AudioFlagFinder import AudioFlagFinder
# from timeit import default_timer as timer

def parse_option():
    parser = argparse.ArgumentParser('argument for feature extraction from trained models')

    parser.add_argument('--input_path', type=str, default='Audio',
                        help='Name of directories you want to input audios from together (you can have as many as you want)')
    parser.add_argument('--output_path', type=str, default='output',
                        help='Output directory of the csv file of all audios (no need to type ".csv" at the end')
    parser.add_argument('--flag_freq', type=int, default=3000,
                        help='frequency of the flag (beep) you are looking for')
    parser.add_argument('--time_cut', type=int, default=3600,
                        help='to analyze only the first n seconds of each audio')
    opt = parser.parse_args()
    return opt
'''    
# Constructor params:
    # input_path_list: List of directories you want to input audios from together (you can have as many as you want)
input_path_list = ['./SonySync']

    # output_directory: Output directory of the csv file of all audios (no need to type ".csv" at the end)
output_directory = './SonySync'
'''
    # n_fft: window size for limbrosa (would leave it at default 256 unless you know what you are doing)
def main():
    opt_get = parse_option()
    input_path_list = [opt_get.input_path]
    output_directory = opt_get.output_path
    audio_obj = AudioFlagFinder(input_path_list=input_path_list, output_directory=output_directory, n_fft=256)

    # find_flag: finds the flag (or beep) of the specified frequency and length.
    # params:
        # flag_freq              (integer, default = 3000): frequency of the flag (beep) you are looking for
        # offset                 (integer, default = 10):   + or - Hz to flag_freq
        # max_gap_time           (float, default = 0.035):  measured in seconds - largest break time in between for beep
        # min_flag_candidate_req (float, default = 0.3):    time measured in seconds to be considered a valid beep canidate
        # time_cut               (integer, default = None): to analyze only the first n seconds of each audio

    audio_obj.find_flag(flag_freq=opt_get.flag_freq, offset=10, max_gap_time=0.035, min_flag_candidate_req=0.3, time_cut=3600)


    # OTHER NOTES:
    # In the output the mean gap difference needs to be fixed, ignore for now... but for reference on average it's supposed to be about 0.004-0.012 seconds
    # You can go to lines (43, 128, 130) to comment out prints you may not be interested in

if __name__ == '__main__':
    main()