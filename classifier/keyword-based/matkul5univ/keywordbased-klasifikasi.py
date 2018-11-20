
# coding: utf-8

# In[27]:


def create_n_gram_keyword(arr, n):
    keywords = []
    if len(arr) > 1:
        for i in range(0, len(arr) - n + 1):
            temp = ''
            for j in range (i, i+n):
                temp = temp + " " + arr[j]
            keywords.append(temp.strip())
        return keywords
    else:
        return arr


# In[28]:


import csv

all_keywords = dict()
with open('keyword_keahlian.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        keywords = row['key'].split(", ")
        label = row['value']
        for keyword in keywords:
            if keyword in all_keywords:
                all_keywords[keyword.lower()].append(label)
            else:
                all_keywords[keyword.lower()] = [label]


# In[30]:


mata_kuliah_keahlian = dict()
field = ['id', 'nama_matakuliah', 'keahlian_id']
f = open('output.csv', 'w')

with open('caripakar_app_matakuliah.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    writer = csv.DictWriter(f, fieldnames= field)
    writer.writeheader()
    for row in reader:
        matkul = row['nama_matakuliah'].lower()
        total_keyword = 0 # total keyword in one title
        count_keyword = dict()

        temp_keywords = dict()
        print ("=======" + matkul + "=========")
        matkul_keywords = matkul.split(" ") #list matkul per kata
        
        for gram in range(1, 4):
            gram_keywords = create_n_gram_keyword(matkul_keywords, gram) # bikin arr gram_keywords tdr dr 1-4 kata
            for keyword in gram_keywords:
                if keyword in all_keywords:
                    value_keyword = all_keywords[keyword]
                    temp_keywords[keyword] = value_keyword
                    for value in all_keywords[keyword]:
                        if value in count_keyword:
                            count_keyword[value] += 1
                        else:
                            count_keyword[value] = 1
                else:
                    temp_keywords[keyword] = None
        
        keys = temp_keywords.keys()
        for key in keys:
            if temp_keywords[key] is not None:
                for k in temp_keywords[key]:
                    print(key + ' -> ' + k)
                    total_keyword += 1
        print("total keyword:", total_keyword)
        print(count_keyword) 
        if total_keyword > 0:
            print("klasifikasi keahlian: " + max(count_keyword.keys(), key=lambda k: count_keyword[k]))
            print("ada")
            new_row = {'id': row['id'], 'nama_matakuliah': row['nama_matakuliah'], 'keahlian_id': max(count_keyword.keys(), key=lambda k: count_keyword[k])}
        else:
            new_row = {'id': row['id'], 'nama_matakuliah': row['nama_matakuliah'], 'keahlian_id': 'NULL'}
        writer.writerow(new_row)


# In[20]:


mata_kuliah = [
	"project JARINGAN KOMPUTER",
	"JARINGAN KOMPUTER & PENGAMANANNYA",
	"Jaringan Komputer",
	"PROJECT MANAGEMENT jaringan",
	"Pemrosesan dan Manajemen Data Multimedia",
	"SISTEM OPERASI",
	"SISTEM TERDISTRIBUSI",
	"Sistem & Arsitektur Komputer A",
	"Sistem ArsitekturKomputer A",
	"Sistem Komputer",
	"Sistem Operasi Lanjut",
	"Sistem Paralel dan Terdistribusi proyek project management",
	"TESIS"
]


# In[21]:


mata_kuliah = [matkul.lower() for matkul in mata_kuliah]


# In[22]:


mata_kuliah


# In[30]:


mata_kuliah_keahlian = dict()
for matkul in mata_kuliah:
    total_keyword = 0 # total keyword in one title
    count_keyword = dict()
    
    temp_keywords = dict()
    print ("=======" + matkul + "=========")
    matkul_keywords = matkul.split(" ") #list matkul per kata

    for gram in range(1, 4):
        gram_keywords = create_n_gram_keyword(matkul_keywords, gram) # bikin arr gram_keywords tdr dr 1-4 kata
        for keyword in gram_keywords:
#             if keyword in all_keywords:
#                 value_keyword = all_keywords[keyword]
#                 temp_keywords[keyword]   = value_keyword
#                 if all_keywords[keyword] in count_keyword:
#                     count_keyword[value_keyword] += 1
#                 else:
#                     count_keyword[value_keyword] = 1
#             else:
#                 temp_keywords[keyword] = None
            if keyword in all_keywords:
                value_keyword = all_keywords[keyword]
                temp_keywords[keyword] = value_keyword
                for value in all_keywords[keyword]:
                    if value in count_keyword:
                        count_keyword[value] += 1
                    else:
                        count_keyword[value] = 1
            else:
                temp_keywords[keyword] = None
    
    keys = temp_keywords.keys()
    for key in keys:
        if temp_keywords[key] is not None:
            for k in temp_keywords[key]:
                print(key + ' -> ' + k)
                total_keyword += 1
    print("total keyword:", total_keyword)
    print(count_keyword) 
    if count_keyword:
        print("klasifikasi keahlian: " + max(count_keyword.keys(), key=lambda k: count_keyword[k]))

