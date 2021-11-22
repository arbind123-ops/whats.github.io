from django.contrib import admin
from .models import *


admin.site.register([
    OrgnizationalInformation, Admin, Editor, NewsCategory, NewsSubCategory,
    News, Comment, Advertizement,Subscriber,

])
