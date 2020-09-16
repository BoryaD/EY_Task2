from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .models import File, Bill, GroupBill, ClassType, IncomingBalance, OutcomingBalance, Turnover
from .forms import FileForm
import pandas as pd
# Create your views here.

class Table:
    def __init__(self, print_seven_col, bill, iba, ibp, tod, toc, obp, oba, class_of):
        self.type_of_str = print_seven_col
        self.bill_str = bill
        self.ib_ac = iba
        self.ib_pas = ibp
        self.to_deb = tod
        self.to_cr = toc
        self.ob_ac = obp
        self.ob_pas = oba
        self.class_of = class_of


def main_view(request):
    files = File.objects.all()
    return render(request, 'SecondTask/home.html', {
        'files': files
    })


def view_file(request, pk):
    bills = Bill.objects.filter(file_id=pk)
    group_bills = GroupBill.objects.filter(file_id=pk)
    class_type = ClassType.objects.filter(file_id=pk)
    inc_balance = IncomingBalance.objects.filter(file_id=pk)
    out_balance = OutcomingBalance.objects.filter(file_id=pk)
    turnover = Turnover.objects.filter(file_id=pk)
    table = []
    print_one_col = 0
    print_seven_col = 1
    print_seven_col_bold = 2
    for ct in class_type:
        if ct.description != '-1':
            b = Table(print_one_col, 0, 0, 0, 0, 0, 0, 0, ct.description)
            table.append(b)
            for bill in bills.filter(class_of=ct):
                if bill.num != '-1':
                    for gb in group_bills.filter(parent_num=bill):
                        if gb.num_group != '-1':
                            ib = inc_balance.get(full_bill=gb)
                            to = turnover.get(full_bill=gb)
                            ob = out_balance.get(full_bill=gb)
                            a = Table(print_seven_col, bill.num + gb.num_group, ib.active, ib.passive, to.debet, to.credit,
                                      ob.passive, ob.active, 0)
                            table.append(a)
                        else:
                            ib = inc_balance.get(full_bill=gb)
                            to = turnover.get(full_bill=gb)
                            ob = out_balance.get(full_bill=gb)
                            a = Table(print_seven_col, bill.num, ib.active, ib.passive, to.debet, to.credit,
                                      ob.passive, ob.active, 0)
                            table.append(a)
                else:
                    print(bill.id)
                    gb = GroupBill.objects.get(parent_num=bill)
                    ib = inc_balance.get(full_bill=gb)
                    to = turnover.get(full_bill=gb)
                    ob = out_balance.get(full_bill=gb)
                    a = Table(print_seven_col, "ПО КЛАССУ", ib.active, ib.passive, to.debet, to.credit,
                              ob.passive, ob.active, 0)
                    table.append(a)
        else:
            bill = Bill.objects.get(class_of=ct)
            gb = GroupBill.objects.get(parent_num=bill)
            ib = inc_balance.get(full_bill=gb)
            to = turnover.get(full_bill=gb)
            ob = out_balance.get(full_bill=gb)
            a = Table(print_seven_col, "БАЛАНС", ib.active, ib.passive, to.debet, to.credit,
                      ob.passive, ob.active, 0)
            table.append(a)

    return render(request, 'SecondTask/file_info.html', {
        'filename': get_object_or_404(File, id=pk).title,
        'table': table
    })


def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_object = form.save()
            parse_xls(file_object)
            return redirect('home')
    else:
        form = FileForm()
    return render(request, 'SecondTask/upload_file.html', {
        'form': form
    })


def parse_xls(file):
    df = pd.read_excel(file.file, index_col=None, header=None)
    current_class = 0
    current_bill = 0
    update_bill = 0
    current_group_bill = 0
    for i in range(8, df.index.stop):
        # print(df[0][i], type(df[0][i]))
        if type(df[0][i]) == str:
            if df[0][i][0] == "К":
                current_class = ClassType(description=df[0][i], file=file)
                current_class.save()
            elif df[0][i][0] == "П":
                current_bill = Bill(num='-1', class_of=current_class, file=file)
                current_bill.save()
                current_group_bill = GroupBill(num_group='-1', parent_num=current_bill, file=file)
                current_group_bill.save()
                inc = IncomingBalance(full_bill=current_group_bill, active=df[1][i], passive=df[2][i], file=file)
                inc.save()

                turn = Turnover(full_bill=current_group_bill, debet=df[3][i], credit=df[4][i], file=file)
                turn.save()
                out = OutcomingBalance(full_bill=current_group_bill, active=df[5][i], passive=df[6 ][i], file=file)
                out.save()
                update_bill = 0
            elif df[0][i][0] == "Б":
                current_class = ClassType(description='-1', file=file)
                current_class.save()
                current_bill =Bill(num='-1', file=file, class_of=current_class)
                current_bill.save()
                current_group_bill = GroupBill(num_group='-1', parent_num=current_bill, file=file)
                current_group_bill.save()
                inc = IncomingBalance(full_bill=current_group_bill, active=df[1][i], passive=df[2][i], file=file)
                inc.save()

                turn = Turnover(full_bill=current_group_bill, debet=df[3][i], credit=df[4][i], file=file)
                turn.save()
                out = OutcomingBalance(full_bill=current_group_bill, active=df[5][i], passive=df[6][i], file=file)
                out.save()

            elif len(df[0][i]) == 4:
                if not update_bill:
                    current_bill = Bill(num=df[0][i][:2], file=file, class_of=current_class)
                    current_bill.save()
                    update_bill = 1
                current_group_bill = GroupBill(num_group=df[0][i][2:], parent_num=current_bill, file=file)
                current_group_bill.save()
                inc = IncomingBalance(full_bill=current_group_bill, active=df[1][i], passive=df[2][i], file=file)
                inc.save()

                turn = Turnover(full_bill=current_group_bill, debet=df[3][i], credit=df[4][i], file=file)
                turn.save()
                out = OutcomingBalance(full_bill=current_group_bill, active=df[5][i], passive=df[6][i], file=file)
                out.save()

        else:
            current_group_bill = GroupBill(num_group='-1', parent_num=current_bill, file=file)
            current_group_bill.save()
            inc = IncomingBalance(full_bill=current_group_bill, active=df[1][i], passive=df[2][i], file=file)
            inc.save()

            turn = Turnover(full_bill=current_group_bill, debet=df[3][i], credit=df[4][i], file=file)
            turn.save()
            out = OutcomingBalance(full_bill=current_group_bill, active=df[5][i], passive=df[6][i], file=file)
            out.save()
            update_bill = 0
