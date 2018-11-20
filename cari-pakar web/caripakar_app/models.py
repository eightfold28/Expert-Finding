# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import *
from django.core.validators import MinValueValidator, MaxValueValidator

class PerguruanTinggi(models.Model):
    nama_perguruantinggi = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.nama_perguruantinggi


class JabatanFungsional(models.Model):
    nama_jabatanfungsional = models.CharField(max_length=100, blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    skor_jabatanfungsional = models.DecimalField(max_digits=12, decimal_places=4, default= Decimal('0.0000'), \
        validators=[MinValueValidator(0), MaxValueValidator(1)])


    def __str__(self):
        return self.nama_jabatanfungsional + ' dengan rank ' + str(self.rank)

    def save(self, *args, **kwargs):
        current_id = self.id
        count_jabfung = JabatanFungsional.objects.count()
        if current_id is None:
            if count_jabfung == 0:
                super(JabatanFungsional, self).save(*args, **kwargs)
            else:
                jabfung_prev = JabatanFungsional.objects.get(rank=count_jabfung)
                if self.skor_jabatanfungsional <= jabfung_prev.skor_jabatanfungsional:
                    raise ValidationError(
                        _('%(value)s skor_jabatanfungsional not valid'),
                        params={'value': self.skor_jabatanfungsional},
                    )
                else:
                    super(JabatanFungsional, self).save(*args, **kwargs)
        else:
            current_rank = self.rank
            try:
                prev_jabfung = JabatanFungsional.objects.get(rank=current_rank-1)
            except JabatanFungsional.DoesNotExist:
                prev_jabfung = None
            try:
                next_jabfung = JabatanFungsional.objects.get(rank=current_rank+1)
            except JabatanFungsional.DoesNotExist:
                next_jabfung = None 
            
            if next_jabfung is None and prev_jabfung is None:
                super(JabatanFungsional, self).save(*args, **kwargs)
            elif next_jabfung is None:
                if prev_jabfung.skor_jabatanfungsional > self.skor_jabatanfungsional:
                    super(JabatanFungsional, self).save(*args, **kwargs)
                else:
                    raise ValidationError(
                        _('%(value)s skor_jabatanfungsional not valid'),
                        params={'value': self.skor_jabatanfungsional},
                    )
            elif prev_jabfung is None:
                if next_jabfung.skor_jabatanfungsional < self.skor_jabatanfungsional:
                    super(JabatanFungsional, self).save(*args, **kwargs)
                else:
                    raise ValidationError(
                        _('%(value)s skor_jabatanfungsional not valid'),
                        params={'value': self.skor_jabatanfungsional},
                    )
            else:
                if prev_jabfung.skor_jabatanfungsional > self.skor_jabatanfungsional and self.skor_jabatanfungsional > next_jabfung.skor_jabatanfungsional:
                    super(JabatanFungsional, self).save(*args, **kwargs)
                else:
                    raise ValidationError(
                        _('%(value)s skor_jabatanfungsional not valid'),
                        params={'value': self.skor_jabatanfungsional},
                    )


    class Meta:
        ordering = ('rank', )

class Keahlian(models.Model):
    nama_keahlian = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama_keahlian


class ProgramStudi(models.Model):
    nama_programstudi = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama_programstudi


class ProgramStudiKeahlian(models.Model):
    programstudi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE, blank=True, null= True)
    keahlian = models.ForeignKey(Keahlian, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.programstudi.nama_programstudi + ' dengan keahlian ' + self.keahlian.nama_keahlian
        

class Dosen(models.Model):
    perguruantinggi = models.ForeignKey(PerguruanTinggi, on_delete=models.CASCADE, blank=True, null=True)
    jabatanfungsional = models.ForeignKey(JabatanFungsional, on_delete=models.CASCADE, blank=True, null=True)
    nama_dosen = models.CharField(max_length=80, blank=True, null=True)
    programstudi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE, blank=True, null= True)
    url = models.CharField(max_length=255, blank=True, null=True)
    total_jumlah_pengajaran = models.IntegerField(default=0)
    total_jumlah_penelitian = models.IntegerField(default=0)
    total_jumlah_proyek = models.IntegerField(default=0)

    def __str__(self):
        return self.nama_dosen + ' di ' + self.perguruantinggi.nama_perguruantinggi

class DosenJumlahPengajaran(models.Model):
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    keahlian = models.ForeignKey(Keahlian, on_delete=models.CASCADE)
    jumlah_pengajaran = models.IntegerField(default=0)

class DosenJumlahPenelitian(models.Model):
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    keahlian = models.ForeignKey(Keahlian, on_delete=models.CASCADE)
    jumlah_penelitian = models.IntegerField(default=0)

class DosenJumlahProyek(models.Model):
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    keahlian = models.ForeignKey(Keahlian, on_delete=models.CASCADE)
    jumlah_proyek = models.IntegerField(default=0)

class Jenjang(models.Model):
    nama_jenjang = models.CharField(max_length=255)
    rank = models.IntegerField(unique=True, default=0, null=True)
    skor_jenjang = models.DecimalField(max_digits=12, decimal_places=4, default= Decimal('0.0000'), \
        validators=[MinValueValidator(0), MaxValueValidator(1)])    

    def __str__(self):
        return self.nama_jenjang + ' rank ' + str(self.rank)

    def save(self, *args, **kwargs):
        current_id = self.id
        count_jenjang = Jenjang.objects.count()
        if current_id is None:
            if count_jenjang == 0:
                super(Jenjang, self).save(*args, **kwargs)
            else:
                jenjang_prev = Jenjang.objects.get(rank=count_jenjang)
                if self.skor_jenjang <= jenjang_prev.skor_jenjang:
                    raise ValidationError(
                        _('%(value)s skor_jenjang not valid'),
                        params={'value': self.skor_jenjang},
                    )
                else:
                    super(Jenjang, self).save(*args, **kwargs)
        else:
            current_rank = self.rank
            try:
                prev_jenjang = Jenjang.objects.get(rank=current_rank-1)
            except Jenjang.DoesNotExist:
                prev_jenjang = None
            try:
                next_jenjang = Jenjang.objects.get(rank=current_rank+1)
            except Jenjang.DoesNotExist:
                next_jenjang = None
            
            if next_jenjang is None and prev_jenjang is None:
                super(Jenjang, self).save(*args, **kwargs)
            elif next_jenjang is None:
                if prev_jenjang.skor_jenjang > self.skor_jenjang:
                    super(Jenjang, self).save(*args, **kwargs)
                else:
                    raise ValidationError(
                        _('%(value)s skor_jenjang not valid'),
                        params={'value': self.skor_jenjang},
                    )
            elif prev_jenjang is None:
                if next_jenjang.skor_jenjang < self.skor_jenjang:
                    super(Jenjang, self).save(*args, **kwargs)
                else:
                    raise ValidationError(
                        _('%(value)s skor_jenjang not valid'),
                        params={'value': self.skor_jenjang},
                    )
            else:
                if prev_jenjang.skor_jenjang > self.skor_jenjang and self.skor_jenjang > next_jenjang.skor_jenjang:
                    super(Jenjang, self).save(*args, **kwargs)
                else:
                    raise ValidationError(
                        _('%(value)s skor_jenjang not valid'),
                        params={'value': self.skor_jenjang},
                    )

    class Meta:
        ordering = ('rank', )

class Gelar(models.Model):
    nama_gelar = models.CharField(max_length=80, blank=True, null=True)
    jenjang = models.ForeignKey(Jenjang, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama_gelar


class MataKuliah(models.Model):
    keahlian = models.ForeignKey(Keahlian, on_delete=models.SET_NULL, blank=True, null=True)
    nama_matakuliah = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama_matakuliah


class Penelitian(models.Model):
    keahlian = models.ForeignKey(Keahlian, on_delete=models.SET_NULL, blank=True, null=True)
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, blank=True, null=True)
    perguruantinggi = models.ForeignKey(PerguruanTinggi, on_delete=models.SET_NULL, blank=True, null=True)
    judul_penelitian = models.CharField(max_length=200, blank=True, null=True)
    tahun = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.judul_penelitian

class Proyek(models.Model):
    keahlian = models.ForeignKey(Keahlian, on_delete=models.SET_NULL, blank=True, null=True)
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, blank=True, null=True)
    judul_proyek = models.CharField(max_length=200, blank=True, null=True)
    tahun = models.IntegerField(blank=True, null=True)
    pengguna_jasa = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.judul_proyek


class DosenGelar(models.Model):
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, blank=True, null=True)
    gelar = models.ForeignKey(Gelar, on_delete=models.CASCADE, blank=True, null=True)
    perguruantinggi = models.ForeignKey(PerguruanTinggi, on_delete=models.CASCADE, blank=True, null=True)
    tahun_ijazah = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.dosen.nama_dosen + ' bergelar ' + self.gelar.nama_gelar


class DosenMatakuliah(models.Model):
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, blank=True, null=True)
    matakuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, blank=True, null=True)
    perguruantinggi = models.ForeignKey(PerguruanTinggi, on_delete=models.CASCADE, blank=True, null=True)
    jumlah_pengajaran = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.dosen.nama_dosen + ' mengajar ' + self.matakuliah.nama_matakuliah + ' sebanyak ' + str(self.jumlah_pengajaran) + ' kali'


class DosenSkor(models.Model):
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, blank=True, null=True)
    keahlian = models.ForeignKey(Keahlian, on_delete=models.CASCADE, blank=True, null=True)
    skor_pendidikan = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    skor_pengajaran = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    skor_penelitian = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    skor_jabatan = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    skor_proyek = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    z_skor_pendidikan = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    z_skor_pengajaran = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    z_skor_penelitian = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    z_skor_jabatan = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)
    z_skor_proyek = models.DecimalField(default=0.0, decimal_places=4, max_digits=12)


    def get_total_skor(self, bobot_pendidikan, bobot_pengajaran, bobot_penelitian, bobot_proyek):
        return bobot_pendidikan * self.skor_pendidikan + bobot_penelitian * self.skor_penelitian + \
        bobot_pengajaran * self.skor_pengajaran + bobot_proyek * self.skor_proyek

    def __str__(self):
        return self.keahlian.nama_keahlian + ' ' + self.dosen.nama_dosen + ' memiliki skor_pendidikan = ' + str(self.skor_pendidikan) \
            + ', skor_penelitian = ' + str(self.skor_penelitian) + ', skor_proyek = ' + str(self.skor_proyek) \
             + ', dan skor_pengajaran = ' + str(self.skor_pengajaran)


class GlobalVar(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " : " + self.value