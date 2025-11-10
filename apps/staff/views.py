# C:\Users\Adeyanju Joshua\Desktop\lexy sofware\wj_professional web\wj_professionals\apps\staff\views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from .models import Staff, Department
from apps.core.models import Company

class TeamListView(ListView):
    model = Staff
    template_name = 'staff/team.html'
    context_object_name = 'team_members'
    
    def get_queryset(self):
        queryset = Staff.objects.filter(is_public=True, is_active=True)
    
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(position__icontains=search_query) |
                Q(department__name__icontains=search_query) |
                Q(specializations__icontains=search_query)
            )
        
        return queryset.order_by('order', 'user__first_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.first()
        context['departments'] = Department.objects.filter(
            is_active=True,
            staff__is_active=True,
            staff__is_public=True
        ).distinct().annotate(
            staff_count=Count('staff', filter=Q(staff__is_active=True, staff__is_public=True))
        ).order_by('order', 'name')
        context['leadership'] = Staff.objects.filter(
            position__in=['managing_partner', 'senior_partner', 'partner'],
            is_public=True,
            is_active=True
        ).order_by('order', 'user__first_name')
        context['senior_staff'] = Staff.objects.filter(
            position__in=['senior_manager', 'manager'],
            is_public=True,
            is_active=True
        ).order_by('order', 'user__first_name')
        context['associates'] = Staff.objects.filter(
            position__in=['senior_associate', 'associate', 'junior_associate'],
            is_public=True,
            is_active=True
        ).order_by('order', 'user__first_name')
        context['team_stats'] = {
            'total_members': Staff.objects.filter(is_active=True, is_public=True).count(),
            'qualified_professionals': Staff.objects.filter(
                is_active=True, 
                is_public=True,
                position__in=['managing_partner', 'senior_partner', 'partner', 'senior_manager', 'manager']
            ).count(),
            'years_combined_experience': sum([
                staff.years_experience for staff in Staff.objects.filter(is_active=True, is_public=True)
            ]),
            'departments': Department.objects.filter(is_active=True).count()
        }
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_department'] = self.request.GET.get('department')
        return context

class StaffDetailView(DetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff_member'
    
    def get_queryset(self):
        return Staff.objects.filter(is_public=True, is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.first()
        context['department_colleagues'] = Staff.objects.filter(
            department=self.object.department,
            is_public=True,
            is_active=True
        ).exclude(id=self.object.id)[:3]
        return context

def department_view(request, department_id):
    """View for specific department"""
    department = get_object_or_404(Department, id=department_id, is_active=True)
    staff_members = Staff.objects.filter(
        department=department,
        is_public=True,
        is_active=True
    ).order_by('order', 'user__first_name')
    company = Company.objects.first()
    departments = Department.objects.filter(is_active=True)
    context = {
        'company': company,
        'department': department,
        'staff_members': staff_members,
        'departments': departments,
        'selected_department': department.id,
        'head_of_department': department.head_of_department,
        'team_stats': {
            'total_members': staff_members.count(),
            'senior_members': staff_members.filter(
                position__in=['managing_partner', 'senior_partner', 'partner', 'senior_manager', 'manager']
            ).count(),
        }
        
    }
    return render(request, 'staff/team.html', context)
