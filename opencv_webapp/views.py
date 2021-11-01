from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face
# Create your views here.

def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})

def simple_upload(request):

    if request.method == 'POST':
        print(request.POST) # dict
        print(request.FILES) # dict
        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():

            myfile = request.FILES['image'] # 유저가 업로드한 파일

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
                #이렇게 써야함 왜냐면 중복으로 동일한 사진이 들어왔을 때 원본으로 보여주기 위해서
                #지우고 싶을 때는 delete
                #DB를 사용하지 않을 때 활용하는 것

            context = {'form':form, 'uploaded_file_url':uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html', context)

    else: # 'GET' request
        form = SimpleUploadForm()
        return render(request, 'opencv_webapp/simple_upload.html', {'form':form})


def detect_face(request):
    if request.method == 'POST' :
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = ImageUploadForm(request.POST, request.FILES) # filled form
        if form.is_valid():
             # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경하거나 추가로 다른 데이터를 추가할 수 있음
            post = form.save(commit=False)
            post.save() # DB에 실제로 Form 객체('form')에 채워져 있는 데이터를 저장
	           # post는 save() 후 DB에 저장된 ImageUploadModel 클래스 객체 자체를 갖고 있게 됨 (record 1건에 해당)

            imageURL = settings.MEDIA_URL + form.instance.document.name
	        # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            # print(form.instance, form.instance.document.name, form.instance.document.url)
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정

            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context )

    else:
         form = ImageUploadForm() # empty form

         context = {'form':form}
         return render(request, 'opencv_webapp/detect_face.html', context)
