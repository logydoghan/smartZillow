#!/bin/bash

RAW_DATA_PATH=/tmp/raw_data.csv

# Export data from MongoDB
mongoexport --host localhost --db real-estate-smart-view --collection property --type=csv --out $RAW_DATA_PATH --fields zipcode,longitude,latitude,is_for_sale,property_type,bedroom,bathroom,size,list_price,last_update

# Remove previous model files
rm -r ./model/

# Trigger the trainer
python trainer.py $RAW_DATA_PATH