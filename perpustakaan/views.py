from django.shortcuts import render, redirect, HttpResponse
from perpustakaan.models import Buku
# fungsi agar menampilkan form otomatis
from perpustakaan.forms import FormBuku
# fungsi menampilkan tampilan pesan
from django.contrib import messages
# fungsi untuk login
from django.contrib.auth.decorators import login_required
from django.conf import settings
# form sign up
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from perpustakaan.resource import BukuResource

def export_xls(request):
    buku = BukuResource()
    dataset = buku.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="laporan excel.xls"'
    return response


@login_required(login_url=settings.LOGIN_URL)
def signup(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "user berhasil dibuat")
            return redirect('signup')
        else:
            messages.error(request, "terjadi kesalahan")
            return redirect('signup')
    else:
        form = UserCreationForm()
        isi = {
            'form': form,
        }
    return render(request, 'signup.html', isi)


@login_required(login_url=settings.LOGIN_URL)
def hapus_buku(request, id_buku):
    buku = Buku.objects.get(id = id_buku)
    buku.delete()

    messages.success(request, "Data Berhasil dihapus")
    return redirect('buku')


@login_required(login_url=settings.LOGIN_URL)
def ubah_buku(request, id_buku):
    buku = Buku.objects.get(id = id_buku)
    template = 'ubah-buku.html'
    
    if request.POST:
        form = FormBuku(request.POST, request.FILES, instance=buku)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil di Ubah!")
            return redirect('ubah_buku', id_buku=id_buku)
    else:
        form = FormBuku(instance=buku)
        isi = {
            'form': form,
            'buku': buku,
        }

        return render(request, 'ubah-buku.html', isi)


@login_required(login_url=settings.LOGIN_URL)
def buku(request):
    books = Buku.objects.all()
    #books = Buku.objects.all()[:5]
    #books = Buku.objects.filter(kelompok_id__nama='Umum')

    isi = {
        'books': books,
    }

    return render(request, 'buku.html', isi)


@login_required(login_url=settings.LOGIN_URL)
def penerbit(request):
    return render(request, 'penerbit.html')
    

@login_required(login_url=settings.LOGIN_URL)
def tambah_buku(request):
    if request.POST:
        # jika ada data yg diterima dr form, maka simpan
        # req.files saat submit data file maka akan ditempatkan di sini juga
        form = FormBuku(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormBuku()
            pesan = "Data berhasil disimpan"

            isi = {
                'form' : form,
                'pesan' : pesan,
            }
            return render(request, 'tambah-buku.html', isi)
            
    else :
        form = FormBuku()

        isi = {
        'form': form,
        }

    return render(request, 'tambah-buku.html', isi)