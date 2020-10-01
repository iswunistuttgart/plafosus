from django.contrib import admin
from core import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class MachineSkillInline(admin.TabularInline):
    model = models.MachineSkill
    extra = 1
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']


class PartSkillInline(admin.TabularInline):
    model = models.PartSkill
    extra = 1
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.Part)
class PartAdmin(admin.ModelAdmin):
    model = models.Part
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['is_valid', 'volume', 'bounding_box_x', 'bounding_box_y', 'bounding_box_z',
                       'created_at', 'updated_at']
    search_fields = ['part']
    list_filter = ['is_valid']
    inlines = [PartSkillInline]


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    model = models.Skill
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name']


@admin.register(models.Machine)
class MachineAdmin(admin.ModelAdmin):
    model = models.Machine
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'manufacturer']
    inlines = [MachineSkillInline]


@admin.register(models.MachineSkill)
class MachineSkillAdmin(admin.ModelAdmin):
    model = models.MachineSkill
    list_display = [field.name for field in model._meta.fields]
    # Remove the old element and replace it with a link.
    list_display.remove('machine')
    list_display.insert(1, 'machine_link')
    list_display.remove('skill')
    list_display.insert(2, 'skill_link')

    readonly_fields = ['created_at', 'updated_at', 'machine_link', 'skill']
    search_fields = ['machine__name', 'skill__name']

    def machine_link(self, machine):
        try:
            url = reverse("admin:core_machine_change", args=[machine.machine.id])
            link = '<a href="%s">%s</a>' % (url, machine.machine.name)
            return mark_safe(link)
        except:
            return "-"
    machine_link.short_description = 'Machine'

    def skill_link(self, skill):
        try:
            url = reverse("admin:core_skill_change", args=[skill.skill.id])
            link = '<a href="%s">%s</a>' % (url, skill.skill.name)
            return mark_safe(link)
        except:
            return "-"
    skill_link.short_description = 'Skill'


@admin.register(models.PartSkill)
class PartSkillAdmin(admin.ModelAdmin):
    model = models.PartSkill
    list_display = [field.name for field in model._meta.fields]
    # Remove the old element and replace it with a link.
    list_display.remove('part')
    list_display.insert(1, 'part_link')
    list_display.remove('skill')
    list_display.insert(2, 'skill_link')

    readonly_fields = ['created_at', 'updated_at', 'part_link', 'skill']
    search_fields = ['skill__name']

    def part_link(self, part):
        try:
            url = reverse("admin:core_part_change", args=[part.part.id])
            link = '<a href="%s">%s</a>' % (url, part.part.id)
            return mark_safe(link)
        except:
            return "-"
    part_link.short_description = 'Part'

    def skill_link(self, skill):
        try:
            url = reverse("admin:core_skill_change", args=[skill.skill.id])
            link = '<a href="%s">%s</a>' % (url, skill.skill.name)
            return mark_safe(link)
        except:
            return "-"
    skill_link.short_description = 'Skill'
