import librosa
import numpy as np
import pandas as pd
import os
# import sys
# from timeit import default_timer as timer

class AudioFlagFinder:

    def __init__(self, input_path_list, output_directory, n_fft=256):
        self.input_path_list = input_path_list
        self.output_directory = output_directory
        self.n_fft = n_fft
    
    def find_flag(self, flag_freq=3000, offset=10, max_gap_time=0.035, min_flag_candidate_req=0.3, time_cut=None):
        #offset --> + or - Hz to flag_freq 
        #max_gap_time --> measured in seconds - largest break time in between for beep 
        #min_flag_candidate_req --> time measured in seconds to be considered a valid beep canidate
        #time_cut --> to analyze only the first "time_cut" in seconds of each audio
        
        # Arrays that hold all the 
        flag_start_time = []
        flag_end_time = []
        
        if type(self.input_path_list) != type([]):
            print('\n\nThe input_path_list parameter must be a list of input directories...\n')
            print('\nWe test with flag frequency {} and time cut {}\n'.format(flag_freq, time_cut))
            exit()
        
        for folder_dir in self.input_path_list:
                
            # Gets the folder path (as well as the folder itself) and then replaces the slashes (reversed)  
            # path_to_folder = os.path.dirname(os.path.realpath(sys.argv[0])).replace("\\","/")

            self.file_str_array = os.listdir(folder_dir)
            
            try:
                beep_df = pd.read_csv(self.output_directory + '.csv', header=0, index_col=0)
                curr_saved_flags = beep_df[['file_name']].values
                self.file_str_array = [n for n in self.file_str_array if n not in curr_saved_flags
                                       and n.split('.')[-1] == 'wav']
            except:
                pass
                
            print('List of audios found in: \n\t' + folder_dir +'\n audios ---> ', self.file_str_array)

            for file_name in self.file_str_array:
                print('\n\nCurrently on: ', file_name)

                # Load the WAV file         
                audio_path = folder_dir + '/' + file_name
                
                # samples raw data, and rate is the number of time the points are measured
                samples, sample_rate = librosa.load(audio_path, sr=None)
                if time_cut:
                    samples = self.cut_audio_by_time(samples, sample_rate, 0, time_cut)            
                
                # Window size of fft measurement
                self.quotient = float(2048/self.n_fft)

                # Compute the Short-Time Fourier Transform (STFT)
                stft = librosa.stft(samples, n_fft=self.n_fft)
                
                # Convert the STFT time stamps
                self.time_stamps = librosa.core.frames_to_time(range(stft.shape[1]), sr=sample_rate)
                # time_stamps = time_stamps

                # Computes the frequencies and magnitudes
                freqs, magnitudes = librosa.core.piptrack(y=samples, sr=sample_rate, S=None, n_fft=self.n_fft, hop_length=None, fmin=150.0,
                                                        fmax=20000.0, threshold=0.1, win_length=None, window='hann', center=True, pad_mode='reflect', ref=None)

                # Stores the frequencies (indices of pitches match time_stamps)
                pitches = []

                # Stores all the beep candidates
                slice_t = []
                candidate = []
                prev_t = 0
                print('looking for candidates...')
                for t in range(len(self.time_stamps)):
                    freq = int(self.get_freq(freqs, magnitudes, t))
                    pitches.append(freq)
                    #if freq > flag_freq - offset: #and freq < flag_freq + offset:
                    #    print(self.time_stamps[t]/self.quotient, freq)

                    # Range of frequencies that we are searching for
                    if freq > flag_freq - offset and freq < flag_freq + offset:
                        # print(self.time_stamps[t]   , t)

                        # To make sure the timestamps are continues
                        if self.time_stamps[t] - self.time_stamps[prev_t] <= max_gap_time*self.quotient:
                            candidate.append(t)
                        else:
                            if len(candidate) and self.time_stamps[candidate[-1]] - self.time_stamps[candidate[0]] > min_flag_candidate_req*self.quotient:
                                slice_t.append(candidate)
                            candidate = []
                        prev_t = t

                    if self.time_stamps[t] - self.time_stamps[prev_t] > max_gap_time*self.quotient and len(candidate) and self.time_stamps[candidate[-1]] - self.time_stamps[candidate[0]] > min_flag_candidate_req*self.quotient:
                        slice_t.append(candidate)
                        candidate = []
                        
                # Stores the smallest mean difference (most likely candidate)
                curr_mean_diff = 10000

                # If there is no flag tone in the audio 
                if slice_t == []:
                    print("No Beep Found, will not be saved in csv.")
                    flag_start_time.append(None)
                
                # Else, beep tone is found 
                else:     

                    # Stores the best beep candidate
                    best_slice = slice_t[0]

                    # Finds the best beep candidate
                    print('candidates mean_diff: ', end="")
                    for slice in slice_t:
                        mean_d, max_gap_in_slice = self.mean_difference(slice)
                        mean_d = mean_d / self.quotient
                        print(mean_d, end=", ")
                        if mean_d < curr_mean_diff:
                            curr_mean_diff = mean_d
                            curr_max_gap_in_slice = max_gap_in_slice
                            best_slice = slice
                    print()
                        
                    flag_start_time.append(self.time_stamps[best_slice[0]]/self.quotient)
                    flag_end_time.append(self.time_stamps[best_slice[-1]]/self.quotient)
                    print(file_name + ":\nFlag start time, end time, length, mean_gap_diff, n_cands: ", flag_start_time[-1], flag_end_time[-1], flag_end_time[-1] - flag_start_time[-1], curr_mean_diff, len(slice_t))
                    # print('slice length, max gap in slice, best_slice: ', len(best_slice), curr_max_gap_in_slice, [self.time_stamps[x] / self.quotient for x in best_slice])
                    print('slice length, max gap in slice: ', len(best_slice), curr_max_gap_in_slice)
                
                if flag_start_time[-1]: 
                    # Read from CSV 
                    try:
                        beep_df = pd.read_csv(self.output_directory + '.csv', header=0, index_col=0)
                    except: # Creates a CSV if it does not already exist 
                        columns = ['file_name','flag_start_time'] #Column titles 
                        beep_df = pd.DataFrame(columns=columns)
                        beep_df = beep_df.loc[:, ~beep_df.columns.str.contains('^Unnamed')]
                    
                    # Writes to CSV
                    beep_df.loc[len(beep_df.index)] = [file_name, flag_start_time[-1]]
                    beep_df.to_csv(self.output_directory +'.csv') 

    # Finds the frequency at timestamp t
    def get_freq(self, freqs, magn, t):
        i = magn[:, t].argmax()
        return freqs[i, t]

    # Computes the mean difference of the beep candidate lst
    def mean_difference(self, slice):
        # diff_arr = np.diff(np.array(slice/self.quotient))
        diff_arr = np.diff(np.array([self.time_stamps[t]/self.quotient for t in slice]))
        # return sum(slice[i+1] - slice[i] for i in range(len(slice)-1)) / (len(slice)-1)
        return np.mean(diff_arr), diff_arr.max()
    
    def cut_audio_by_time(self, input_samples, sample_rate, start_time, end_time):
        # Calculate the start and end samples
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)

        # Extract the portion of the audio
        audio_portion = input_samples[start_sample:end_sample]

        return audio_portion