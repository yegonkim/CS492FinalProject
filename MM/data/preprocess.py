# PREPROCESS IEMOCAP
import os

def get_IEMOCAP_files():

    emos = {'ang': 0, 'exc':0, 'neu':0, 'sad':0}
    final_dict = {'ang': [], 'exc': [], 'neu': [], 'sad': []}

    ## START OF HELPER FUNCTIONS
    #############################

    def find_emotion(txt_file):

        f = open(txt_file, "r")
        # Skip one line.
        next(f)

        data = {}
        for line in f:
            
            if len(line) < 1 or line[0] != '[':
                continue

            idx1 = line.index(']')
            idx2 = line.rindex('[')
            found = line[idx1+1:idx2].strip()
            fname, emo = found.split()

            if emo == 'xxx' or emo not in ['ang', 'exc', 'hap', 'neu', 'sad']:
                continue
            else:
            # Treat happiness same as exc.
                if emo == 'hap':
                    emo = 'exc'
                    emos[emo] += 1
                    data[fname] = emo

        return data

    #############################

    def find_text(txt_file): 
        f = open(txt_file, "r")

        data = {}
        for line in f:
            if len(line) < 1 or line[0] != 'S':
                continue
            idx1 = line.index(' ')
            idx2 = line.rindex(':')
            fname = line[:idx1].strip()
            text = line[idx2+1:].strip()

            data[fname] = text
        
        return data

    # END OF HELPER FUNCTIONS
    #########################

    for i in range(1, 6):
        wav_path = f"/content/IEMOCAP_full_release/Session{i}/sentences/wav"
            
        # FIND EMOTION
        dialog_path = f"/content/IEMOCAP_full_release/Session{i}/dialog"
        emo_path = f"{dialog_path}/EmoEvaluation"
        trans_path = f"{dialog_path}/transcriptions"

        for emo_file in os.listdir(emo_path):
        # IF not txt,
            if emo_file[-3:] != 'txt':
                continue
            else:
                # Gets dictionary of filenames and emotions.
                emo_dict = find_emotion(os.path.join(emo_path, emo_file))
            
                # Get transcription now.
                text_dict = find_text(os.path.join(trans_path, emo_file))
                
                for fname in emo_dict:
                    category = fname[:fname.rindex("_")]
                    real_fname = f"{wav_path}/{category}/{fname}.wav"

                    emotion = emo_dict[fname]
                    text = text_dict[fname]

                    final_dict[emotion].append((real_fname, text))

    return final_dict
    