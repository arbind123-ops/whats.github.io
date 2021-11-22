from django.conf import settings
from django.conf.urls.static import static
from newsapp.views import *
import django.contrib
from django.urls import include, path
from newsapp import views

app_name = "newsapp"
urlpatterns = [


    # client url
    # client url
    # client url
    # client url
    # path('base/',ClientBaseView.as_view(),name='clientbase'),
    path('', ClientHomeView.as_view(), name='clienthome'),
    path('video/',VideoGalleryView.as_view(),name='videogallery'),
    path('news/<int:pk>/detail/',
         ClientNewsDetailView.as_view(), name='clientnewsdetail'),
    path('news/category/<int:pk>/detail/', ClientCategoryDetailView.as_view(),
         name='clientcategorydetail'),
    path('news/popular/list/', PopularNewsListView.as_view(),
         name='popularnewslist'),
    path('news/mostcommented/list/', MostCommentedNewsListView.as_view(),
         name='mostcommentednewslist'),
    path('client/subcategory/<int:pk>/detail/',
         ClientSubcategoryDetailView.as_view(), name='clientsubcategory'),
    path('editor/<int:pk>/detail/',
         EditorDetailView.as_view(), name='editornewsdetail'),
    path('search/', SearchView.as_view(), name='searched'),
    path('contact/', ClientContactView.as_view(), name='clientcontact'),
    path('about/',ClientAboutView.as_view(),name='clientabout'),
    path('privacy/policy/',OrganizationPrivacyView.as_view(),name='organizationprivacy'),



    path('subscriber/', SubscriberView.as_view(), name='subscriber'),
    path('commentcreate/<int:pk>/',
         CommentCreateView.as_view(), name='commentcreate'),
    # path('news/<int:pk>/detail/',
    #      ClientNewsDetailView.as_view(), name='clientnewsdetail'),
    # editor url
    # editor url
    # editor url
    # editor url


    path('editor/', EditorHomeView.as_view(), name='editorhome'),
    path('editor/newslist/', EditorNewsList.as_view(), name='newslist'),

    # editor news
    # editor news 
    # editor news
    # editor news
    path('editor/<int:pk>/newsdetail',
         EditorNewsDetailView.as_view(), name='newsdetail'),
    path('ajax/load-subcategories/', views.load_subcategories,
         name='load_subcategories'),
    path('editor/newsadd/',
         EditorNewsCreate.as_view(), name='newsadd'),
    path('editor/<int:pk>/newsupdate/',
         EditorNewsUpdate.as_view(), name='newsupdate'),
    path('editor/<int:pk>/newsdelete/',
         EditorNewsDelete.as_view(), name='newsdelete'),
    path('editor-registration/',
         EditorRegistrationView.as_view(), name='editorregistration'),
    path('login/',
         LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('admin/<int:pk>/edit/', EditUserProfileView.as_view(),
         name="edit-user-profile"),
    path('editor/<int:pk>/edit/', EditUsersProfileView.as_view(),
         name="editor-user-profile"),
    path("password/change/",
         PasswordChangeView.as_view(), name="passwordchange"),
    path("editor-password/change/",
         EditorPasswordChangeView.as_view(), name="editorpasswordchange"),


    # admin url
    # admin url
    # admin url
    # admin url

    # admin advertizementposition
    # admin advertizementposition
    # admin advertizementposition
    # admin advertizementposition

    path('adminhome/', AdminView.as_view(), name='adminhome'),
    path('admin/adminadvetizementposition',
         AdminAdvertizementPositionList.as_view(), name='advertizementposition'),
    path('admin/advertizementpositionadd',
         AdminAdvertizementPositionCreate.as_view(), name='advertizementpositionadd'),
    path('admin/<int:pk>/advertizementpositionupdate',
         AdminAdvertizementPositionUpdate.as_view(), name='advertizementpositionupdate'),
    path('admin/<int:pk>/advertizementpositiondelete',
         AdminAdvertizementPositionDelete.as_view(), name='advertizementpositiondelete'),

    # admin advertizement
    # admin advertizement
    # admin advertizement
    # admin advertizement

    path('admin/adminadvettizement',
         AdminAdvertizementList.as_view(), name='advertizement'),
    path('admin/advertizementadd',
         AdminAdvertizementCreate.as_view(), name='advertizementadd'),
    path('admin/<int:pk>/advertizementupdate',
         AdminAdvertizementUpdate.as_view(), name='advertizementupdate'),
    path('admin/<int:pk>/advertizementdelete',
         AdminAdvertizementDelete.as_view(), name='advertizementdelete'),
    path('admin-registration/', AdminRegistrationView.as_view(),
         name='adminregistration'),

    # admin organizationinformation
    # admin organizationinformation
    # admin organizationinformation
    # admin organizationinformation
    path('admin/organizationinformation',
         AdminOrganizationInformationList.as_view(), name='organizationinformationlist'),

    path('admin/<int:pk>/organizationinformationdetail',
         AdminOrganizationInformationDetail.as_view(), name='organizationinformationdetail'),
    path('admin/<int:pk>/organizationinformationupdate',
         AdminOrganizationInformationUpdate.as_view(), name='organizationinformationupdate'),

    # admin newscategory
    # admin newscategory
    # admin newscategory
    # admin newscategory

    path('admin/newscategory/',
         AdminNewsCategoryList.as_view(), name='adminnewscategory'),
    path('admin/newscategoryadd',
         AdminNewsCategoryCreate.as_view(), name='adminnewscategoryadd'),
    path('admin/<int:pk>/newscategoryupdate/',
         AdminNewsCategoryUpdate.as_view(), name='adminnewscategoryupdate'),
    path('admin/<int:pk>/newscategorydelete/',
         AdminNewsCategoryDelete.as_view(), name='adminnewscategorydelete'),

    # admin newssubcategory
    # admin newssubcategory
    # admin newssubcategory
    # admin newssubcategory

    path('admin/newssubcategorylist/',
         AdminNewsSubCategoryList.as_view(), name='adminnewssubcategorylist'),
    path('admin/newssubcategoryadd',
         AdminNewsSubCategoryCreate.as_view(), name='adminnewssubcategoryadd'),
    path('admin/<int:pk>/newssubcategoryupdate/',
         AdminNewsSubCategoryUpdate.as_view(), name='adminnewssubcategoryupdate'),
    path('admin/<int:pk>/newssubcategorydelete/',
         AdminNewsSubCategoryDelete.as_view(), name='adminnewssubcategorydelete'),


    # admin news
    # admin news
    # admin news
    # admin news

    path('admin/newslist',
         AdminNewsList.as_view(), name='adminnewslist'),
    path('admin/newslist/<int:pk>/', AdminDetailView.as_view(), name='newslist'),
    path('admin/<int:pk>/newsdetail',
         AdminNewsDetailView.as_view(), name='adminnewsdetail'),
    path('admin/newsadd/',
         AdminNewsCreate.as_view(), name='adminnewsadd'),
    path('admin/<int:pk>/newsupdate/',
         AdminNewsUpdate.as_view(), name='adminnewsupdate'),
    path('admin/<int:pk>/newsdelete/',
         AdminNewsDelete.as_view(), name='adminnewsdelete'),

    # admin editor
    # admin editor
    # admin editor
    # admin editor
    path('admin/editorlist',
         EditorList.as_view(), name='editorlist'),
    path('admin/editor',
         EditorDashboardList.as_view(), name='editor'),
    path('admin/editorcreate',
         EditorCreate.as_view(), name='editoradd'),
    path('admin/<int:pk>/editorupdate/',
         EditorUpdate.as_view(), name='editorupdate'),
    path('admin/<int:pk>/editordelete/',
         EditorDelete.as_view(), name='editordelete'),
    path('admin/<int:pk>/editordetail/',
         AdminEditorDetailView.as_view(), name='admineditordetail'),
    path('admin/<int:pk>/detail/',
         AdminDetailsView.as_view(), name='admindetails'),

    # admin admin
    # admin admin
    # admin admin
    # admin admin

    path('admin/adminlist',
         AdminList.as_view(), name='adminlist'),


    path('admineditor/<int:pk>/news-list/',
         AdminEditorNewsListView.as_view(), name='admineditornewslist'),
    path('admineditor/<int:pk>/news-list/detail/',
         AdminEditorNewsListDetailView.as_view(), name='admineditornewslistdetail'),
    path('ajaxadminhome/', AjaxAdminHome.as_view(), name='ajaxadminhome'),


]
