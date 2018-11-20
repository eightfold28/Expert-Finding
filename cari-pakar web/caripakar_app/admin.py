from django.contrib import admin
from .models import PerguruanTinggi, JabatanFungsional, Dosen, \
    Gelar, Keahlian, MataKuliah, Penelitian, Proyek, DosenGelar, DosenMatakuliah, DosenSkor, \
    ProgramStudi, Jenjang, ProgramStudiKeahlian, GlobalVar, DosenJumlahPengajaran, \
    DosenJumlahPenelitian, DosenJumlahProyek

'''user: admin, password: qwerty123'''
# Register your models here.

class JabatanFungsionalAdmin(admin.ModelAdmin):
    list_display = ('nama_jabatanfungsional', 'rank', 'skor_jabatanfungsional',)
    list_display_links = ('nama_jabatanfungsional',)


class JenjangAdmin(admin.ModelAdmin):
    list_display = ('nama_jenjang', 'rank', 'skor_jenjang',)
    list_display_links = ('nama_jenjang',)

class GlobalVarAdmin(admin.ModelAdmin):
    list_display = ('name', 'value',)
    list_display_links = ('name',)

class DosenAdmin(admin.ModelAdmin):
    list_display = ('nama_dosen', 'perguruantinggi', 'jabatanfungsional', \
        'programstudi', \
        'total_jumlah_pengajaran', 'total_jumlah_penelitian', 'total_jumlah_proyek')
    list_display_links = ('nama_dosen',)

class ProyekAdmin(admin.ModelAdmin):
    list_display = ('judul_proyek', 'dosen', 'keahlian', \
        'pengguna_jasa', \
        'tahun')
    list_display_links = ('judul_proyek',)

class PenelitianAdmin(admin.ModelAdmin):
    list_display = ('judul_penelitian', 'dosen', 'keahlian', \
        'perguruantinggi', \
        'tahun')
    list_display_links = ('judul_penelitian',)

class DosenJumlahPenelitianAdmin(admin.ModelAdmin):
    list_display = ('dosen', 'keahlian', 'jumlah_penelitian')
    list_display_links = ('dosen',)

class DosenJumlahPengajaranAdmin(admin.ModelAdmin):
    list_display = ('dosen', 'keahlian', 'jumlah_pengajaran')
    list_display_links = ('dosen',)

class DosenJumlahProyekAdmin(admin.ModelAdmin):
    list_display = ('dosen', 'keahlian', 'jumlah_proyek')
    list_display_links = ('dosen',)

class DosenSkorAdmin(admin.ModelAdmin):
    list_display = ('dosen', 'keahlian', 'skor_pendidikan', 'skor_jabatan', 'skor_penelitian', 'skor_pengajaran', \
        'z_skor_pendidikan', 'z_skor_jabatan', 'z_skor_penelitian', 'z_skor_pengajaran')
    list_display_links = ('dosen',)


admin.site.register(PerguruanTinggi)
admin.site.register(JabatanFungsional, JabatanFungsionalAdmin)
admin.site.register(Dosen, DosenAdmin)
admin.site.register(Gelar)
admin.site.register(Keahlian)
admin.site.register(MataKuliah)
admin.site.register(Penelitian, PenelitianAdmin)
admin.site.register(Proyek, ProyekAdmin)
admin.site.register(DosenGelar)
admin.site.register(DosenMatakuliah)
admin.site.register(DosenSkor, DosenSkorAdmin)
admin.site.register(ProgramStudi)
admin.site.register(Jenjang, JenjangAdmin)
admin.site.register(ProgramStudiKeahlian)
admin.site.register(GlobalVar, GlobalVarAdmin)
admin.site.register(DosenJumlahPengajaran, DosenJumlahPengajaranAdmin)
admin.site.register(DosenJumlahPenelitian, DosenJumlahPenelitianAdmin)
admin.site.register(DosenJumlahProyek, DosenJumlahProyekAdmin)