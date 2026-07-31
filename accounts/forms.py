from django import forms
from campuses.models import Campus, Department
from .models import User


class DepartmentSelectWithCampus(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            try:
                dept_id = value.value if hasattr(value, 'value') else value
                dept = Department.objects.select_related('campus').get(pk=dept_id)
                option['attrs']['data-campus'] = dept.campus_id
            except Department.DoesNotExist:
                pass
        return option


class UserAdminForm(forms.ModelForm):
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(), required=False,
        help_text="Pick a campus to filter the department list below.",
    )

    class Meta:
        model = User
        fields = '__all__'
        widgets = {'department': DepartmentSelectWithCampus}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.department_id:
            self.fields['campus'].initial = self.instance.department.campus_id
        self.fields['department'].queryset = Department.objects.select_related('campus').order_by('campus__name', 'name')

    class Media:
        js = ('accounts/campus_department_filter.js',)