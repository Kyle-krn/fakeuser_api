from rest_framework_csv.renderers import CSVRenderer
from . import utils

class UserCsvRender(CSVRenderer):
    def render(self, data, *args, **kwargs):
        self.header = utils.flatten(data['results'][0]).keys()
        data = [utils.flatten(i) for i in data['results']]
        return super(UserCsvRender, self).render(data, *args, **kwargs)