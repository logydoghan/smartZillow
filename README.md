# smartZillow

I. To Start the www server:

npm start

or supervisor ./bin/www

II. To use the web crawler

you will also need a local mongodb

Run "mongoimport --db real_estate_smart_view --collection property --drop property_collection.json"

Please replace all cloud amqp url with your own;

Please replace ZWS_ID with your own;

III. To use Tensorflow

docker image for Jupyter with Tensorflow: 

docker run -d -p 8888:8888 jupyter/tensorflow-notebook

Jupyter Notebook file: jupyter_demo.py can be used for your test;
