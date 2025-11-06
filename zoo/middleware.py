from django.utils.deprecation import MiddlewareMixin
from zoo.models import Animal

class AnimalViewCounterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__name__ == 'animal_detail':
            animal_id = view_kwargs.get('pk')
            if animal_id:
                try:
                    animal = Animal.objects.get(pk=animal_id)
                    animal.view_count = getattr(animal, 'view_count', 0) + 1
                    animal.save(update_fields=['view_count'])
                except Animal.DoesNotExist:
                    pass
        return None
