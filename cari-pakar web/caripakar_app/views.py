from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import F

from .models import Keahlian, DosenSkor, Dosen
from .utils import get_all_keahlian_by_dosen
import pickle


with open('./caripakar_app/KlasifikasiPakar.sav', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open('./caripakar_app/tvect.sav', 'rb') as tvect_file:
    tvect = pickle.load(tvect_file)


# Create your views here.
def index(request):
    
    if request.method == 'POST':
        query = request.POST['search-data']
        return HttpResponseRedirect(reverse('searchresult') + '?q=' + query)
    else:
        template_name = 'index.html'
        return render(request, template_name, {'nbar': 'home'})

def searchresult(request):
    template_name = 'searchresult.html'
    query = request.GET['q'].lower()
    id_keahlian = request.GET['keahlian'] if 'keahlian' in request.GET else None
    bobot_pendidikan = request.GET['skor-pendidikan'] if 'skor-pendidikan' in request.GET else 50
    bobot_penelitian = request.GET['skor-penelitian'] if 'skor-penelitian' in request.GET else 50
    bobot_pengajaran = request.GET['skor-pengajaran'] if 'skor-pengajaran' in request.GET else 50
    bobot_jabatan = request.GET['skor-jabatan'] if 'skor-jabatan' in request.GET else 50
    bobot_proyek = request.GET['skor-proyek'] if 'skor-proyek' in request.GET else 50
    prediction = loaded_model.predict(tvect.transform([query]))[0]
    try:
        if 'keahlian' in request.GET:
            keahlian = Keahlian.objects.get(pk=id_keahlian)
        else:
            keahlian = Keahlian.objects.get(nama_keahlian=prediction)
        keahlian_list = Keahlian.objects.all()
        dosen_recommendation_list = DosenSkor.objects.filter(keahlian=keahlian).annotate(
            total_skor=(F('z_skor_pendidikan') * bobot_pendidikan + F('z_skor_proyek') * bobot_proyek \
            + F('z_skor_pengajaran') * bobot_pengajaran + F('z_skor_penelitian') \
            * bobot_pendidikan) + F('z_skor_jabatan') * bobot_jabatan).order_by('-total_skor')[:5]
        dosen_recommendation_list = [(dosen_skor.dosen, get_all_keahlian_by_dosen(
            dosen_skor.dosen, \
            bobot_pendidikan, \
            bobot_penelitian, \
            bobot_pengajaran, \
            bobot_proyek, \
            bobot_jabatan)) \
            for dosen_skor in dosen_recommendation_list]
        print(dosen_recommendation_list)
        return render(request, template_name, {
            'nbar': 'home', 
            'keahlian_list': keahlian_list, 
            'keahlian': keahlian, 
            'skor_pengajaran': bobot_pengajaran,
            'skor_penelitian': bobot_penelitian,
            'skor_pendidikan': bobot_pendidikan,
            'skor_jabatan': bobot_jabatan,
            'skor_proyek': bobot_proyek,
            'query_param': query,
            'dosen_recommendation_list': dosen_recommendation_list })
    except Keahlian.DoesNotExist:
        raise Http404


def expertprofile(request, pk):
    template_name = 'expertprofile.html'
    try:
        dosen = Dosen.objects.get(pk=pk)
        return render(request, template_name, {'nbar': 'home', 'dosen': dosen})
    except Dosen.DoesNotExist:
        raise Http404
    

    # TO-DO

def about(request):
    template_name = 'about.html'
    return render(request, template_name, {'nbar': 'about'})

