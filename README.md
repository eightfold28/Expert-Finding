# Expert-Finding


Expert finding system development in Indonesia's academic institution.
*Education purpose only.*


### Abstract

Expert is a person who is recognized to have a comprehensive and authoritative knowledge of or skill in a particular area. Expert finding is important and needed both in industry and academy. One of the shortcomings of existing expert finding system is that there is no expertise validation for the expert’s skills which is selfproclaimed. Furthermore, the criteria to determine someone's expertise is portrayed poorly through their profile page and those criteria might not meet finder's needs for expertise sufficiently. Currently in Indonesia, there is no system to accommodate the need of finding expert publicly, specifically for educational institutions. 

Expert finding system in this research is developed by using Indonesia’s lecturers data taken by PD Dikti Indonesia website. The system consists of two main subsystem, which are classifying the expertise area based on the problems given and recommending the suitable lecture in accordance with the expertise classification result. Data is collected by crawling through the website. Classification model is built using machine learning approach with feature extraction using TF-IDF. The expert candidate’s score is calculated using weighted sum model method by which the weight and score are determined by admin. Criterias to determine expert are education, research, teaching, position, and community service (project). The system is a web application developed using Django framework. For validation, the system is tested using 3 methods, which are functionality, classification model quality, and expert recommendation quality. From the result, it can be concluded that the system requirement is satisfied. The classification model is adequate with 79% accuracy with Random Forest algorithm for 10 class classification. 

The system is expected to be used by government and education institution to find the expert recommendation especially lecturer for projects or community services. In the future, it is suggested that the multi-label classification model will be used so that the expertise area classification could be more accurate to address the problem given. 


### About this repo


This repo includes:
1. Source code to develop the web-based system, build a classification model, keyword-based to classify a subject, crawl PD Dikti's web, and script to migrate data from Mongo to mySQL
2. Data used (lecturers (.json), projects (.csv), subjects (.csv), research (.csv)) and the sql dump (both in .sql and .csv for each table)


### Limitation


- Due to max file size limit in Github, some data will be truncated using some filters I applied (POC only)
- Scope for this project is only for Informatics and CS related
- Lecturers data is only from PD Dikti
- Projects data is only from LPPM and LAPI ITB
- Only Bahasa Indonesia is used for the whole system


## Running the Project

### Django Web

You have to make sure you have python and pip installed.
I used `python 3.6.4` and `pip 10.0.1`.

Then install the requirement as listed in requirements.txt with command:
```sh
$ pip install -r requirements.txt
```

Migrate Django model:
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

To run server in localhost:8000/caripakar_app:
```sh
$ python manage.py runserver 
```

For the first time, you have to update the db related to the lecturers' data first:
  - to update the number of research and teachings of lecturers
  - to update lecturers' score
  - to update z_score of each aspect

Run these commands:
```sh
$ python manage.py update_total_penelitian_pengajaran
$ python manage.py update_skor_dosen 
$ python manage.py update_z_skor
```

### Classifier

**Run classification and load model** were made using Python on top of Jupyter Notebook.
You could install Anaconda Navigator for complete package and launch Jupyter there.


### Scrapy

Install the requirements as listed in requirements.txt using `pip`

1. Get list of all universities and output to csv
```sh
$ scrapy crawl forlap_daftar_univ -o data_univ.csv
```

2. Get id of each university
```sh
$ python map_univ_name_to_id.py
```

3. Crawl lecturers' data
```sh
$ scrapy crawl forlap_daftar_dosen
```

Data is pushed in dictionary form and saved to Mongo DB.
To access the data, you have to install [Mongo](https://www.mongodb.com/).
You can export the data to json using this command:
```sh
$ mongoexport --host=localhost --port=27017 --db=forlapdikti --collection=daftar_dosen --out=data.json
```

You could also use some query when exporting the data. 
For example to choose lecturers' data who only teach IF or STI subjects and from ITB, query could be added like this:
```sh
mongoexport --db=datadosenfull --collection=daftar_dosen --query='{"perguruan_tinggi": "Institut Teknologi Bandung", "program_studi": { $in: ["Informatika", "Sistem dan Teknologi Informasi"] }}' --out=dataitbifsti.json 
```


**Feedback is much appreciated. Thank you!**
