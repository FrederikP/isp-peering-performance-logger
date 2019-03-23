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
    download_sample 'ard' 'https://dasersteuni-vh.akamaihd.net/i/de/2019/03/22/ee56c487-3f1c-489f-bb13-2c51fd3872ec/,320-1_379735,512-1_379735,960-1_379735,480-1_379735,640-1_379735,1280-1_379735,.mp4.csmil/segment3_5_av.ts?null=0' >> $logfile
    sleep 10m
done