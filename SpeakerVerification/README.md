Download the required models with download.sh
Run
```
./download.sh
```

To perform speaker verification, import `enroll_and_test`, and run
```
eval(enroll_paths, test_path)
```
with `enroll_paths` being a list of paths (string format) to enrollment .wav files, and `test_path` being the path (str) to .wav file for testing.

The `.wav` files should have sampling rate of 16kHz.
