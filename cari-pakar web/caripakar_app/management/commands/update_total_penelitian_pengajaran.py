from django.core.management.base import BaseCommand
from caripakar_app.models import DosenGelar, Jenjang, Dosen, DosenJumlahPengajaran, DosenJumlahPenelitian, DosenJumlahProyek
from caripakar_app.utils import update_total_jumlah_penelitian, update_total_jumlah_pengajaran, update_total_jumlah_proyek

class Command(BaseCommand):
    help = (
        "To update number of research and teachings :)"
    )

    def handle(self, **options):
        all_dosen = Dosen.objects.all()
        DosenJumlahPenelitian.objects.all().delete()
        DosenJumlahPengajaran.objects.all().delete()
        DosenJumlahProyek.objects.all().delete()
        for dosen in all_dosen:
            update_total_jumlah_pengajaran(dosen)
            update_total_jumlah_penelitian(dosen)
            update_total_jumlah_proyek(dosen)