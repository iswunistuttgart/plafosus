from django.contrib import admin
from solutions import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class PermutationConsumableCostInline(admin.TabularInline):
    view_on_site = False
    model = models.Permutation.consumables.through
    extra = 0
    can_delete = False
    can_add = False
    list_display = [field.name for field in model._meta.fields]
    list_display.remove("id")
    readonly_fields = list_display
    readonly_fields.append('name_link')
    readonly_fields.append('quantity_link')
    readonly_fields.append('unit_link')
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

    def name_link(self, instance):
        try:
            url = reverse("admin:core_consumable_change", args=[instance.consumablecost.consumable.id])
            link = '<a href="%s">%s</a>' % (url, instance.consumablecost.consumable.name)
            return mark_safe(link)
        except:
            return "-"

    name_link.short_description = 'Consumable'

    def unit_link(self, instance):
        try:
            unit = str(instance.consumablecost.consumable.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'

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
    can_add = False
    list_display = [field.name for field in model._meta.fields]
    list_display.remove("id")
    readonly_fields = list_display
    readonly_fields.append('name_link')
    readonly_fields.append('quantity_link')
    readonly_fields.append('unit_link')
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

    def name_link(self, instance):
        try:
            url = reverse("admin:core_consumable_change", args=[instance.consumablecost.consumable.id])
            link = '<a href="%s">%s</a>' % (url, instance.consumablecost.consumable.name)
            return mark_safe(link)
        except:
            return "-"

    name_link.short_description = 'Consumable'

    def unit_link(self, instance):
        try:
            unit = str(instance.consumablecost.consumable.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'

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
    can_add = False
    list_display = [field.name for field in model._meta.fields]
    list_display.remove("id")
    readonly_fields = list_display
    readonly_fields.append('rank_link')
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

    def rank_link(self, instance):
        try:
            rank = str(instance.permutation.rank)
            return rank
        except:
            return "-"

    rank_link.short_description = 'Rank'

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
    readonly_fields.append('resource_link')
    readonly_fields.append('resource_skill_link')
    readonly_fields.append('part_manufacturing_process_step_link')
    readonly_fields.append('quantity_link')
    readonly_fields.append('unit_link')
    readonly_fields.append('price_link')
    readonly_fields.append('time_link')
    readonly_fields.append('co2_link')
    readonly_fields.append('manufacturing_sequence_number_link')
    readonly_fields.append('show_link')

    def quantity_link(self, instance):
        try:
            quantity = str(instance.solution.quantity)
            return quantity
        except:
            return "-"

    quantity_link.short_description = 'Quantity'

    def unit_link(self, instance):
        try:
            unit = str(instance.solution.resource_skill.skill.process_step.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'

    def resource_link(self, instance):
        try:
            url = reverse("admin:core_resource_change", args=[instance.solution.resource_skill.resource.id])
            link = '<a href="%s">%s</a>' % (url, instance.solution.resource_skill.resource.name)
            return mark_safe(link)
        except:
            return "-"

    resource_link.short_description = 'Resource'

    def resource_skill_link(self, instance):
        try:
            url = reverse("admin:core_resourceskill_change", args=[instance.solution.resource_skill.id])
            link = '<a href="%s">%s</a>' % (url, instance.solution.resource_skill.skill.name)
            return mark_safe(link)
        except:
            return "-"

    resource_skill_link.short_description = 'Resource Skill'

    def part_manufacturing_process_step_link(self, instance):
        try:
            url = reverse("admin:core_partmanufacturingprocessstep_change",
                          args=[instance.solution.part_manufacturing_process_step.id])
            link = '<a href="%s">%s</a>' % (
            url, instance.solution.part_manufacturing_process_step.process_step.manufacturing_process)
            return mark_safe(link)
        except:
            return "-"

    part_manufacturing_process_step_link.short_description = 'Part Manufacturing Process Step'

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

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ['id', 'consumable_link', 'is_overall', 'quantity', 'price', 'co2', 'created_at', 'updated_at']
    readonly_fields = ['consumable_link', 'is_overall', 'quantity', 'price', 'co2', 'created_at', 'updated_at']

    fieldsets = (
        ('Consumable Cost', {
            'fields': ('consumable_link', 'is_overall', 'quantity', 'price', 'co2',)
        }),
        ('Optional Information', {

            'classes': ('collapse',),

            'fields': ('created_at', 'updated_at')
        }),
    )

    def consumable_link(self, instance):
        try:
            url = reverse("admin:core_consumable_change", args=[instance.consumable.id])
            link = '<a href="%s">%s</a>' % (url, instance.consumable.name)
            return mark_safe(link)
        except:
            return "-"

    consumable_link.short_description = 'Consumable'


@admin.register(models.Solution)
class SolutionAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Solution

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ['id', 'resource_skill_link', 'part_manufacturing_process_step_link', 'quantity', 'price', 'time',
                    'co2','unit_link', 'created_at', 'updated_at']
    readonly_fields = ['part_manufacturing_process_step_link', 'resource_link', 'resource_skill_link', 'quantity',
                       'unit_link', 'price', 'time', 'co2', 'manufacturing_sequence_number', 'created_at', 'updated_at']

    fieldsets = (
        ('Solution', {
            'fields': ('resource_link', 'resource_skill_link', 'part_manufacturing_process_step_link',
                       'manufacturing_sequence_number', 'quantity', 'unit_link', 'price', 'time', 'co2',)
        }),
        ('Optional Information', {

            'classes': ('collapse',),

            'fields': ('created_at', 'updated_at')
        }),
    )

    inlines = [SolutionConsumableCostInline]

    def unit_link(self, instance):
        try:
            unit = str(instance.resource_skill.skill.process_step.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'

    def resource_link(self, instance):
        try:
            url = reverse("admin:core_resource_change", args=[instance.resource_skill.resource.id])
            link = '<a href="%s">%s</a>' % (url, instance.resource_skill.resource.name)
            return mark_safe(link)
        except:
            return "-"

    resource_link.short_description = 'Resource'

    def resource_skill_link(self, instance):
        try:
            url = reverse("admin:core_resourceskill_change", args=[instance.resource_skill.id])
            link = '<a href="%s">%s</a>' % (url, instance.resource_skill.skill.name)
            return mark_safe(link)
        except:
            return "-"

    resource_skill_link.short_description = 'Resource Skill'

    def part_manufacturing_process_step_link(self, instance):
        try:
            url = reverse("admin:core_partmanufacturingprocessstep_change",
                          args=[instance.part_manufacturing_process_step.id])
            link = '<a href="%s">%s</a>' % (
            url, instance.part_manufacturing_process_step.process_step.manufacturing_process)
            return mark_safe(link)
        except:
            return "-"

    part_manufacturing_process_step_link.short_description = 'Part Manufacturing Process Step'


@admin.register(models.Permutation)
class PermutationAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Permutation

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ['id', 'rank', 'manufacturing_possibility', 'price', 'time', 'co2', 'created_at', 'updated_at']
    readonly_fields = ['rank', 'manufacturing_possibility', 'price', 'time', 'co2', 'created_at', 'updated_at']
    inlines = [PermutationConsumableCostInline, PermutationSolutionsInline]

    fieldsets = (
        ('Solution Space', {
            'fields': ('rank', 'manufacturing_possibility', 'price', 'time', 'co2',)
        }),
        ('Optional Information', {

            'classes': ('collapse',),

            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(models.SolutionSpace)
class SolutionSpaceAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.SolutionSpace

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ['id', 'part_link', 'created_at', 'updated_at']
    readonly_fields = ['part_link', 'created_at', 'updated_at']
    inlines = [SolutionSpacePermutationsInline]

    fieldsets = (
        ('Solution Space', {
            'fields': ('part_link',)
        }),
        ('Optional Information', {

            'classes': ('collapse',),

            'fields': ('created_at', 'updated_at')
        }),
    )

    def part_link(self, instance):
        try:
            url = reverse("admin:core_part_change", args=[instance.part.id])
            link = '<a href="%s">%s</a>' % (url, instance.part.id)
            return mark_safe(link)
        except:
            return "-"

    part_link.short_description = 'Part'
