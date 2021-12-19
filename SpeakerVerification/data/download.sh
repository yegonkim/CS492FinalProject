mkdir -p ./data/RAVDESS
mkdir -p ./data/Libri
mkdir -p ./data/voxceleb/
mkdir -p ./data/BERLIN
mkdir -p ./data/CREMA

# RAVDESS
gdown https://drive.google.com/uc?id=1G8Vum5TwDXh6eQ6RjyhEkk6y9GmxQxy4
# wget -P data/RAVDESS/ https://zenodo.org/record/1188976/files/Audio_Speech_Actors_01-24.zip 
mv Audio_Speech_Actors_01-24.zip ./ravdess.zip
unzip -q -o ravdess -d ./data/RAVDESS

#Libri
wget https://www.openslr.org/resources/12/train-clean-100.tar.gz
tar -zxf train-clean-100.tar.gz --directory ./data/Libri

# VoxCeleb1
wget --user voxceleb1912 --password 0s42xuw6 https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partaa
wget --user voxceleb1912 --password 0s42xuw6 https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partab
wget --user voxceleb1912 --password 0s42xuw6 https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partac
wget --user voxceleb1912 --password 0s42xuw6 https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partad
cat vox1_dev* > vox1_dev_wav.zip
unzip -q -o vox1_dev_wav.zip -d ./data/voxceleb/

#Our dataset
unzip -q -o ./data/our_dataset -d ./data

# BERLIN
gdown https://drive.google.com/uc?id=1OaYxZQbRzSBY5BomY0A8NrVykOTjqS4z
unzip -q -o Berlin_emo
mv ./wav ./data/BERLIN

#CREMA-D
gdown https://drive.google.com/uc?id=1v6vt23yOlIRiQInBhTAgHJNZydpABw6j
unzip -q -o CREMA-D.zip -d ./data/CREMA
rm ./data/CREMA/CREMA-D/AudioWAV/1076_*

rm -rf *.zip *.tar.gz
rm vox1_dev_*
