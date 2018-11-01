# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from . import models
from django.core.mail import send_mail
import datetime
from library import settings

from django.shortcuts import render

# Create your views here.
def homepage(request):
    user = request.POST.get("username", None)
    pwd = request.POST.get("password", None)
    identity = request.POST.get("identity", None)
    post = models.default.objects.values('post').first().values()[0]
    if request.POST.has_key('librarian_recover'):
        try:
            lib = models.librarian.objects.get(id=user)
            if lib:
                lib[0].isrequest = 1
            return render(request, "homepage.html", {'ans':'Already sent the message to the admin.', 'post':post})
        except:
            return render(request, "homepage.html", {'ans': 'not exist id.', 'post':post})
    elif request.POST.has_key('login'):
        if identity == 'librarian':
            try:
                get_id = models.librarian.objects.get(id=user)
                try:
                    compare_user = models.librarian.objects.get(id=user, pwd=pwd)
                    if compare_user:
                        request.session['user'] = user
                        request.session['pwd'] = pwd
                        return HttpResponseRedirect('/librarian_home/')
                    else:
                        return render(request, "homepage.html", {'post':post})
                except:
                    return render(request, "homepage.html", {'ans': 'password wrong.', 'post':post})
            except:
                return render(request, "homepage.html", {'ans': 'not exist id.', 'post':post})

        else:
            try:
                get_id = models.reader.objects.get(id=user)
                try:
                    compare_user = models.reader.objects.get(id=user, pwd=pwd)
                    if compare_user:
                        request.session['user'] = user
                        request.session['pwd'] = pwd
                        return HttpResponseRedirect('/reader_home/')
                    else:
                        return render(request, "homepage.html", {'post':post})
                except:
                    return render(request, "homepage.html", {'and': 'password wrong.', 'post':post})
            except:
                return render(request, "homepage.html", {'ans': 'not exist id.', 'post':post})
    elif request.POST.has_key('signup'):
        reader_id = request.POST.get('reader_id', None)
        try:
            reader_email = request.POST.get('email', None)
            models.reader.objects.get(id=reader_id, email=reader_email)
            send_mail('New password of Bibliosoft', 'Your new password is 12345678.', settings.EMAIL_FROM,
                      [reader_email])
            reader = models.reader.objects.filter(id=reader_id)[0]
            reader.pwd = '12345678'
            reader.save()
            return render(request, "homepage.html")
        except:
            return render(request, "homepage.html", {'new_ans': 'Your id or email is wrong.'})
    else:
        return render(request, "homepage.html", {'post':post})

def admin_login(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        try:
            get_id = models.admin.objects.get(id=user)
            try:
                compare_user = models.admin.objects.get(id=user, pwd=pwd)
                if compare_user:
                    request.session['user'] = user
                    request.session['pwd'] = pwd
                    return HttpResponseRedirect('/admin_home/')
                else:
                    return render(request, "login.html")
            except:
                return render(request, "login.html", {'ans': 'password wrong.'})
        except:
            return render(request, "login.html", {'ans': 'not exist id.'})
    else:
        return render(request, "login.html")

def reader_home(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        return render(request, "reader_home.html",{'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_search(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            if request.POST.has_key('reserve'):
                book_id = request.POST.get('book id', None)
                book_name = models.book.objects.filter(id=book_id)[0].name
                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")
                models.appointment.objects.create(reader_id=request.session['user'], book_id=book_id,
                                                  book_name=book_name, time=time)
                return render(request, "reader_search.html", {'login': request.session['user']})
            book_name = request.POST.get('search', None)
            try:
                searchlist = models.book.objects.filter(name=book_name)
                return render(request, "reader_search.html", {'searchresult': searchlist,'login':request.session['user']})
            except:
                return render(request, "reader_search.html",{'login':request.session['user']})
        else:
            return render(request, "reader_search.html",{'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_lending(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        lend = models.lend.objects.filter(reader_id=request.session['user'])
        today_date = datetime.datetime.now()
        default_period = models.default.objects.values('return_period').first()

        if len(lend) == 0:
            return render(request, "reader_home.html",{'ans':'no lending books.','login':request.session['user']})
        for record in lend:
            lend_date = record.date
            Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
            record.remain_lendingtime = int(default_period.values()[0]) - (today_date - Lend_date).days
            record.save()
        return render(request, "reader_lending books.html", {'reader_lendingbooks':lend,'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_returnhistory(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        lend = models.lend.objects.filter(reader_id=request.session['user'])

        if len(lend) == 0:
            return render(request, "reader_home.html",{'ans':'no lending history.','login':request.session['user']})
        return render(request, "reader_return history.html", {'reader_returnhistory': lend,'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_lookupfine(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        fine = models.fine.objects.filter(reader_id=request.session['user'])
        today_date = datetime.datetime.now()
        default_fine = float(models.default.objects.values('fine').first().values()[0])
        default_period = int(models.default.objects.values('return_period').first().values()[0])

        if len(fine) == 0:
            return render(request, "reader_home.html",{'ans':'no fine history.','login':request.session['user']})

        for record in fine:
            if record.ispayed == '0':
                lend_date = record.date
                Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
                lenddays = (today_date - Lend_date).days
                if lenddays > default_period:
                    record.topay_fine = ( lenddays - default_period ) * default_fine
                    record.save()
        return render(request, "reader_to-pay fine.html", {'reader_finelist': fine,'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_reserve(request):
    try:
        models.reader.objects.get(id=request.session['user'],
                                     pwd=request.session['pwd'])
        try:
            appointment = models.appointment.objects.filter(reader_id=request.session['user'])
            now = datetime.datetime.now()
            for record in appointment:
                time = record.time
                appointment_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                if (now - appointment_time).seconds > 7200:
                    models.appointment.objects.filter(book_id=record.book_id, reader_id=request.session['user']).delete()
            appointment = models.appointment.objects.filter(reader_id=request.session['user'])
            if len(appointment) == 0:
                return render(request, "reader_reserve.html", {'ans': 'no appointment history.','login':request.session['user']})
            return render(request, "reader_reserve.html", {'reader_reserve': appointment,'login':request.session['user']})
        except:
            return HttpResponseRedirect('/reader_home/',{'login':request.session['user']})

    except:
        return HttpResponseRedirect('/homepage/')


def reader_changeinfo(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            pwd = request.POST.get('password', None)
            email = request.POST.get('email', None)
            reader = models.reader.objects.filter(id = request.session['user'])[0]
            reader.pwd = pwd
            reader.email = email
            reader.save()
            return HttpResponseRedirect('/reader_home/',{'login':request.session['user']})
        else:
            return render(request, "reader_changeinfo.html",{'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def admin_home(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        return render(request, "admin_home.html")
    except:
        return HttpResponseRedirect('/homepage/')


def admin_addlibrarian(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            id = request.POST.get('username', None)
            models.librarian.objects.create(id=id)
            return HttpResponseRedirect('/admin_home/')
        else:
            return render(request, "admin_addlibrarian.html")
    except:
        return render(request, "homepage.html")

def admin_manage(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            id = request.POST.get('librarian id', None)
            models.librarian.objects.filter(id=id).delete()
        librarian_list = models.librarian.objects.all()
        return render(request, "admin_manage.html", {'librarian_list': librarian_list})
    except:
        return render(request, "homepage.html")

def admin_defaultvalue(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        fine = models.default.objects.values('fine').first().values()[0]
        period = models.default.objects.values('return_period').first().values()[0]
        deposit = models.default.objects.values('deposit').first().values()[0]
        if request.method == 'POST':
            fine = request.POST.get('fine', None)
            return_period = request.POST.get('return_period', None)
            deposit = request.POST.get('deposit', None)
            line = models.default.objects.all()[0]
            line.fine = fine
            line.return_period = return_period
            line.deposit = deposit
            line.save()
            return HttpResponseRedirect('/admin_home/')
        return render(request, "admin_defaultvalue.html",{'fine':fine, 'period':period, 'deposit':deposit})
    except:
        return render(request, "homepage.html")

def admin_request(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        #librarian = models.librarian.objects.all()
        if request.method == 'POST':
            id = request.POST.get('librarian id', None)
            lib = models.librarian.objects.filter(id=id)[0]
            lib.pwd = '00010001'
            lib.isrequest = '0'
            lib.save()
        librarian = models.librarian.objects.all()
        return render(request, "admin_request.html", {'request_list':librarian})
    except:
        return render(request, "homepage.html")


def librarian_home(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        return render(request, "librarian_home.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_managebook(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            if request.POST.has_key('delete'):
                book_id = request.POST.get('book id', None)
                book_name = request.POST.get('book name', None)
                models.book.objects.filter(id=book_id)[0].delete()
                models.delete.objects.create(book_id=book_id, book_name=book_name, librarian_id=request.session['user'])
            else:
                book_name = request.POST.get('search', None)
            try:
                searchlist = models.book.objects.filter(name=book_name)
                if len(searchlist) == 0:
                    return render(request, "librarian_managebook.html", {'ans': 'no such book.'})
                return render(request, "librarian_managebook.html", {'searchresult': searchlist})
            except:
                return render(request, "librarian_managebook.html")
        else:
            return render(request, "librarian_managebook.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_addcategory(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            category = request.POST.get('category', None)
            models.category.objects.create(name=category)
        categories = models.category.objects.all()
        return render(request, "librarian_addcategory.html",{'categories':categories})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_changepwd(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            old_pwd = request.POST.get('old password', None)
            if old_pwd == request.session['pwd']:
                new_pwd = request.POST.get('new password', None)
                lib = models.librarian.objects.filter(id=request.session['user'],
                                                   pwd=request.session['pwd'])[0]
                lib.pwd = new_pwd
                lib.save()
                return render(request, "librarian_changepwd.html", {'ans':'Change password successfully.'})
            else:
                return render(request, "librarian_changepwd.html", {'ans':'old password wrong.'})
        return render(request, "librarian_changepwd.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_addreader(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            id = request.POST.get('username', None)
            email = request.POST.get('email', None)
            sex = request.POST.get('sex', None)
            deposit = models.default.objects.values('deposit').first().values()[0]
            models.reader.objects.create(id=id, sex=sex, email=email, deposit=deposit)

            today_date = datetime.datetime.now().strftime("%Y-%m-%d")

            income_search = models.income.objects.filter(date=today_date)

            if len(income_search) == 0:
                models.income.objects.create(date=today_date, deposit=deposit, fine=0, sum=deposit)
            else:
                income = income_search[0]
                income.deposit = float(income.deposit) + float(deposit)
                income.sum = float(income.sum) + float(deposit)
                income.save()

            return HttpResponseRedirect('/librarian_home/')
        else:
            return render(request, "librarian_addreader.html")
    except:
        return render(request, "homepage.html")


def librarian_managereader(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            if request.POST.has_key('delete'):
                reader_id = request.POST.get('reader id', None)

                lend = models.lend.objects.filter(reader_id=reader_id)
                if len(lend) != 0:
                    for line in lend:
                        if line.isreturned == '0':
                            return render(request, "librarian_managereader.html",
                                          {'ans': 'the reader cannot be deleted because of the not-returned book.'})

                fine = models.fine.objects.filter(reader_id=reader_id)
                today_date = datetime.datetime.now()
                default_fine = float(models.default.objects.values('fine').first().values()[0])
                default_period = int(models.default.objects.values('return_period').first().values()[0])

                if len(fine) == 0:
                    models.reader.objects.filter(id=reader_id)[0].delete()
                    return render(request, "librarian_managereader.html", {'ans': 'no reader of this id.'})

                for record in fine:
                    if record.ispayed == '0':
                        lend_date = record.date
                        Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
                        lenddays = (today_date - Lend_date).days
                        if lenddays > default_period:
                            record.topay_fine = (lenddays - default_period) * default_fine
                            record.save()
                for record in fine:
                    if float(record.topay_fine) > 0:
                        return render(request, "librarian_managereader.html", {'ans': 'the reader cannot be deleted because of the to-pay fine.'})
                models.reader.objects.filter(id=reader_id)[0].delete()
                return render(request, "librarian_managereader.html", {'ans': 'no reader of this id.'})
            else:
                reader_id = request.POST.get('search', None)
            readers = models.reader.objects.filter(id=reader_id)
            if len(readers) == 0:
                return render(request, "librarian_managereader.html", {'ans': 'no reader of this id.'})
            else:
                return render(request, "librarian_managereader.html", {'searchresult': readers})
        else:
            return render(request, "librarian_managereader.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_checkincome(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        income = models.income.objects.all()
        today_date = datetime.datetime.now()
        daily = 0.0
        weekly = 0.0
        monthly = 0.0
        for record in income:
            date = record.date.split(' ')[0]
            income_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            days = (today_date - income_date).days
            if days == 0:
                daily = daily + float(record.sum)
            if days >= 0 & days <7:
                weekly = weekly + float(record.sum)
            if days >= 0 & days <30:
                monthly = monthly + float(record.sum)

        return render(request, "librarian_checkincome.html",
        {'income_daily':daily, 'income_weekly':weekly, 'income_monthly':monthly})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_post(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            word = request.POST.get('post', None)
            line = models.default.objects.all()[0]
            line.post = word
            line.save()
        post = models.default.objects.values('post').first().values()[0]
        return render(request, "librarian_post.html",{'post':post})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_lend(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            book_id = request.POST.get('book_id', None)
            reader_id = request.POST.get('reader_id', None)
            book = models.book.objects.filter(id=book_id)[0]
            book.islent = '1'
            book.save()
            default_period = models.default.objects.values('return_period').first().values()[0]
            models.lend.objects.create(book_id=book_id, book_name=book.name, reader_id=reader_id,
                                       remain_lendingtime=default_period, isreturned='0', date=datetime.datetime.now().strftime("%Y-%m-%d"))
            models.fine.objects.create(book_name=book.name, reader_id=reader_id, date=datetime.datetime.now().strftime("%Y-%m-%d"))
            return render(request, "librarian_lend.html", {'ans': 'lend the book << ' + book.name + ' >> successfully'})
        return render(request, "librarian_lend.html")
    except:
        return HttpResponseRedirect('/homepage/')


def librarian_return(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            book_id = request.POST.get('book_id', None)
            book_name = models.book.objects.filter(id=book_id)[0].name
            lend_record = models.lend.objects.filter(book_id=book_id, isreturned='0')[0]
            lend_record.isreturned = '1'
            lend_record.save()
            list_id = lend_record.list_id
            fine_record = models.fine.objects.filter(list_id=list_id)[0]
            fine_record.ispayed = '1'

            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
            default_fine = float(models.default.objects.values('fine').first().values()[0])
            default_period = int(models.default.objects.values('return_period').first().values()[0])

            lend_date = fine_record.date
            Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
            lenddays = (datetime.datetime.now() - Lend_date).days
            if lenddays > default_period:
                fine_record.topay_fine = (lenddays - default_period) * default_fine
            fine_record.save()

            income_search = models.income.objects.filter(date=today_date)
            if len(income_search) == 0:
                models.income.objects.create(date=today_date, deposit=0, fine=default_fine, sum=default_fine)
            else:
                income = income_search[0]
                income.fine = float(income.fine) + float(fine_record.topay_fine)
                income.sum = float(income.deposit) + float(fine_record.topay_fine)
                income.save()

            return render(request, "librarian_return.html",{'ans': 'return the book << ' + book_name + ' >> successfully'})
        else:
            return render(request, "librarian_return.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_addbook(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        categories = models.category.objects.all()
        if request.method == 'POST':
            book_name = request.POST.get('bookname', None)
            floor = request.POST.get('floor', None)
            shelf = request.POST.get('shelf', None)
            area = request.POST.get('area', None)
            price = request.POST.get('price', None)
            category = request.POST.get('category', None)
            ISBN = request.POST.get('ISBN', None)
            models.book.objects.create(name=book_name, floor=floor, shelf=shelf, area=area,
                                       price=price, category=category, ISBN=ISBN)
            return render(request, "librarian_addbook.html",{'ans':'add book << '+book_name+' >> successfully.',
                                                             'categories':categories})
        else:
            return render(request, "librarian_addbook.html", {'categories':categories})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_deletelist(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        deletelist = models.delete.objects.all()
        if len(deletelist) == 0:
            return render(request, "librarian_deletelist.html", {'ans':'no delete history.'})
        else:
            return render(request, "librarian_deletelist.html", {'deletelist':deletelist})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_editbook(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        categories = models.category.objects.all()
        if request.method == 'POST':
            if request.POST.has_key('submit'):
                id = request.POST.get('book id', None)
                book = models.book.objects.filter(id=id)[0]
                book.name = request.POST.get('name', None)
                book.floor = request.POST.get('floor', None)
                book.shelf = request.POST.get('shelf', None)
                book.area = request.POST.get('area', None)
                book.price = request.POST.get('price', None)
                book.category = request.POST.get('category', None)
                book.ISBN = request.POST.get('ISBN', None)
                book.save()

            elif request.POST.has_key('edit'):
                book_id = request.POST.get('book id', None)
                book = models.book.objects.filter(id=book_id)[0]
            return render(request, "librarian_editbook.html", {'book': book, 'categories':categories})
        else:
            return render(request, "librarian_editbook.html", {'categories':categories})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_checkfine(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            reader_id = request.POST.get('reader id', None)
            finelist = models.fine.objects.filter(reader_id=reader_id)
            if len(finelist) == 0:
                return render(request, "librarian_checkfine.html", {'ans':'no fine history.'})
            return render(request, "librarian_checkfine.html", {'finelist':finelist})
        return render(request, "librarian_checkfine.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_checklend(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            reader_id = request.POST.get('reader id', None)
            lendlist = models.lend.objects.filter(reader_id=reader_id)
            if len(lendlist)==0:
                return render(request, "librarian_checklend.html",{'ans':'no lend history.'})
            return render(request, "librarian_checklend.html", {'lendlist':lendlist})
        return render(request, "librarian_checklend.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_checkreturn(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            reader_id = request.POST.get('reader id', None)
            lendlist = models.lend.objects.filter(reader_id=reader_id)
            returnlist = []
            if len(lendlist) == 0:
                render(request, "librarian_checkreturn.html", {'ans':'no return history.'})
            for line in lendlist:
                if line.isreturned == '1':
                    returnlist.append(line)
            if len(returnlist) == 0:
                return render(request, "librarian_checkreturn.html", {'ans': 'no return history.'})
            else:
                return render(request, "librarian_checkreturn.html", {'returnlist':returnlist})
        return render(request, "librarian_checklend.html")
    except:
        return HttpResponseRedirect('/homepage/')
