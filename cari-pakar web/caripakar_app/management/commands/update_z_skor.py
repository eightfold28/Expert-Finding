from django.core.management.base import BaseCommand
from caripakar_app.utils import update_skor, get_all_dosens_by_keahlian
from caripakar_app.models import Dosen, Keahlian, DosenMatakuliah, DosenSkor
import numpy as np
from scipy.stats import zscore 
class Command(BaseCommand):
    help = (
        "To update lecturers' score in z_score type."
    )

    def handle(self, **options):
        all_dosen_skor = DosenSkor.objects.all()
        all_dosen_skor_pendidikan = np.array([dosenskor.skor_pendidikan for dosenskor in all_dosen_skor])
        all_dosen_z_skor_pendidikan = zscore(all_dosen_skor_pendidikan)

       	all_dosen_skor_pengajaran = np.array([dosenskor.skor_pengajaran for dosenskor in all_dosen_skor])
        all_dosen_z_skor_pengajaran = zscore(all_dosen_skor_pengajaran)

        all_dosen_skor_jabatan = np.array([dosenskor.skor_jabatan for dosenskor in all_dosen_skor])
        all_dosen_z_skor_jabatan = zscore(all_dosen_skor_jabatan)

        all_dosen_skor_penelitian = np.array([dosenskor.skor_penelitian for dosenskor in all_dosen_skor])
        all_dosen_z_skor_penelitian = zscore(all_dosen_skor_penelitian)

        all_dosen_skor_proyek = np.array([dosenskor.skor_proyek for dosenskor in all_dosen_skor])
        all_dosen_z_skor_proyek = zscore(all_dosen_skor_proyek)

        for index, dosenskor in enumerate(all_dosen_skor):
            dosenskor.z_skor_pendidikan = all_dosen_z_skor_pendidikan[index]
            dosenskor.z_skor_penelitian = all_dosen_z_skor_penelitian[index]
            dosenskor.z_skor_jabatan = all_dosen_z_skor_jabatan[index]
            dosenskor.z_skor_pengajaran = all_dosen_z_skor_pengajaran[index]
            dosenskor.z_skor_proyek = all_dosen_z_skor_proyek[index]
            dosenskor.save()
            print(dosenskor)