from django.contrib import admin
from core import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class ResourceSkillInline(admin.TabularInline):
    view_on_site = False
    model = models.ResourceSkill
    extra = 0
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['unit_link', 'process_step_link', 'edit_link', 'description']

    def edit_link(self, instance):
        try:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                                  instance._meta.model_name),
                          args=[instance.pk])
            if instance.pk and len(type(instance).objects.filter(pk=instance.pk)) == 1:
                return mark_safe(u'<a href="{u}">Edit</a>'.format(u=url))
            else:
                return '-'
        except:
            return '-'

    edit_link.short_description = 'Edit details'

    def process_step_link(self, instance):
        try:
            process_step = str(instance.skill.process_step.manufacturing_process)
            return process_step
        except:
            return "-"

    process_step_link.short_description = 'Process step'

    def unit_link(self, instance):
        try:
            unit = str(instance.skill.process_step.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'


class PartManufacturingProcessInline(admin.TabularInline):
    view_on_site = False
    model = models.PartManufacturingProcessStep
    extra = 0
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['unit_link', 'edit_link']

    def edit_link(self, instance):
        try:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                                  instance._meta.model_name),
                          args=[instance.pk])
            if instance.pk and len(type(instance).objects.filter(pk=instance.pk)) == 1:
                return mark_safe(u'<a href="{u}">Edit</a>'.format(u=url))
            else:
                return '-'
        except:
            return '-'

    edit_link.short_description = 'Edit details'

    def unit_link(self, instance):
        try:
            unit = str(instance.process_step.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'


class ConstraintInline(admin.TabularInline):
    view_on_site = False
    model = models.Constraint
    extra = 0
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['unit_link']

    def unit_link(self, instance):
        try:
            unit = str(instance.requirement.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'


class SkillConsumableInline(admin.TabularInline):
    view_on_site = False
    model = models.SkillConsumable
    extra = 0
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['unit_link']

    def unit_link(self, instance):
        try:
            unit = str(instance.consumable.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'


class AbilityInline(admin.TabularInline):
    view_on_site = False
    model = models.Ability
    extra = 0
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['unit_link']

    def unit_link(self, instance):
        try:
            unit = str(instance.requirement.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Unit
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'description']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Category
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'description']


@admin.register(models.ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.ProcessStep
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['manufacturing_process']


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Skill
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'description']


@admin.register(models.Part)
class PartAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Part
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['is_valid', 'volume', 'bounding_box_x', 'bounding_box_y', 'bounding_box_z',
                       'created_at', 'updated_at']
    search_fields = ['part']
    list_filter = ['is_valid']
    inlines = [PartManufacturingProcessInline]


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Resource
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'manufacturer', 'description']
    list_filter = ['manufacturer']
    inlines = [ResourceSkillInline]


@admin.register(models.Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Consumable
    list_display = [field.name for field in model._meta.fields]
    list_display.remove('unit')
    list_display.insert(2, 'unit_link')
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['unit__name']

    def unit_link(self, unit):
        try:
            url = reverse("admin:core_unit_change", args=[unit.unit.id])
            link = '<a href="%s">%s</a>' % (url, unit.unit.name)
            return mark_safe(link)
        except:
            return "-"

    unit_link.short_description = 'Unit'


@admin.register(models.Requirement)
class RequirementAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Requirement
    list_display = [field.name for field in model._meta.fields]
    list_display.remove('unit')
    list_display.insert(1, 'unit_link')
    list_display.remove('category')
    list_display.insert(1, 'category_link')
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['unit__name']

    def unit_link(self, unit):
        try:
            url = reverse("admin:core_unit_change", args=[unit.unit.id])
            link = '<a href="%s">%s</a>' % (url, unit.unit.name)
            return mark_safe(link)
        except:
            return "-"

    unit_link.short_description = 'Unit'

    def category_link(self, category):
        try:
            url = reverse("admin:core_category_change", args=[category.category.id])
            link = '<a href="%s">%s</a>' % (url, category.category.name)
            return mark_safe(link)
        except:
            return "-"

    category_link.short_description = 'Category'


@admin.register(models.ResourceSkill)
class ResourceSkillAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.ResourceSkill
    list_display = [field.name for field in model._meta.fields]
    # Remove the old element and replace it with a link.
    list_display.remove('resource')
    list_display.insert(1, 'resource_link')
    list_display.remove('skill')
    list_display.insert(2, 'skill_link')
    list_display.insert(3, 'process_step_link')
    list_display.insert(4, 'unit_link')

    readonly_fields = ['process_step_link', 'unit_link', 'created_at', 'updated_at']
    search_fields = ['resource__name', 'skill__name']
    inlines = [SkillConsumableInline, AbilityInline]

    def resource_link(self, resource):
        try:
            url = reverse("admin:core_resource_change", args=[resource.resource.id])
            link = '<a href="%s">%s</a>' % (url, resource.resource.name)
            return mark_safe(link)
        except:
            return "-"

    resource_link.short_description = 'Resource'

    def skill_link(self, skill):
        try:
            url = reverse("admin:core_skill_change", args=[skill.skill.id])
            link = '<a href="%s">%s</a>' % (url, skill.skill.name)
            return mark_safe(link)
        except:
            return "-"

    skill_link.short_description = 'Skill'

    def process_step_link(self, processstep):
        try:
            url = reverse("admin:core_processstep_change", args=[processstep.skill.process_step.id])
            link = '<a href="%s">%s</a>' % (url, processstep.skill.process_step.manufacturing_process)
            return mark_safe(link)
        except:
            return "-"

    process_step_link.short_description = 'Process step'

    def unit_link(self, instance):
        try:
            unit = str(instance.skill.process_step.unit)
            return unit
        except:
            return "-"

    unit_link.short_description = 'Unit'


@admin.register(models.SkillConsumable)
class SkillConsumableAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.SkillConsumable
    list_display = [field.name for field in model._meta.fields]
    # Remove the old element and replace it with a link.
    list_display.remove('resource_skill')
    list_display.insert(1, 'resource_skill_link')
    list_display.remove('consumable')
    list_display.insert(2, 'consumable_link')

    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['resource_skill__resource__name',
                     'resource_skill__skill__name',
                     'consumable__name']

    def resource_skill_link(self, resourceskill):
        try:
            url = reverse("admin:core_resourceskill_change", args=[resourceskill.resourceskill.id])
            link = '<a href="%s">%s</a>' % (url, resourceskill.resourceskill.name)
            return mark_safe(link)
        except:
            return "-"

    resource_skill_link.short_description = 'Resource Skill'

    def consumable_link(self, consumable):
        try:
            url = reverse("admin:core_consumable_change", args=[consumable.consumable.id])
            link = '<a href="%s">%s</a>' % (url, consumable.consumable.name)
            return mark_safe(link)
        except:
            return "-"

    consumable_link.short_description = 'Consumable'


@admin.register(models.Ability)
class AbilityAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Ability
    list_display = [field.name for field in model._meta.fields]
    # Remove the old element and replace it with a link.
    list_display.remove('resource_skill')
    list_display.insert(1, 'resource_skill_link')
    list_display.remove('requirement')
    list_display.insert(2, 'requirement_link')

    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['resource_skill__skill__name', 'resource_skill__resource__name', 'requirement__name']

    def resource_skill_link(self, resourceskill):
        try:
            url = reverse("admin:core_resourceskill_change", args=[resourceskill.resourceskill.id])
            link = '<a href="%s">%s</a>' % (url, resourceskill.resourceskill.name)
            return mark_safe(link)
        except:
            return "-"

    resource_skill_link.short_description = 'Resource Skill'

    def requirement_link(self, requirement):
        try:
            url = reverse("admin:core_requirement_change", args=[requirement.requirement.id])
            link = '<a href="%s">%s</a>' % (url, requirement.requirement.name)
            return mark_safe(link)
        except:
            return "-"

    requirement_link.short_description = 'Requirement'


@admin.register(models.PartManufacturingProcessStep)
class PartManufacturingProcessAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.PartManufacturingProcessStep
    list_display = [field.name for field in model._meta.fields]
    # Remove the old element and replace it with a link.
    list_display.remove('part')
    list_display.insert(1, 'part_link')
    list_display.remove('process_step')
    list_display.insert(2, 'process_step_link')

    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['process_step__manufacturing_process']
    inlines = [ConstraintInline]

    def part_link(self, part):
        try:
            url = reverse("admin:core_part_change", args=[part.part.id])
            link = '<a href="%s">%s</a>' % (url, part.part.id)
            return mark_safe(link)
        except:
            return "-"

    part_link.short_description = 'Part'

    def process_step_link(self, process_step):
        try:
            url = reverse("admin:core_skill_change", args=[process_step.process_step.id])
            link = '<a href="%s">%s</a>' % (url, process_step.process_step.manufacturing_process)
            return mark_safe(link)
        except:
            return "-"

    process_step_link.short_description = 'Process Step'


@admin.register(models.Constraint)
class ConstraintAdmin(admin.ModelAdmin):
    view_on_site = False
    model = models.Constraint
    list_display = [field.name for field in model._meta.fields]
    # Remove the old element and replace it with a link.
    list_display.remove('part_manufacturing_process_step')
    list_display.insert(1, 'part_manufacturing_process_step_link')
    list_display.remove('requirement')
    list_display.insert(2, 'requirement_link')

    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['part_manufacturing_process_step__process_step__manufacturing_process', 'requirement__name']

    def part_manufacturing_process_step_link(self, part_manufacturing_process_step):
        try:
            url = reverse("admin:core_part_manufacturing_process_step_change",
                          args=[part_manufacturing_process_step.part_manufacturing_process_step.id])
            link = '<a href="%s">%s</a>' % (url,
                                            part_manufacturing_process_step.part_manufacturing_process_step.process_step.manufacturing_process)
            return mark_safe(link)
        except:
            return "-"

    part_manufacturing_process_step_link.short_description = 'Part Manufacturing Process Step'

    def requirement_link(self, requirement):
        try:
            url = reverse("admin:core_requirement_change", args=[requirement.requirement.id])
            link = '<a href="%s">%s</a>' % (url, requirement.requirement.name)
            return mark_safe(link)
        except:
            return "-"

    requirement_link.short_description = 'Requirement'
