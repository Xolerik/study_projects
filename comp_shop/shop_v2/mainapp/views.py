from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from .models import Product, Smartphone, Notebook
# Create your views here.
def index(request):

    return render(request, "layout/base.html", {})

class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        #_base_manager - аналог objects для выборки объектов
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'




