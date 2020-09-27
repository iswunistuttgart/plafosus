from django.contrib import admin
from core import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class AppliedSkillInline(admin.TabularInline):
    model = models.AppliedSkill
    extra = 1
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.Part)
class PartAdmin(admin.ModelAdmin):
    model = models.Part
    list_display = [field.name for field in model._meta.fields]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['part']
    list_filter = ['is_valid']


@admin.register(models.Skill)
class AbstractSkillAdmin(admin.ModelAdmin):
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
    inlines = [AppliedSkillInline]


@admin.register(models.AppliedSkill)
class SkillAdmin(admin.ModelAdmin):
    model = models.AppliedSkill
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
