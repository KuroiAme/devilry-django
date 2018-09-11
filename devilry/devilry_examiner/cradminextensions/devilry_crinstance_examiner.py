from django_cradmin import crinstance


class BaseCrInstanceExaminer(crinstance.BaseCrAdminInstance):
    def add_extra_instance_variables_to_request(self, request):
        setattr(request, 'devilryrole', 'examiner')
