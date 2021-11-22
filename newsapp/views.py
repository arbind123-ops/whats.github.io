from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.views.generic.edit import *
from newsapp.forms import *
from .models import *
from datetime import timedelta, date, datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from .mixin import SuperUserMixin
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib. auth import authenticate, login, logout
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .forms import *
from django.utils import timezone


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

class EditorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="Editor").exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)


class EditorHomeView(EditorRequiredMixin, TemplateView):
    template_name = 'admintemplates/editorhome.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(timezone.now().date(), '_____________'),
        view = 0
        for news in News.objects.all():
            view += news.view_count
        context['totalview'] = view
        # context['totaleditors'] = Editor.objects.all()
        context['totalnew'] = News.objects.all()
        context['editornames'] = Editor.objects.all()
        context['adminnames'] = Admin.objects.all()
        org = OrgnizationalInformation.objects.first()
        print(org.created_at.date(), ')))))))))))))))))')
        start_date = org.created_at
        start_date = date(start_date.year, start_date.month, start_date.day)
        end_date = timezone.now().date()
        end_date = date(end_date.year, end_date.month, end_date.day+1)
        for single_date in daterange(start_date, end_date):
            print(single_date)
        return context



class EditorNewsList(EditorRequiredMixin,ListView):
    template_name = 'admintemplates/editornewslist.html'
    model = Editor
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.username
        context['editor'] = Editor.objects.get(user__username=user)

        # context['newslist'] = News.objects.filter(editor.user.username=self.request.user.username)


        return context

    # def get_queryset(self):
    #     news = News.verified.all()
    #     title = self.request.GET.get('title')
    #     if title:
    #         news = news.filter(title=title)
    #     return news

class EditorNewsDetailView(DetailView):
    template_name = "admintemplates/editornewsdetail.html"
    model = News
    context_object_name = 'newsdetail'


class EditorNewsCreate(EditorRequiredMixin, CreateView):
    template_name = 'admintemplates/editornewsadd.html'
    model = News
    form_class = EditorNewsForm
    success_url = reverse_lazy('newsapp:newslist')

    def form_valid(self, form):
        user = self.request.user.editor.id
        print(user)
        editor = Editor.objects.get(id=user)
        print(editor)
        form.instance.editor = editor
        return super().form_valid(form)


def load_subcategories(request):
    category_id = request.GET.get('main_category')
    print(category_id)
    sub_category = NewsSubCategory.objects.filter(
        main_category_id=category_id).order_by('title')
    print(sub_category)
    return render(request, 'admintemplates/subcategory_dropdown_list_options.html', {'sub_category': sub_category})


class EditorNewsUpdate(EditorRequiredMixin, UpdateView):
    template_name = 'admintemplates/editornewsupdate.html'
    model = News
    form_class = EditorNewsForm
    success_url = reverse_lazy('newsapp:newslist')


class EditorNewsDelete(EditorRequiredMixin, DeleteView):
    template_name = 'admintemplates/editornewsdelete.html'
    model = News
    success_url = reverse_lazy('newsapp:newslist')


class EditorRegistrationView(CreateView):
    template_name = "admintemplates/editorregistration.html"
    form_class = EditorForm
    success_url = reverse_lazy('newsapp:login')

    def form_valid(self, form):
        u_name = form.cleaned_data["username"]
        p_word = form.cleaned_data["password"]
        user = User.objects.create_user(u_name, "", p_word)
        form.instance.user = user
        return super().form_valid(form)


class AdminRegistrationView(CreateView):
    template_name = "admintemplates/adminregistration.html"
    form_class = AdminForm
    success_url = reverse_lazy('newsapp:login')

    def form_valid(self, form):
        u_name = form.cleaned_data["username"]
        p_word = form.cleaned_data["password"]
        user = User.objects.create_user(u_name, "", p_word)
        form.instance.user = user
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "admintemplates/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('newsapp:editor')

    def form_valid(self, form):
        u_name = form.cleaned_data["username"]
        p_word = form.cleaned_data["password"]
        user = authenticate(username=u_name, password=p_word)
        self.thisuser = user

        if user is not None and user.groups.exists():
            login(self.request, user)

        else:
            return render(self.request, self.template_name,
                          {"error": "username or password didn't match", "form": form})

        return super().form_valid(form)

    def get_success_url(self):
        if self.thisuser.groups.filter(name="Editor").exists():
            return reverse("newsapp:editorhome")
        elif self.thisuser.groups.filter(name="Admin").exists():
            return reverse("newsapp:adminhome")

        else:
            return reverse("newsapp:login")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/login/")

class PasswordChangeView(FormView):
    template_name = "admintemplates/passwordchange.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy('newsapp:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        logged_in_user = self.request.user
        user = authenticate(username=logged_in_user.username,
                            password=old_password)
        if user is not None:
            password = form.cleaned_data['password']
            logged_in_user.set_password(password)
            logged_in_user.save()
        else:
            return render(self.request, "admintemplates/passwordchange.html", {
                'error': 'Old password did not match. please try again later',
                'form': form
            })
        return super().form_valid(form)

class EditorPasswordChangeView(FormView):
    template_name = "admintemplates/editorpasswordchange.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy('newsapp:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        logged_in_user = self.request.user
        user = authenticate(username=logged_in_user.username,
                            password=old_password)
        if user is not None:
            password = form.cleaned_data['password']
            logged_in_user.set_password(password)
            logged_in_user.save()
        else:
            return render(self.request, "admintemplates/editorpasswordchange.html", {
                'error': 'Old password did not match. please try again later',
                'form': form
            })
        return super().form_valid(form)


class EditUserProfileView(UpdateView):
    template_name = "admintemplates/user_profile.html"
    model = Admin
    # fields = ['user','full_name','email','contact_no','address','image','about']
    form_class = AdminUpdateForm
    success_url = reverse_lazy('newsapp:adminhome')

class EditUsersProfileView(UpdateView):
    template_name = "admintemplates/editor_user_profile.html"
    model = Editor
    # fields = ['user','full_name','email','contact_no','address','image','about']
    form_class = EditorUpdateForm
    success_url = reverse_lazy('newsapp:editorhome')

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="Admin").exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)

class AdminView(AdminRequiredMixin, TemplateView):
    template_name = 'admintemplates/adminhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(timezone.now().date(), '_____________'),
        view = 0
        for news in News.objects.all():
            view += news.view_count
        context['totalviews'] = view
        # context['totaleditors'] = Editor.objects.all()
        context['totalnews'] = News.objects.all()
        context['editorname'] = Editor.objects.all()
        org = OrgnizationalInformation.objects.first()
        print(org.created_at.date(), ')))))))))))))))))')
        start_date = org.created_at
        start_date = date(start_date.year, start_date.month, start_date.day)
        end_date = timezone.now().date()
        end_date = date(end_date.year, end_date.month, end_date.day+1)
        for single_date in daterange(start_date, end_date):
            print(single_date)
        return context

class AdminDetailView(AdminRequiredMixin, DetailView):
    template_name = 'admintemplates/adminnews.html'
    model = Admin
    context_object_name = 'newslist'


class AdminAdvertizementPositionList(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminadvertizementpositionlist.html'
    model = AdvertizementPosition
    context_object_name = 'advertizementpositionlist'


class AdminAdvertizementPositionCreate(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "admintemplates/adminadvertizementpositionadd.html"

    model = AdvertizementPosition
    form_class = AdminAdvertizementPosition
    success_url = reverse_lazy('newsapp:advertizementposition')
    success_message = 'Created successfully !!!!'


class AdminAdvertizementPositionUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'admintemplates/adminadvertizementpositionupdate.html'

    model = AdvertizementPosition
    fields = ['position']
    template_name_suffix = '_form'
    success_url = reverse_lazy('newsapp:advertizementposition')
    success_message = 'Update is successfully saved!!!!'


class AdminAdvertizementPositionDelete(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'admintemplates/adminadvertizementpositiondelete.html'

    model = AdvertizementPosition
    success_url = reverse_lazy('newsapp:advertizementposition')
    success_message = 'Deleted  successfully !!!!'

class AdminAdvertizementList(ListView):
    template_name = 'admintemplates/adminadvertizementlist.html'
    model = Advertizement
    context_object_name = 'advertizementlist'


class AdminAdvertizementCreate(SuccessMessageMixin, CreateView):
    template_name = "admintemplates/adminadvertizementadd.html"
    model = Advertizement
    form_class = AdminAdvertizement
    success_url = reverse_lazy('newsapp:advertizement')
    success_message = 'Created successfully !!!!'


class AdminAdvertizementUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'admintemplates/adminadvertizementupdate.html'
    model = Advertizement
    form_class = AdminAdvertizement
    success_url = reverse_lazy('newsapp:advertizement')
    success_message = 'Update is successfully saved!!!!'


class AdminAdvertizementDelete(SuccessMessageMixin, DeleteView):
    template_name = 'admintemplates/adminadvertizementdelete.html'
    model = Advertizement
    context_object_name = 'adsdelete'
    success_url = reverse_lazy('newsapp:advertizement')
    success_message = 'Deleted successfully !!!!'

class AdminOrganizationInformationList(ListView):
    template_name = 'admintemplates/adminorganizationinformationlist.html'
    model = OrgnizationalInformation
    # _form = template_name_suffix
    context_object_name = 'organizationinformationlist'

class AdminOrganizationInformationDetail(DetailView):
    template_name = 'admintemplates/adminorganizationinformationdetail.html'
    model = OrgnizationalInformation
    context_object_name = 'informationdetail'

class AdminOrganizationInformationUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'admintemplates/adminorganizationinformationupdate.html'
    model = OrgnizationalInformation
    form_class= OrganizationInformationForm
    success_url = reverse_lazy('newsapp:organizationinformationlist')
    success_message = 'Update is successfully saved!!!!'

class AdminNewsCategoryCreate(SuccessMessageMixin, CreateView):
    template_name = "admintemplates/adminnewscategoryadd.html"
    model = NewsCategory
    form_class = NewsForm
    success_url = reverse_lazy('newsapp:adminnewscategory')
    success_message = 'Created successfully !!!!'

class AdminNewsCategoryList(ListView):
    template_name = 'admintemplates/adminnewscategorylist.html'
    model = NewsCategory
    context_object_name = 'adminnewscategorylist'

class AdminNewsCategoryUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'admintemplates/adminnewscategoryupdate.html'
    model = NewsCategory
    # fields = ['title', 'image', 'icon_character']
    # template_name_suffix = '_form'
    form_class = NewsCategoryForm
    success_url = reverse_lazy('newsapp:adminnewscategory')
    success_message = 'Update is successfully saved!!!!'

class AdminNewsCategoryDelete(SuccessMessageMixin, DeleteView):
    template_name = "admintemplates/adminnewscategorydelete.html"
    model = NewsCategory
    context_object_name = 'admincategorydelete'
    success_url = reverse_lazy('newsapp:adminnewscategory')
    success_message = 'Deleted  successfully !!!!'

class AdminNewsSubCategoryList(ListView):
    template_name = 'admintemplates/adminnewssubcategorylist.html'
    model = NewsSubCategory
    context_object_name = 'adminnewssubcategorylist'

class AdminNewsSubCategoryCreate(SuccessMessageMixin, CreateView):
    template_name = "admintemplates/adminnewssubcategoryadd.html"
    model = NewsSubCategory
    form_class = NewsSubCategoryForm
    success_url = reverse_lazy('newsapp:adminnewssubcategorylist')
    success_message = 'Created successfully !!!!'

class AdminNewsSubCategoryUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'admintemplates/adminnewssubcategoryupdate.html'
    model = NewsSubCategory
    fields = ['title', 'main_category', 'image', 'icon_character']
    template_name_suffix = '_form'
    success_url = reverse_lazy('newsapp:adminnewssubcategorylist')
    success_message = 'Update is successfully saved!!!!'

class AdminNewsSubCategoryDelete(SuccessMessageMixin, DeleteView):
    template_name = "admintemplates/adminnewssubcategorydelete.html"
    model = NewsSubCategory
    success_url = reverse_lazy('newsapp:adminnewssubcategorylist')
    success_message = 'Deleted successfully !!!!'

class AdminNewsList(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminnewslist.html'
    model = News
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = News.objects.order_by('-created_at')
        return context
class AdminNewsDetailView(DetailView):
    template_name = "admintemplates/adminnewsdetail.html"
    model = News
    context_object_name = 'adminnewsdetail'

class AdminNewsCreate(SuccessMessageMixin, CreateView):
    template_name = 'admintemplates/adminnewsadd.html'
    model = News
    form_class = AdminNewsForm
    context_object_name = 'newscreate'
    success_url = reverse_lazy('newsapp:adminnewslist')
    success_message = 'Created successfully !!!!'

    def form_valid(self, form):
        user = self.request.user.admin.id
        print(user)
        editor = Admin.objects.get(id=user)
        print(editor)
        form.instance.admin = editor
        return super().form_valid(form)


class AdminNewsUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'admintemplates/adminnewsupdate.html'
    model = News
    form_class = AdminNewsForm
    success_url = reverse_lazy('newsapp:adminnewslist')
    success_message = 'Update is successfully saved!!!!'


class AdminNewsDelete(SuccessMessageMixin, DeleteView):
    template_name = 'admintemplates/adminewsdelete.html'
    model = News
    success_url = reverse_lazy('newsapp:adminnewslist')
    success_message = 'Deleted successfully !!!!'


class AdminEditorNewsListView(AdminRequiredMixin, DetailView):
    template_name = 'admintemplates/admineditornewslist.html'
    model = Editor
    context_object_name = 'admineditorlist'

class AdminEditorNewsListDetailView(AdminRequiredMixin, DetailView):
    template_name = 'admintemplates/admineditornewslistdetail.html'
    model = News
    context_object_name = 'newslistdetails'

class EditorDashboardList(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/admineditorlist.html'
    model = Editor
    context_object_name = 'admineditor'

class AdminEditorDetailView(DetailView):
    template_name = 'admintemplates/admineditordetail.html'
    model = Editor
    context_object_name = 'admineditordetail'

class AdminDetailsView(DetailView):
    template_name = 'admintemplates/admindetails.html'
    model = Admin
    context_object_name = 'admindetails'


class EditorList(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/admineditorlist.html'
    model = Editor
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['admineditorlist'] = Editor.objects.order_by('-created_at')
        return context

class EditorCreate(SuccessMessageMixin, CreateView):
    template_name = 'admintemplates/admineditoradd.html'
    model = Editor
    form_class = EditorForm
    context_object_name = 'admineditorcreate'
    success_url = reverse_lazy('newsapp:editorlist')

class EditorUpdate(UpdateView,SuccessMessageMixin):
    template_name = 'admintemplates/admineditorupdate.html'
    model = Editor
    form_class = EditorUpdateForm
    success_url = reverse_lazy('newsapp:editorlist')
    success_message = 'Update is successfully saved!!!!'

class EditorDelete(SuccessMessageMixin, DeleteView):
    template_name = 'admintemplates/admineditordelete.html'
    model = Editor
    context_object_name = 'editordelete'
    success_url = reverse_lazy('newsapp:editorlist')
    success_message = 'Deleted  successfully !!!!'

class AdminList(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminlist.html'
    model = Admin
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['adminlist'] = Admin.objects.order_by('-created_at')
        return context
class ClientMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.filter(root=None)
        context['subform'] = SubscriberForm
        context['latestnews'] = News.objects.order_by('-id')
        context['testnewslist'] = News.objects.all()
        return context

class OrganizationMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = OrgnizationalInformation.objects.all()
        return context

class EditorMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editornewsdetail'] = Editor.objects.all()
        return context


class RootNewsMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rootnewslist'] = News.objects.filter(root=self.object.root)
        return context

# class NewsVerified(object):
#     def get_context_data(self,**kwargs):
#         context=super().get_context_data(**kwargs)
#         news=News.objects.filter(is_verified=True)
#         context['news']=news
#         return context
# class ClientHomeView(ClientMixin, TemplateView):


class ClientHomeView(ClientMixin, OrganizationMixin, TemplateView):
    template_name = 'clienttemplates/clienthome1.html'
    def get_context_data(self, **kwargs):
        news = News.objects.filter(is_verified=True)
        context = super().get_context_data(**kwargs)

        context['videolist'] = news.exclude(video_link=None)
        context['clientcategorylist'] = NewsCategory.objects.filter(root=None)
        context['topviewednews'] = news.order_by('-view_count')
        context['popularnews'] = news.order_by('-view_count')
        context['hotnews'] = news.order_by('-created_at')
        context['newslist'] = News.objects.filter(is_verified=True)
        context['clientcategorylist'] = NewsCategory.objects.filter(root=None)
        context['topviewednews'] = News.objects.order_by(
            '-view_count').filter(is_verified=True)
        context['popularnews'] = News.objects.order_by(
            '-view_count').filter(is_verified=True)
        context['hotnews'] = News.objects.order_by(
            'created_at').filter(is_verified=True)
        context['mostcommented'] = Comment.objects.order_by('-comment')
        context['newseditor'] = Editor.objects.all()
        context['advertiselist'] = Advertizement.objects.all()
        context['subform'] = SubscriberForm

        context['latestnews'] = news.order_by('-id')
        context['topviews'] = news.order_by('-view_count')
        context['categorys'] = NewsCategory.objects.filter(root=None)
        categories = NewsCategory.objects.filter(root=None)
        
        return context


class ClientAboutView(ClientMixin, OrganizationMixin, TemplateView):
    template_name = 'clienttemplates/clientabout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = OrgnizationalInformation.objects.all()
        return context


class VideoGalleryView(ClientMixin, OrganizationMixin, TemplateView):
    template_name = 'clienttemplates/videogallery.html'

    def get_context_data(self, **kwargs):
        news = News.objects.filter(is_verified=True)
        context = super().get_context_data(**kwargs)
        context['videogallerys'] = news.exclude(video_link=None)
        print('--', context['videogallerys'])
        return context


class OrganizationPrivacyView(ClientMixin, OrganizationMixin, TemplateView):
    template_name = 'clienttemplates/privacypolicy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacypolicy'] = OrgnizationalInformation.objects.all()
        return context

class SearchView(ClientMixin, OrganizationMixin, TemplateView):
    template_name = 'clienttemplates/searchresult.html'

    def get_context_data(self, **kwargs):
        news1 = News.objects.filter(is_verified=True)
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('search')
        print(keyword, '***********')
        news = news1.filter(Q(title__icontains=keyword) | Q(
            content__icontains=keyword) | Q(main_category__title__icontains=keyword))
        context['searchednews'] = news
        return context


class CommentCreateView(ClientMixin, OrganizationMixin, CreateView):
    template_name = 'clienttemplates/commentcreate.html'
    form_class = CommentForm
    success_url = '/'
    def form_valid(self, form):
        news_id = self.kwargs['pk']
        news = News.objects.get(id=news_id)
        form.instance.news = news
        return super().form_valid(form)
    def get_success_url(self):
        news_id = self.kwargs['pk']
        return '/news/' + str(news_id) + '/detail/'

class ClientNewsDetailView(ClientMixin, OrganizationMixin, DetailView):
    template_name = 'clienttemplates/clientnewsdetail.html'
    queryset = News.objects.all()
    context_object_name = 'clientnewsdetail'
    def get_context_data(self, **kwargs):
        news = News.objects.filter(is_verified=True)
        context = super().get_context_data(**kwargs)
        news_id = self.kwargs["pk"]
        clientnewsdetail = News.objects.get(id=news_id)
        clientnewsdetail.view_count += 1
        clientnewsdetail.save()
        context['advertiselist'] = Advertizement.objects.all()
        context['popularnews'] = news.order_by('-view_count')
        context['latestnews'] = news.order_by('-id')
        context['newseditor'] = Editor.objects.all()
        context['commentform'] = CommentForm
        context['commentlist'] = Comment.objects.all().order_by('-id')
        context['commentlist1'] = str(Comment.objects.all().count())
        context['relatednewslist'] = news.filter(
            main_category=self.object.main_category).exclude(slug=self.object.slug)
        return context


class ClientContactView(ClientMixin, OrganizationMixin, SuccessMessageMixin, CreateView):
    template_name = 'clienttemplates/clientcontact.html'
    form_class = ContactForm
    success_message = 'thank you,we will contact '
    success_url = '/'


class ClientCategoryDetailView(ClientMixin, OrganizationMixin, DetailView):
    template_name = 'clienttemplates/clientcategorydetail.html'
    model = NewsCategory
    context_object_name = 'clientcategorydetail'
    def get_context_data(self, **kwargs):
        news=News.objects.filter(is_verified=True)
        context = super().get_context_data(**kwargs)
        news1 = News.objects.filter(
            main_category=self.object).exclude(is_verified=False)
        context['filtered_news'] = news1
        context['rootcategorylist'] = NewsCategory.objects.filter(
            root=self.object.root)
        context['advertiselist'] = Advertizement.objects.all()
        context['popularnews'] = news.order_by('-view_count')
        context['mostcommented'] = Comment.objects.order_by('-comment')
        context['newseditor'] = Editor.objects.all()
        context['latestnews'] = news.order_by('-id')
        context['videolist'] = news.exclude(video_link=None)
        return context

class EditorDetailView(ClientMixin, OrganizationMixin, DetailView):
    template_name = 'clienttemplates/editordetail.html'
    model = Editor
    context_object_name = 'editordetail'


class ClientSubcategoryDetailView(ClientMixin, DetailView):
    template_name = 'clienttemplates/clientsubcategorydetail.html'
    model = NewsSubCategory
    context_object_name = 'clientsubcategorydetail'


class PopularNewsListView(ClientMixin, OrganizationMixin, ListView):
    template_name = 'clienttemplates/clientpopularnewslist.html'
    model = News
    context_object_name = 'popularnewslist'
    def get_context_data(self, **kwargs):
        news = News.objects.filter(is_verified=True)
        context = super().get_context_data(**kwargs)
        context['advertiselist'] = Advertizement.objects.all()
        context['popularnews'] = news.order_by('-view_count')
        context['mostcommented'] = Comment.objects.order_by('-comment')
        return context

class MostCommentedNewsListView(ClientMixin, OrganizationMixin, ListView):
    template_name = 'clienttemplates/clientmostcommentednewslist.html'
    model = News
    context_object_name = 'mostcommentednewslist'
    def get_context_data(self, **kwargs):
        news = News.objects.filter(is_verified=True)
        context = super().get_context_data(**kwargs)
        context['advertiselist'] = Advertizement.objects.all()
        context['popularnews'] = news.order_by('-view_count')
        context['mostcommented'] = news.order_by('-comment')
        return context

class SubscriberView(SuccessMessageMixin, CreateView):
    template_name = "clienttemplates/clientbase.html"
    form_class = SubscriberForm
    success_url = reverse_lazy('newsapp:clienthome')
    # success_message = "thank you for subscribing"
    def form_valid(self, form):
        self.success_url = self.request.META.get('HTTP_REFERER')
        email = form.cleaned_data["email"]
        if Subscriber.objects.filter(email=email).exists():
            data = {
                'error': "Email already exists!"
            }
            return JsonResponse(data)
        else:
            form.save()
            data = {
                'success': "Thank you for subscribing us!"
            }
            return JsonResponse(data)
        return super().form_valid(form)

class AjaxAdminHome(View):
    def get(self, request, **kwargs):
        start = request.GET.get('start')
        end = request.GET.get('end')
        print(start + end, '_________')
        newscount = News.objects.filter(
            created_at__gte=start, created_at__lte=end).count()
        print(newscount,'____________________')
        viewscount = 0
        for views in News.objects.filter(created_at__gte=start,created_at__lte=end):
            viewscount += views.view_count

        print(viewscount,'_________________')

        editorinfo = request.GET.get('editorinfo')
        editorinfocount = Editor.objects.filter(
            created_at__gte=start, created_at__lte=end).count()
        print(editorinfocount,'-------------')
        allnews = News.objects.filter(created_at__gte=start, created_at__lte=end)
        editors = Editor.objects.all()
        return render(request, 'admintemplates/ajaxadminhome1.html', {'allnews': allnews,
         'editors': editors, 'newscount': newscount,'viewscount':viewscount,'editorinfocount':editorinfocount,
         'start':start,'end':end,})
