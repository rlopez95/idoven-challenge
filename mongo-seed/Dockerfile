FROM mongo

COPY ecg_seed.json /init.json

CMD mongoimport --drop --host mongo --db ecg --collection ecg --mode delete --type json --file /init.json --jsonArray

CMD mongoimport --drop --host mongo --db ecg --collection ecg --type json --file /init.json --jsonArray