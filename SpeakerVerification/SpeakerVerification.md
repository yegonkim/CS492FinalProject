Download the required models with download.sh
Run
'''
./download.sh
'''

To perform speaker verification, import 'enroll_and_test', and run
'''
eval(enroll_path, test_path)
'''
with enroll_path, test_path being the paths (str) to .wav files for enrollment and testing, respectively.
