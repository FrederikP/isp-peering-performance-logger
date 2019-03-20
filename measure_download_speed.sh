logfile='ispspeed.log'

download_sample () {
    datetime=$(date --iso-8601=seconds)

    result=$(curl $2 -o /dev/null -w %{speed_download} -s)
    speed="${result%%,*}"
    echo "$1 ${datetime} ${speed}"
}

while :
do
    download_sample 'reddit' 'https://external-preview.redd.it/mp4/Y0CsmhfSFvu_HqysQA1Ed4oD73OtpsYorCIFJrSgvYw-source.mp4?s=c24d071636a35de8bfad866c018bed59672234ae' >> $logfile
    download_sample 'tagesschau' 'https://hlstagesschau-vh.akamaihd.net/i/video/2019/0314/TV-20190314-2104-3701.,webs,webm,webl,webxl,.h264.mp4.csmil/segment3_3_av.ts?null=0' >> $logfile
    sleep 10m
done