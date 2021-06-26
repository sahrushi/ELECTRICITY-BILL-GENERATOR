import io
from django.shortcuts import render,redirect
from home.models import BillDetail
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, FileResponse
from django.views.generic import View
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Create your views here.
global stud
def home(request):
    if request.method == "POST":
        CID = request.POST['CID']
        user = auth.authenticate(CID=CID)
        if user is not None:
            auth.index(request,user)
            stud=BillDetail.objects.filter(CID=request.CID)
            return redirect(request,"details",{'stu':stud})
        else:
            return redirect('home')
    else:
        return render(request,'home.html')

def details(request):
    global stud
    x=int(request.POST['CID'])
    stud=BillDetail.objects.get(CID=x)
    Name=request.POST.get('Name')
    CID=request.POST.get('CID')
    Units=request.POST.get('Units')
    Amount=request.POST.get('Amount')
    BillGenerated=request.POST.get('BillGenerated')

    context = {}
    context["Name"] = Name
    context["CID"] = CID
    context["Units"] = Units
    context["Amount"] = Amount
    context["BillGenerated"] = BillGenerated
    return render(request,'details.html',{'stu':stud})

def pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    
    details = BillDetail.objects.all()
    lines = []

    for detail in details:
        lines.append(detail.Name)
        lines.append(detail.CID)
        lines.append(detail.Units)
        lines.append(detail.Amount)
        lines.append(detail.BillGenerated)
    
    for line in lines:
        textob.textLine(line)
     
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='bill.pdf')