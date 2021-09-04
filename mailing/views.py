import smtplib
from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from validate_email import validate_email
from email import encoders
import pandas as pd
# from email.mime.image import MIMEImage
from django.conf import settings
import os
import time

# Create your views here.
error="No Error"
matter=""
val=""
mail=""
pswd=""
csv_file_name=""
i=0
colnam=""
subject=""
end=0
def home(request):
    return render(request,'mailing/home.html')
def starting(request):
    global matter,val,pswd,mail,csv_file_name,colnam,direct,i,subject,end,error
    val=request.POST['pdfs']
    mail=request.POST['mail']
    pswd=request.POST['pass']
    matter=request.POST['mailtext']
    directry=settings.MEDIA_ROOT
    files=os.listdir(directry)
    filtered_files=[file for file in files if file.endswith(".csv")]
    for file in filtered_files:
	    path_to_file = os.path.join(directry, file)
	    os.remove(path_to_file)
    filtered_files_pdf=[file for file in files if file.endswith(".pdf")]
    for file in filtered_files_pdf:
	    path_to_file_pdf = os.path.join(directry, file)
	    os.remove(path_to_file_pdf)
    i=int(request.POST['counting'])
    subject=request.POST['subject']
    end=int(request.POST['ending'])
    print(pswd,mail)
    if(request.method=="POST"):
        csv_file=request.FILES['csv']
        csv_file_name=csv_file.name
        fs=FileSystemStorage()
        fs.save(csv_file.name,csv_file)
    data=pd.read_csv(settings.MEDIA_ROOT / csv_file_name,encoding="cp1252")
    if(val=='0'):
        return render(request,'mailing/pdf0.html',{'Columns':data.columns})
    elif(val=='1'):
        return render(request,'mailing/pdf1.html',{'Columns':data.columns})
    else:
        return render(request,'mailing/pdf2.html',{'Columns':data.columns})
def startingmails(request):
        global csv_file_name,colnam,val,subject,end,i,error
        colnam=request.POST['col-nam']
        startindex=i
        data=pd.read_csv(settings.MEDIA_ROOT / csv_file_name,encoding="cp1252")
        render(request,'mailing/startingmails.html')
        print(data.columns)
        limit=i
        try:
            if(request.method=="POST"):
                print("ENTERING POST REQUEST")
                if(val=='0'):
                        fromaddr = mail
                        body = matter
                        count=i
                        s = smtplib.SMTP('smtp.gmail.com', 587,timeout=600)
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                        s.login(mail, pswd)
                        while(count<=i+490 and (i!=data.shape[0]) and count<=end):
                                msg = MIMEMultipart('alternative')
                                msg.attach(MIMEText(body, 'plain'))
                                msg['From'] = mail
                                msg['Subject'] = subject
                                var = data[f"{colnam}"][i]
                                i=i+1
                                msg['To'] = var
                                text = msg.as_string()
                                is_valid = validate_email(var)
                                if(is_valid):
                                    s.sendmail(fromaddr, var, text)
                                    count=count+1
                                    print(var,count)
                                if(limit+60==i):
                                    time.sleep(10)
                                    limit+=60
                                if(count==startindex+150):
                                    break
                        s.quit()
                elif(val=="1"):
                        uploaded_file=request.FILES['pdf1']
                        fs=FileSystemStorage()
                        fs.save(uploaded_file.name,uploaded_file)
                        print(uploaded_file.name,csv_file_name)
                        fromaddr = mail
                        body = matter
                        count=i
                        s = smtplib.SMTP('smtp.gmail.com', 587,timeout=600)
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                        s.login(mail, pswd)
                        while(count<=i+490 and (i!=data.shape[0]) and count<=end):
                                msg = MIMEMultipart()
                                msg.attach(MIMEText(body, 'plain'))
                                filename = uploaded_file.name
                                attachment = open(settings.MEDIA_ROOT / filename, "rb")
                                p = MIMEBase('application', 'octet-stream',Name=filename)
                                p.set_payload((attachment).read())
                                encoders.encode_base64(p)
                                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                                msg.attach(p)
                                msg['From'] = mail
                                msg['Subject'] = subject
                                var = data[f"{colnam}"][i]
                                i=i+1
                                msg['To'] = var
                                text = msg.as_string()
                                is_valid = validate_email(var)
                                if(is_valid):
                                    s.sendmail(fromaddr, var, text)
                                    count=count+1
                                    print(var,count)
                                if(limit+60==i):
                                    time.sleep(10)
                                    limit+=60
                                if(count==startindex+150):
                                    break
                        s.quit()
                        attachment.close()
                        os.remove( settings.MEDIA_ROOT / filename)
                        os.remove(settings.MEDIA_ROOT / csv_file_name)

                else:
                        uploaded_file1=request.FILES['pdf2']
                        uploaded_file2=request.FILES['pdf3']
                        fs1=FileSystemStorage()
                        fs1.save(uploaded_file1.name,uploaded_file1)
                        fs1.save(uploaded_file2.name,uploaded_file2)
                        print(uploaded_file1.name)
                        print(uploaded_file2.name)
                        fromaddr = mail
                        body = matter
                        count=i
                        s = smtplib.SMTP('smtp.gmail.com', 587,timeout=600)
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                        s.login(mail,pswd)
                        while(count<=i+490 and (i!=data.shape[0]) and count <=end):
                                msg = MIMEMultipart()
                                msg.attach(MIMEText(body, 'plain'))
                                filename = uploaded_file1.name
                                # print("../media" / filename)
                                attachment = open(settings.MEDIA_ROOT / filename, "rb")
                                p = MIMEBase('application', 'octet-stream',Name=filename)
                                p.set_payload((attachment).read())
                                encoders.encode_base64(p)
                                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                                msg.attach(p)
                                filename1 = uploaded_file2.name
                                attachment1 = open(settings.MEDIA_ROOT / filename1, "rb")
                                q = MIMEBase('application', 'octet-stream',Name=filename1)
                                q.set_payload((attachment1).read())
                                encoders.encode_base64(q)
                                q.add_header('Content-Disposition', "attachment; filename= %s" % filename1)
                                msg.attach(q)
                                msg['From'] = fromaddr
                                msg['Subject'] = subject
                                var = data[f"{colnam}"][i]
                                i=i+1
                                msg['To'] = var
                                text = msg.as_string()
                                is_valid = validate_email(var)
                                if(is_valid):
                                    s.sendmail(fromaddr, var, text)
                                    count=count+1
                                    print(var,count)
                                if(limit+60==i):
                                    time.sleep(10)
                                    limit+=60
                                if(count==startindex+150):
                                    break
                        s.quit()
                        attachment.close()
                        attachment1.close()
                        os.remove( settings.MEDIA_ROOT / filename)
                        os.remove(settings.MEDIA_ROOT / filename1)
                        os.remove(settings.MEDIA_ROOT / csv_file_name)
        except Exception as e:
            attachment.close()
            attachment1.close()
            os.remove( settings.MEDIA_ROOT / filename)
            os.remove(settings.MEDIA_ROOT / filename1)
            os.remove(settings.MEDIA_ROOT / csv_file_name)
            error=str(e.__class__)
            print(error)

        return render(request,'mailing/startingmails.html',{'index':i,'error':error})