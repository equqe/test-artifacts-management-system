from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import ContentType

class Command(BaseCommand):
    help = 'Create test groups and assign permissions'

    def handle(self, *args, **kwargs):

        log_entry_ct = ContentType.objects.get(app_label='admin', model='logentry')
        group_ct = ContentType.objects.get(app_label='auth', model='group')
        permission_ct = ContentType.objects.get(app_label='auth', model='permission')
        content_type_ct = ContentType.objects.get(app_label='contenttypes', model='contenttype')
        bug_report_ct = ContentType.objects.get(app_label='main', model='bugreports')
        case_step_ct = ContentType.objects.get(app_label='main', model='casesteps')
        projects_ct = ContentType.objects.get(app_label='main', model='projects')
        test_case_ct = ContentType.objects.get(app_label='main', model='testcases')
        tester_ct = ContentType.objects.get(app_label='main', model='tester')
        test_set_ct = ContentType.objects.get(app_label='main', model='testset')
        session_ct = ContentType.objects.get(app_label='sessions', model='session')


        tester_permissions = [
            'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
            'add_group', 'change_group', 'delete_group', 'view_group',
            'add_permission', 'change_permission', 'delete_permission', 'view_permission',
            'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
            'add_bugreports', 'change_bugreports', 'view_bugreports',
            'add_casesteps', 'change_casesteps', 'delete_casesteps', 'view_casesteps',
            'view_projects',
            'add_testcases', 'change_testcases', 'delete_testcases', 'view_testcases',
            'add_tester', 'change_tester', 'view_tester',
            'add_testset', 'change_testset', 'view_testset',
            'add_session', 'change_session', 'delete_session', 'view_session',
        ]

        # Permissions for Senior Tester group
        senior_tester_permissions = [
            'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
            'add_group', 'change_group', 'delete_group', 'view_group',
            'add_permission', 'change_permission', 'delete_permission', 'view_permission',
            'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
            'add_bugreports', 'change_bugreports', 'delete_bugreports', 'view_bugreports',
            'add_casesteps', 'change_casesteps', 'delete_casesteps', 'view_casesteps',
            'add_projects', 'change_projects', 'delete_projects', 'view_projects',
            'add_testcases', 'change_testcases', 'delete_testcases', 'view_testcases',
            'add_tester', 'change_tester', 'delete_tester', 'view_tester',
            'add_testset', 'change_testset', 'view_testset',
            'add_session', 'change_session', 'delete_session', 'view_session',
        ]

        tester_group, _ = Group.objects.get_or_create(name='Тестировщик')
        senior_tester_group, _ = Group.objects.get_or_create(name='Главный тестировщик')
                
        for permission_name in tester_permissions:
            permission = Permission.objects.get(codename=permission_name)
            tester_group.permissions.add(permission)

        for permission_name in senior_tester_permissions:
            permission = Permission.objects.get(codename=permission_name)
            senior_tester_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Groups created and permissions assigned'))
