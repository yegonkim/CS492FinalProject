# RAVDESS DOWNLOAD
mkdir data
gdown https://drive.google.com/uc?id=1G8Vum5TwDXh6eQ6RjyhEkk6y9GmxQxy4
mv Audio_Speech_Actors_01-24.zip ./ravdess.zip
unzip -q -o ravdess -d ./data/RAVDESS
   
# TESS
gdown https://drive.google.com/uc?id=12HAbGl2iviCDGDluhp3YoiuQBh50y7mS
unzip -q -o TESS -d TESS
rm -rf ./TESS/MANIFEST.TXT
mv TESS ./data/TESS

# RESAMPLED FILE for RAVDESS and TESS (to 16 kHz.)
gdown https://drive.google.com/uc?id=1y--UIcL59C_DRSqf7w63kLa1vWOG5yPp
unzip -q -o rs_audio.zip
mv rs_audio ./data/rs_audio