from caripakar_app.models import Dosen, Penelitian, Proyek, DosenSkor, DosenGelar, \
	DosenMatakuliah, Penelitian, GlobalVar, Keahlian, \
	DosenJumlahPengajaran, DosenJumlahPenelitian, DosenJumlahProyek
from decimal import Decimal
from django.db.models import Max, Count, F


def get_all_dosens_by_keahlian(keahlian):
	penelitians = Penelitian.objects.filter(keahlian=keahlian).all()
	proyeks = Proyek.objects.filter(keahlian=keahlian).all()
	dosens = set()
	for penilitian in penelitians:
		dosens.add(penilitian.dosen)
	for proyek in proyeks:
		dosens.add(proyek.dosen)
	return dosens

def get_all_keahlian_by_dosen(dosen, bobot_pendidikan, bobot_penelitian, bobot_pengajaran, bobot_jabatan, bobot_proyek):
	# all_keahlian = set()
	# dosen_matakuliahs = DosenMatakuliah.objects.filter(dosen=dosen).all()
	# for dosen_matakuliah in dosen_matakuliahs:
	# 	all_keahlian.add(dosen_matakuliah.matakuliah.keahlian)
	# penelitians = Penelitian.objects.filter(dosen=dosen).all()
	# for penilitian in penelitians:
	# 	all_keahlian.add(penilitian.keahlian)
	# if bobot_pendidikan is None or bobot_penelitian is None or bobot_pengajaran is None or bobot_jabatan is None:
	# 	return all_keahlian
	# else:
	dosen_skors = DosenSkor.objects.filter(dosen=dosen).annotate(
            total_skor=(F('z_skor_pendidikan') * bobot_pendidikan + F('z_skor_proyek') * bobot_proyek \
            + F('z_skor_pengajaran') * bobot_pengajaran + F('z_skor_penelitian') \
            * bobot_pendidikan) + F('z_skor_jabatan') * bobot_jabatan).order_by('-total_skor').all()
	all_keahlian = [(dosen_skor.keahlian, dosen_skor.total_skor) for dosen_skor in dosen_skors]
	return all_keahlian

def update_total_jumlah_pengajaran(dosen):
	keahlians = Keahlian.objects.all()
	total_jumlah_pengajaran = 0
	for keahlian in keahlians:
		dosen_matakuliahs = DosenMatakuliah.objects.filter(dosen=dosen, matakuliah__keahlian=keahlian).all()
		total_jumlah_pengajaran_keahlian = 0
		for dosen_matakuliah in dosen_matakuliahs:
			total_jumlah_pengajaran_keahlian += dosen_matakuliah.jumlah_pengajaran
		total_jumlah_pengajaran += total_jumlah_pengajaran_keahlian
		instance = DosenJumlahPengajaran(dosen=dosen, keahlian=keahlian, jumlah_pengajaran=total_jumlah_pengajaran_keahlian)
		instance.save()
	dosen.total_jumlah_pengajaran = total_jumlah_pengajaran
	dosen.save()

def update_total_jumlah_penelitian(dosen):
	keahlians = Keahlian.objects.all()
	total_jumlah_penelitian = 0
	for keahlian in keahlians:
		total_jumlah_penelitian_keahlian = Penelitian.objects.filter(dosen=dosen, keahlian=keahlian).count()
		total_jumlah_penelitian += total_jumlah_penelitian_keahlian
		instance = DosenJumlahPenelitian(dosen=dosen, keahlian=keahlian, jumlah_penelitian=total_jumlah_penelitian_keahlian)
		instance.save()
	dosen.total_jumlah_penelitian = total_jumlah_penelitian
	dosen.save()

def update_total_jumlah_proyek(dosen):
	keahlians = Keahlian.objects.all()
	total_jumlah_proyek = 0
	for keahlian in keahlians:
		total_jumlah_proyek_keahlian = Proyek.objects.filter(dosen=dosen, keahlian=keahlian).count()
		total_jumlah_proyek += total_jumlah_proyek_keahlian
		instance = DosenJumlahProyek(dosen=dosen, keahlian=keahlian, jumlah_proyek=total_jumlah_proyek_keahlian)
		instance.save()
	dosen.total_jumlah_proyek = total_jumlah_proyek
	dosen.save()



def update_skor(keahlian, dosen):
	skor_pendidikan = 0
	dosen_pendidikans = DosenGelar.objects.filter(dosen=dosen).order_by('-gelar__jenjang__skor_jenjang').all()
	ratio_skor_pendidikan = Decimal(GlobalVar.objects.get(name='SKOR_JENJANG_RATIO').value)
	print("ratio_skor_pendidikan", ratio_skor_pendidikan)
	for index, dosen_pendidikan in enumerate(dosen_pendidikans):
		print(dosen_pendidikan.gelar.jenjang.skor_jenjang)
		skor_pendidikan += (dosen_pendidikan.gelar.jenjang.skor_jenjang * (ratio_skor_pendidikan ** index))
	skor_jabatan = dosen.jabatanfungsional.skor_jabatanfungsional if dosen.jabatanfungsional is not None else 0
	max_count_penelitian = DosenJumlahPenelitian.objects.filter(keahlian=keahlian) \
		.aggregate(max_penelitian_keahlian=Max('jumlah_penelitian'))['max_penelitian_keahlian']
	max_count_proyek = DosenJumlahProyek.objects.filter(keahlian=keahlian) \
		.aggregate(max_proyek_keahlian=Max('jumlah_proyek'))['max_proyek_keahlian']
	max_count_pengajaran = DosenJumlahPengajaran.objects.filter(keahlian=keahlian) \
		.aggregate(max_pengajaran_keahlian=Max('jumlah_pengajaran'))['max_pengajaran_keahlian']
	skor_pengajaran = DosenJumlahPengajaran.objects.get(keahlian=keahlian, dosen=dosen).jumlah_pengajaran
	skor_pengajaran = skor_pengajaran / float(max_count_pengajaran)
	skor_penelitian = DosenJumlahPenelitian.objects.get(keahlian=keahlian, dosen=dosen).jumlah_penelitian
	skor_penelitian = skor_penelitian / float(max_count_penelitian)
	skor_proyek = DosenJumlahProyek.objects.get(keahlian=keahlian, dosen=dosen).jumlah_proyek
	skor_proyek = skor_proyek / float(max_count_proyek)
	instance = DosenSkor(dosen=dosen, keahlian=keahlian, skor_penelitian=skor_penelitian, \
		skor_pengajaran=skor_pengajaran, skor_pendidikan=skor_pendidikan, \
		skor_jabatan=skor_jabatan, skor_proyek=skor_proyek)
	instance.save()
	print((skor_pendidikan, skor_penelitian, skor_jabatan, skor_pengajaran, skor_proyek))
	return instance