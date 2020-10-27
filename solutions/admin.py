from django.contrib import admin
from solutions import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class PermutationConsumableCostInline(admin.TabularInline):
    view_on_site = False
    model = models.Permutation.consumables.through
    extra = 0
    can_delete = False
    list_display = [field.name for field in model._meta.fields]
    list_display.remove("id")
    readonly_fields = list_display
    readonly_fields.append('is_overall_link')
    readonly_fields.append('quantity_link')
    readonly_fields.append('price_link')
    readonly_fields.append('co2_link')
    readonly_fields.append('show_link')

    def show_link(self, instance):
        try:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                                  'consumablecost'),
                          args=[instance.consumablecost.pk])
            if instance.consumablecost.pk and len(type(instance).objects.filter(pk=instance.pk)) == 1:
                return mark_safe(u'<a href="{u}">Show</a>'.format(u=url))
            else:
                return '-'
        except Exception as e:
            return '-'

    show_link.short_description = 'Show details'

    def is_overall_link(self, instance):
        try:
            is_overall = str(instance.consumablecost.is_overall)
            return is_overall
        except:
            return "-"

    is_overall_link.short_description = 'Is Overall'

    def price_link(self, instance):
        try:
            price = str(instance.consumablecost.price)
            return price
        except:
            return "-"

    price_link.short_description = 'Price'

    def quantity_link(self, instance):
        try:
            quantity = str(instance.consumablecost.quantity)
            return quantity
        except:
            return "-"

    quantity_link.short_description = 'Quantity'

    def co2_link(self, instance):
        try:
            co2 = str(instance.consumablecost.co2)
            return co2
        except:
            return "-"

    co2_link.short_description = 'CO2'


class SolutionConsumableCostInline(admin.TabularInline):
    view_on_site = False
    model = models.Solution.consumables.through
    extra = 0
    can_delete = False
    list_display = [field.name for field in model._meta.fields]
    list_display.remove("id")
    readonly_fields = list_display
    readonly_fields.append('is_overall_link')
    readonly_fields.append('quantity_link')
    readonly_fields.append('price_link')
    readonly_fields.append('co2_link')
    readonly_fields.append('show_link')

    def show_link(self, instance):
        try:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                                  'consumablecost'),
                          args=[instance.consumablecost.pk])
            if instance.consumablecost.pk and len(type(instance).objects.filter(pk=instance.pk)) == 1:
                return mark_safe(u'<a href="{u}">Show</a>'.format(u=url))
            else:
                return '-'
        except Exception as e:
            return '-'

    show_link.short_description = 'Show details'

    def is_overall_link(self, instance):
        try:
            is_overall = str(instance.consumablecost.is_overall)
            return is_overall
        except:
            return "-"

    is_overall_link.short_description = 'Is Overall'

    def price_link(self, instance):
        try:
            price = str(instance.consumablecost.price)
            return price
        except:
            return "-"

    price_link.short_description = 'Price'

    def quantity_link(self, instance):
        try:
            quantity = str(instance.consumablecost.quantity)
            return quantity
        except:
            return "-"

    quantity_link.short_description = 'Quantity'

    def co2_link(self, instance):
        try:
            co2 = str(instance.consumablecost.co2)
            return co2
        except:
            return "-"

    co2_link.short_description = 'CO2'


class SolutionSpacePermutationsInline(admin.TabularInline):
    view_on_site = False
    model = models.SolutionSpace.permutations.through
    extra = 0
    can_delete = False
    list_display = [field.name for field in model._meta.fields]
    list_display.remove("id")
    readonly_fields = list_display
    readonly_fields.append('is_optimal_link')
    readonly_fields.append('manufacturing_possibility_link')
    readonly_fields.append('price_link')
    readonly_fields.append('time_link')
    readonly_fields.append('co2_link')
    readonly_fields.append('show_link')

    def show_link(self, instance):
        try:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                                  'permutation'),
                          args=[instance.permutation.pk])
            if instance.permutation.pk and len(type(instance).objects.filter(pk=instance.pk)) == 1:
                return mark_safe(u'<a href="{u}">Show</a>'.format(u=url))
            else:
                return '-'
        except Exception as e:
            return '-'

    show_link.short_description = 'Show details'

    def is_optimal_link(self, instance):
        try:
            is_optimal = str(instance.permutation.is_optimal)
            return is_optimal
        except:
            return "-"

    is_optimal_link.short_description = 'Is Optimal'

    def manufacturing_possibility_link(self, instance):
        try:
            manufacturing_possibility = str(instance.permutation.manufacturing_possibility)
            return manufacturing_possibility
        except:
            return "-"

    manufacturing_possibility_link.short_description = 'Manufacturing Possibility'

    def price_link(self, instance):
        try:
            price = str(instance.permutation.price)
            return price
        except:
            return "-"

    price_link.short_description = 'Price'

    def time_link(self, instance):
        try:
            time = str(instance.permutation.time)
            return time
        except:
            return "-"

    time_link.short_description = 'Time'

    def co2_link(self, instance):
        try:
            co2 = str(instance.permutation.co2)
            return co2
        except:
            return "-"

    co2_link.short_description = 'CO2'


class PermutationSolutionsInline(admin.TabularInline):
    view_on_site = False
    model = models.Permutation.solutions.through
    extra = 0
    can_delete = False
    list_display = [field.name for field in model._meta.fields]
    list_display.remove("id")
    readonly_fields = list_display
    readonly_fields.append('price_link')
    readonly_fields.append('time_link')
    readonly_fields.append('co2_link')
    readonly_fields.append('manufacturing_sequence_number_link')
    readonly_fields.append('show_link')

    def show_link(self, instance):
        try:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                                  'solution'),
                          args=[instance.solution.pk])
            if instance.solution.pk and len(type(instance).objects.filter(pk=instance.pk)) == 1:
                return mark_safe(u'<a href="{u}">Show</a>'.format(u=url))
            else:
                return '-'
        except Exception as e:
            return '-'

    show_link.short_description = 'Show details'

    def price_link(self, instance):
        try:
            price = str(instance.solution.price)
            return price
        except:
            return "-"

    price_link.short_description = 'Price'

    def time_link(self, instance):
        try:
            time = str(instance.solution.time)
            return time
        except:
            return "-"

    time_link.short_description = 'Time'

    def co2_link(self, instance):
        try:
            co2 = str(instance.solution.co2)
            return co2
        except:
            return "-"

    co2_link.short_description = 'CO2'

    def manufacturing_sequence_number_link(self, instance):
        try:
            manufacturing_sequence_number = str(instance.solution.manufacturing_sequence_number)
            return manufacturing_sequence_number
        except:
            return "-"

    manufacturing_sequence_number_link.short_description = 'Sequence Number'


@admin.register(models.ConsumableCost)
class ConsumableCostAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.ConsumableCost
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = list_display


@admin.register(models.Solution)
class SolutionAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Solution
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = list_display
    inlines = [SolutionConsumableCostInline]


@admin.register(models.Permutation)
class PermutationAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Permutation
    list_display = [field.name for field in model._meta.fields]
    # list_display.remove('solutions')
    readonly_fields = list_display
    inlines = [PermutationConsumableCostInline, PermutationSolutionsInline]


@admin.register(models.SolutionSpace)
class SolutionSpaceAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.SolutionSpace
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = list_display
    inlines = [SolutionSpacePermutationsInline]

# TODO: Display the names of the consumables in the single inlines.
