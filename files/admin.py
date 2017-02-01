from django.contrib import admin
from files.models import MyFile, Imprt, TagType, Tag


@admin.register(MyFile)
class MyFileAdmin(admin.ModelAdmin):
    readonly_fields = ('imported_date', 'created_date', 'hash', 'path', 'imported_from_path', 'imprt')
    ordering = ('created_date', 'path')


class MyFileTabularInline(admin.TabularInline):
    model = MyFile
    extra = 0
    can_delete = False
    fields = ('imported_from_path', 'path')
    readonly_fields = ('imported_from_path', 'path')
    show_change_link = True


@admin.register(Imprt)
class ImprtAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    inlines = [MyFileTabularInline,]


class TagInline(admin.TabularInline):
    model = Tag
    extra = 0
    can_delete = False
    fields = ('value',)
    readonly_fields = ('value',)
    show_change_link = True


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    inlines = [TagInline,]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # inlines = [ImprtInline,]
    pass