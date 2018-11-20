 # INSERT INTO `caripakar_app_keahlian` (`id`, `nama_keahlian`)
	# 	VALUES
	# 	 (1,'Algoritma dan Pemrograman'),
	# 	 (2,'Dasar Matematika'),
	# 	 (3,'Sistem Komputer'),
	# 	 (4,'Information Management'),
	# 	 (5,'Software Engineering'),
	# 	 (6,'Graphics and Visualization'),
	# 	 (7,'Intelligent System'),
	# 	 (8,'Social and Professional Issue'),
	# 	 (9,'Enterprise Computing'),
	# 	 (10,'Hardware');


import pymysql
import pymysql.cursors
import json

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='',
                            db='caripakarapp',
                            cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        db_json = open('data5univIF.json', 'r').readlines()
        for row in db_json:
            parsed_json = json.loads(row)
            url = parsed_json['url']
            nama_dosen = None
            perguruan_tinggi = None
            jabatan_fungsional = None
            jabatan_fungsional_id = None
            perguruan_tinggi_id = None
            dosen_id = None
            program_studi_id = None
            sql = "select * from caripakar_app_dosen where url = '%s'" % url
            cursor.execute(sql)
            temp = cursor.fetchone()
            insert = temp is None
            if insert:
                if 'program_studi' in parsed_json and parsed_json['program_studi'] is not None:
                    program_studi = parsed_json['program_studi'].title()
                    sql = "select * from caripakar_app_programstudi where nama_programstudi = '%s'" % program_studi
                    cursor.execute(sql)

                    temp = cursor.fetchone()
                    if temp is None:
                        sql =  "insert into caripakar_app_programstudi (`nama_programstudi`, `keahlian_id`) values ('%s', 1)" % program_studi
                        cursor.execute(sql)
                        connection.commit()
                        program_studi_id = int(cursor.lastrowid)
                    else:
                        program_studi_id = int(temp['id'])
                if 'jabatan_fungsional' in parsed_json and parsed_json['jabatan_fungsional'] is not None:
                    jabatan_fungsional = parsed_json['jabatan_fungsional'].title()
                    sql = "select * from caripakar_app_jabatanfungsional where nama_jabatanfungsional = '%s';" % jabatan_fungsional
                    cursor.execute(sql)
                    temp = cursor.fetchone()
                    if temp is None:
                        sql = "insert into caripakar_app_jabatanfungsional (`nama_jabatanfungsional`, `rank`) values ('%s', 0)" % jabatan_fungsional
                        cursor.execute(sql)
                        connection.commit()
                        jabatan_fungsional_id = int(cursor.lastrowid)
                    else:
                        jabatan_fungsional_id = int(temp['id'])
                if 'perguruan_tinggi' in parsed_json and parsed_json['perguruan_tinggi'] is not None:
                    perguruan_tinggi = parsed_json['perguruan_tinggi'].title()
                    sql = "select * from caripakar_app_perguruantinggi where nama_perguruantinggi = '%s';" % perguruan_tinggi
                    cursor.execute(sql)
                    temp = cursor.fetchone()
                    if temp is None:
                        sql = "insert into caripakar_app_perguruantinggi (`nama_perguruantinggi`) values ('%s')" % perguruan_tinggi
                        cursor.execute(sql)
                        perguruan_tinggi_id = int(cursor.lastrowid)
                    else:
                        perguruan_tinggi_id = int(temp['id'])
                if 'nama_dosen' in parsed_json and parsed_json['nama_dosen'] is not None:
                    nama_dosen = parsed_json['nama_dosen'].title()
                    nama_dosen = nama_dosen.replace("'", "\\'")
                    sql = None
                    if perguruan_tinggi_id is None and jabatan_fungsional_id is None:
                        sql = "insert into caripakar_app_dosen (`url`, `nama_dosen`) values('%s', '%s')" % (url, nama_dosen,)
                    elif perguruan_tinggi_id is None:
                        sql = "insert into caripakar_app_dosen (`url`, `nama_dosen`, `jabatanfungsional_id`) values('%s', '%s', '%d')" % \
                            (url, nama_dosen, jabatan_fungsional_id,)
                    elif jabatan_fungsional_id is None:
                        sql = "insert into caripakar_app_dosen (`url`, `nama_dosen`, `perguruantinggi_id`) values('%s', '%s', '%d')" % \
                            (url, nama_dosen, perguruan_tinggi_id,)
                    else:
                        sql = "insert into caripakar_app_dosen (`url`, `nama_dosen`, `perguruantinggi_id`, `jabatanfungsional_id`) values('%s', '%s', '%d', '%d')" % \
                            (url, nama_dosen, perguruan_tinggi_id, jabatan_fungsional_id,)
                    cursor.execute(sql)
                    connection.commit()
                    dosen_id = cursor.lastrowid

                    sql = "update caripakar_app_dosen set programstudi_id = '%s' where id = '%s'" % (program_studi_id, dosen_id,)
                    cursor.execute(sql)
                    connection.commit()
                if 'riwayat_pendidikan' in parsed_json:
                    riwayat_pendidikans = parsed_json['riwayat_pendidikan']
                    for riwayat_pendidikan in riwayat_pendidikans:
                        attrs = "(`dosen_id`"
                        valss = "('%s'" % dosen_id
                        gelar_akademik = None
                        jenjang = None
                        tahun_ijazah = None
                    
                        if 'gelar_akademik' in riwayat_pendidikan:
                            gelar_akademik = riwayat_pendidikan['gelar_akademik']

                        if 'jenjang' in riwayat_pendidikan:
                            jenjang = riwayat_pendidikan['jenjang']

                        gelar_id = None
                        if gelar_akademik is not None:
                            sql = "select * from caripakar_app_gelar where nama_gelar = '%s'" % gelar_akademik
                            if jenjang is not None:
                                sql1 = "select * from caripakar_app_jenjang where nama_jenjang = '%s'" % jenjang
                                cursor.execute(sql1)
                                temp = cursor.fetchone()
                                print(temp)
                                if temp is None:
                                    sql1 = "insert into caripakar_app_jenjang (`nama_jenjang`) values ('%s')" % jenjang
                                    cursor.execute(sql1)
                                    connection.commit()
                                    jenjang = cursor.lastrowid
                                else:
                                    jenjang = temp['id']
                                sql = sql + " and jenjang_id = '%s'" % jenjang
                            sql = sql + ";"

                            cursor.execute(sql)
                            temp = cursor.fetchone()

                            if temp is not None:
                                gelar_id = temp['id']
                            else:
                                attr = "(`nama_gelar`"
                                vals = "('%s'" % gelar_akademik
                                if jenjang is not None:
                                    attr = attr + ", `jenjang_id`"
                                    vals = vals + ", '%s'" % jenjang
                                attr = attr + ")"
                                vals = vals + ")"

                                sql = "insert into caripakar_app_gelar %s values %s" % (attr, vals,)
                                print(sql)
                                cursor.execute(sql)
                                gelar_id = cursor.lastrowid
                            attrs = attrs + ", `gelar_id`"
                            valss = valss + ", '%d'" % int(gelar_id) 

                        perguruan_tinggi_riwayat = None
                        if 'perguruan_tinggi' in riwayat_pendidikan:
                            perguruan_tinggi_riwayat = riwayat_pendidikan['perguruan_tinggi'].title()

                        perguruan_tinggi_riwayat_id = None
                        if perguruan_tinggi_riwayat is not None:
                            sql = "select * from caripakar_app_perguruantinggi where nama_perguruantinggi = '%s'" \
                                % perguruan_tinggi_riwayat
                            cursor.execute(sql)
                            temp = cursor.fetchone()

                            if temp is not None:
                                perguruan_tinggi_riwayat_id = temp['id']
                            else:
                                sql = "insert into caripakar_app_perguruantinggi (`nama_perguruantinggi`) values ('%s')" % \
                                    perguruan_tinggi_riwayat
                                cursor.execute(sql)
                                connection.commit()
                                perguruan_tinggi_riwayat_id = cursor.lastrowid
                            attrs = attrs + ", `perguruantinggi_id`"
                            valss = valss + ", '%d'" % int(perguruan_tinggi_riwayat_id)

                        if 'tanggal_ijazah' in riwayat_pendidikan and riwayat_pendidikan['tanggal_ijazah'] != '':
                            tahun_ijazah = int(riwayat_pendidikan['tanggal_ijazah'])
                            attrs = attrs + ", `tahun_ijazah`"
                            valss = valss + ", '%d'" % tahun_ijazah

                        attrs = attrs + ")"
                        valss = valss + ");"
                        sql = "insert into caripakar_app_dosengelar %s values %s" % (attrs, valss)
                        connection.commit()
                        cursor.execute(sql)
                if 'riwayat_mengajar' in parsed_json:
                    riwayat_mengajars = parsed_json['riwayat_mengajar']
                    for riwayat_mengajar in riwayat_mengajars:
                        attrs = "(`dosen_id`"
                        valss = "(%d" % dosen_id
                        mata_kuliah = None
                        if 'nama_mata_kuliah' in riwayat_mengajar:
                            mata_kuliah = riwayat_mengajar['nama_mata_kuliah'].title()
                        update = False
                        mata_kuliah_id = None
                        if mata_kuliah is not None:
                            mata_kuliah = mata_kuliah.replace('\'', "\\'")
                            sql = "select * from caripakar_app_matakuliah where nama_matakuliah = '%s'" % mata_kuliah
                            cursor.execute(sql)
                            temp = cursor.fetchone()
                            if temp is not None:
                                mata_kuliah_id = temp['id']
                                sql = "select * from caripakar_app_dosenmatakuliah where dosen_id = %d and matakuliah_id = %d" % \
                                    (dosen_id, mata_kuliah_id)
                                cursor.execute(sql)
                                temp = cursor.fetchone()
                                if temp is not None:
                                    update = True
                                    sql = "update caripakar_app_dosenmatakuliah set jumlah_pengajaran = %d where dosen_id = %d and matakuliah_id = %d" %\
                                        (temp['jumlah_pengajaran'] +1, dosen_id, mata_kuliah_id)
                                    cursor.execute(sql)
                                    connection.commit()
                            else:
                                sql = "insert into caripakar_app_matakuliah (`nama_matakuliah`) values ('%s')" % mata_kuliah
                                cursor.execute(sql)
                                connection.commit()
                                mata_kuliah_id = cursor.lastrowid
                            attrs = attrs + ", `matakuliah_id`"
                            valss = valss + ", %d" % mata_kuliah_id
                            attrs = attrs + ", `jumlah_pengajaran`"
                            valss = valss + ", %d" % 1
                        perguruan_tinggi_mengajar_id = None
                        perguruan_tinggi_mengajar = None
                        if 'perguruan_tinggi' in riwayat_mengajar:
                            perguruan_tinggi_mengajar = riwayat_mengajar['perguruan_tinggi'].title()

                        if perguruan_tinggi_mengajar is not None:
                            perguruan_tinggi_mengajar = perguruan_tinggi_mengajar.replace("\'", "\\'")
                            sql = "select * from caripakar_app_perguruantinggi where nama_perguruantinggi = '%s'" % perguruan_tinggi_mengajar
                            cursor.execute(sql)
                            temp = cursor.fetchone()
                            if temp is not None:
                                perguruan_tinggi_mengajar_id = temp['id']
                            else:
                                sql = "insert into caripakar_app_perguruantinggi (`nama_perguruantinggi`) values ('%s')" % perguruan_tinggi_mengajar
                                cursor.execute(sql)
                                connection.commit()
                                perguruan_tinggi_mengajar_id = cursor.lastrowid
                            attrs = attrs + ", `perguruantinggi_id`"
                            valss = valss + ", %d" % perguruan_tinggi_mengajar_id
                        
                        attrs = attrs + ")"
                        valss = valss + ")"
                        sql = "insert into caripakar_app_dosenmatakuliah %s values %s" % (attrs, valss,)
                        if not update:
                            cursor.execute(sql)
                            connection.commit()
                if 'penelitian' in parsed_json:
                    penelitian = parsed_json['penelitian']
                    for p in penelitian:
                        perguruan_tinggi_penelitian = None
                        perguruan_tinggi_penelitian_id = None
                        attrs = "(`dosen_id`"
                        valss = "(%d" % dosen_id
                        if 'judul_penelitian' in p:
                            judul_penelitian = p['judul_penelitian'].title()
                            judul_penelitian= judul_penelitian.replace('\'', "\\'")
                            attrs = attrs + ", `judul_penelitian`"
                            valss = valss + ", '%s'" % judul_penelitian
                        if 'tahun' in p:
                            tahun = int(p['tahun'])
                            attrs = attrs + ", `tahun`"
                            valss = valss + ", %d" % tahun
                        k = False
                        if judul_penelitian is not None and tahun is not None:
                            sql = "select * from caripakar_app_penelitian where judul_penelitian = '%s' and tahun = %d" % (judul_penelitian, tahun,)
                            cursor.execute(sql)
                            temp = cursor.fetchone()
                            if temp is None:
                                k = True
                        if k and 'lembaga' in p:
                            perguruan_tinggi_penelitian = p['lembaga'].title()
                            sql = "select * from caripakar_app_perguruantinggi where nama_perguruantinggi = '%s'" % \
                                perguruan_tinggi_penelitian
                            cursor.execute(sql)
                            temp = cursor.fetchone()
                            if temp is not None:
                                perguruan_tinggi_penelitian_id = temp['id']
                            else:
                                sql = "insert into caripakar_app_perguruantinggi (`nama_perguruantinggi`) values ('%s')" % \
                                    perguruan_tinggi_penelitian
                                cursor.execute(sql)
                                connection.commit()
                                perguruan_tinggi_penelitian_id = cursor.lastrowid
                            attrs = attrs + ", `perguruantinggi_id`"
                            valss = valss + ", %d" % perguruan_tinggi_penelitian_id
                        judul_penelitian = None
                        tahun = None
                        attrs = attrs + ")"
                        valss = valss + ")"
                        if k:
                            sql = "insert into caripakar_app_penelitian %s values %s;" % (attrs, valss,)
                            cursor.execute(sql)
                            connection.commit()
                print(dosen_id)
# except:
#   connection.rollback()
finally:
    connection.close()  
