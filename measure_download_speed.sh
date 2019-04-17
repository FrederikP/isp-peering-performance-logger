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
    download_sample 'ard' 'https://dasersteuni-vh.akamaihd.net/i/int/2019/04/15/3f90bbab-6d00-4a57-8d6f-167fff3f32e1/,960-1_391599,640-1_391599,512-1_391599,480-1_391599,320-1_391599,1280-1_391599,.mp4.csmil/segment13_5_av.ts?null=0' >> $logfile
    sleep 10m
done