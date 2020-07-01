import json
import datetime

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm
from .models import Book
from mysite import settings



class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def parse_data(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        base = settings.MEDIA_ROOT
        final_result = {}
        if book.pdf or book.pdf is not "" or book.pdf is not None:
            data = [json.loads(line) for line in open(str(base)+str("/")+str(book.pdf), 'r')]

            for i in range(0, len(data)):
                final_result[str(data[i]['timestamp'])] = {}
                Mppt_Output_DC_Voltage = [value for key, value in data[i].items() if 'Output_DC_Voltage' in key]
                if Mppt_Output_DC_Voltage is not None and Mppt_Output_DC_Voltage is not "":
                    average_Mppt_Output_DC_Voltage = round(sum(Mppt_Output_DC_Voltage)/len(Mppt_Output_DC_Voltage), 2)
                else:
                    average_Mppt_Output_DC_Voltage = 0

                final_result[str(data[i]['timestamp'])]["average_Mppt_Output_DC_Voltage"] = average_Mppt_Output_DC_Voltage

                Xw_Fault_Bitmap = []
                final_Xw_Fault_Bitmap = {}

                for key, value in data[i].items():
                    if 'Fault_Bitmap' in key:
                        if 'Xw' in key:
                            Xw_Fault_Bitmap.append(key)

                sorted(Xw_Fault_Bitmap)

                max_Xw_Fault_Bitmap_no = int(Xw_Fault_Bitmap[-1][2])
                min_Xw_Fault_Bitmap_no = int(Xw_Fault_Bitmap[0][2])

                temp = []

                for i in range(0, len(Xw_Fault_Bitmap)):
                    if int(Xw_Fault_Bitmap[i][-1]) not in temp:
                        temp.append(int(Xw_Fault_Bitmap[i][-1]))

                max_end = max(temp)
                min_end = min(temp)

                temp_dict = {}
                for i in range(min_Xw_Fault_Bitmap_no, max_Xw_Fault_Bitmap_no+1):
                    temp_dict[i] = {}
                    for j in range(min_end, max_end+1):
                        if "Xw"+str(i)+"_Fault_Bitmap_"+str(j) in Xw_Fault_Bitmap:
                            temp_dict[i][j] = data[i]["Xw"+str(i)+"_Fault_Bitmap_"+str(j)]

                for key, val in temp_dict.items():
                    keymax = max(temp_dict[key], key=temp_dict[key].get)
                    final_Xw_Fault_Bitmap["Xw"+str(key)+"_Fault_Bitmap_"+str(keymax)] = data[i]["Xw" + str(key) +
                                                                                                "_Fault_Bitmap_"
                                                                                                + str(keymax)]
                if str(data[i]['timestamp']) in final_result.keys():
                    final_result[str(data[i]['timestamp'])]["final_Xw_Fault_Bitmap"] = final_Xw_Fault_Bitmap
            result = final_result
            for i in range(0, len(data)-1):
                date_time_str1 = data[i+1]['timestamp']
                date_time_str2 = data[i]['timestamp']
                date_time_str1 = datetime.datetime.strptime(date_time_str1, '%Y-%m-%d %H:%M:%S')
                date_time_str2 = datetime.datetime.strptime(date_time_str2, '%Y-%m-%d %H:%M:%S')
                diff = date_time_str1 - date_time_str2
                date_time_str = "00:05:00"
                date_time_obj = datetime.datetime.strptime(date_time_str, '%H:%M:%S')
                date_time_diff = datetime.datetime.strptime(str(diff), '%H:%M:%S')
                # print(date_time_obj)
                if date_time_diff > date_time_obj:
                    # print(data[i]['timestamp'])
                    if str(data[i]['timestamp']) in result.keys():
                        minutes = diff.seconds/60
                        result[str(data[i]['timestamp'])]["Data_missing"] = minutes

        print(final_result)

    return redirect('book_list')


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'


def showdata(request):
    if request.method == 'POST':
        data = Book.objects.all()
        print(data)
    else:
        data = ""
    return render(request, 'show_data.html', {
        'data': data
    })


def data_list(request):
    books = Book.objects.all()
    return render(request, 'show_data.html', {
        'books': books
    })


def upload_data(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('data_list')
    else:
        form = BookForm()
    return render(request, 'upload_data.html', {
        'form': form
    })
