from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Product, ProductImage, Stock, ProductReview


class ProductImageInline(admin.TabularInline):
    """
    Inline para imagens dos produtos.
    """
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')


class StockInline(admin.TabularInline):
    """
    Inline para movimentações de estoque.
    """
    model = Stock
    extra = 0
    fields = ('movement_type', 'quantity', 'reason', 'created_by', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Department.
    """
    list_display = ('name', 'slug', 'is_active', 'products_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Produtos'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Product.
    """
    list_display = ('name', 'department', 'current_price_display', 'stock_quantity', 'is_active', 'is_featured', 'created_at')
    list_filter = ('department', 'is_active', 'is_featured', 'is_on_promotion', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'stock_quantity')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'slug', 'department', 'short_description', 'description')
        }),
        ('Preços', {
            'fields': ('price', 'promotional_price', 'is_on_promotion')
        }),
        ('Imagens', {
            'fields': ('main_image',)
        }),
        ('Especificações', {
            'fields': ('weight', 'dimensions'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at', 'stock_quantity'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProductImageInline, StockInline]
    
    def current_price_display(self, obj):
        if obj.is_on_promotion and obj.promotional_price:
            return format_html(
                '<span style="text-decoration: line-through;">R$ {}</span><br>'
                '<strong style="color: red;">R$ {}</strong>',
                obj.price, obj.promotional_price
            )
        return f'R$ {obj.price}'
    current_price_display.short_description = 'Preço Atual'
    current_price_display.allow_tags = True


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo ProductImage.
    """
    list_display = ('product', 'image_preview', 'alt_text', 'order')
    list_filter = ('product__department',)
    search_fields = ('product__name', 'alt_text')
    ordering = ('product', 'order')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return 'Sem imagem'
    image_preview.short_description = 'Preview'


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Stock.
    """
    list_display = ('product', 'movement_type', 'quantity', 'reason', 'created_by', 'created_at')
    list_filter = ('movement_type', 'created_at', 'product__department')
    search_fields = ('product__name', 'reason')
    readonly_fields = ('created_at',)
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo ProductReview.
    """
    list_display = ('product', 'customer', 'rating', 'title', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'customer__full_name', 'title', 'comment')
    readonly_fields = ('created_at',)
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Aprovar avaliações selecionadas'
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = 'Desaprovar avaliações selecionadas'
