sudo docker pull gcr.io/object-detect-179719/object-detect

sudo docker run -it -p 6006:6006 -p 8888:8888 -p 5000:5000 gcr.io/object-detect-179719/object-detect

gcloud config set project object-detect-179719

python mountain_lion_data/create_pet_tf_record.py \
    --label_map_path=`pwd`/mountain_lion_data/mountain_lion_label_map.pbtxt \
    --data_dir=`pwd`/mountain_lion_data \
    --output_dir=`pwd`


####
gather images from google and bing or whatever into images_orig_.  Rename them sequentially using rename_files.py into images_new


####
annotate the files in images using rectlab - downloaded on MAC


