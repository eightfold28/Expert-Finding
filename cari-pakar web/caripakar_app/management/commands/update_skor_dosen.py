from django.core.management.base import BaseCommand
from caripakar_app.utils import update_skor, get_all_dosens_by_keahlian
from caripakar_app.models import Dosen, Keahlian, DosenMatakuliah, DosenSkor

class Command(BaseCommand):
    help = (
        "For updating lecturer's score. Related tables should already be migrated."
    )

    def handle(self, **options):
        DosenSkor.objects.all().delete()
       	all_keahlian = Keahlian.objects.all()
       	dosen_keahlian = dict()
       	for keahlian in all_keahlian:
       		all_dosen = get_all_dosens_by_keahlian(keahlian)
       		all_dosen_matakuliah = DosenMatakuliah.objects.filter(matakuliah__keahlian=keahlian).all()
       		for dosen_matakuliah in all_dosen_matakuliah:
       			all_dosen.add(dosen_matakuliah.dosen)
       		dosen_keahlian[keahlian] = all_dosen
       	for keahlian in all_keahlian:
       		for dosen in dosen_keahlian[keahlian]:
       			dosen_skor = update_skor(keahlian, dosen)
