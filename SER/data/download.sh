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

# BERLIN
gdown https://drive.google.com/uc?id=1OaYxZQbRzSBY5BomY0A8NrVykOTjqS4z
unzip -q -o Berlin_emo
mv ./wav ./data/BERLIN

# MELD
wget http://web.eecs.umich.edu/~mihalcea/downloads/MELD.Raw.tar.gz
mkdir ./data/MELD
tar -zxvf MELD.Raw.tar.gz --directory ./data/MELD

tar -zxvf /content/data/MELD/MELD.Raw/test.tar.gz --directory ./data/MELD
tar -zxf /content/data/MELD/MELD.Raw/dev.tar.gz --directory ./data/MELD
tar -zxf /content/data/MELD/MELD.Raw/train.tar.gz --directory ./data/MELD
mv /content/data/MELD/MELD.Raw/*.csv /content/data/MELD
rm -rf MELD.Raw

rm -rf *.zip *.tar.gz

# OR optionally you could directly get MELD MP3 files with...   
# gdown https://drive.google.com/uc?id=1-gbzOCBcuS-IcMx6-667qnCsbNi1iq3G