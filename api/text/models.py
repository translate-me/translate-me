from django.db import models
import json

CHOICES = (
    ('1', 'To translate'),
    ('2', 'Translating'),
    ('3', 'To review'),
    ('4', 'Reviewing'),
    ('5', 'To finish'),
    ('6', 'Finished')
)

""" Text."""


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, null=False, blank=False)
    category_description = models.CharField(max_length=200, null=False,
                                            blank=False)


class Text(models.Model):
    body = models.TextField(null=False, blank=False)
    total_fragments = models.IntegerField(default=0)
    fragments_done = models.IntegerField(default=0)
    fragments_revision = models.IntegerField(default=0)
    fragments_doing = models.IntegerField(default=0)
    context = models.CharField(max_length=200, null=False, blank=False)
    author = models.CharField(max_length=50, null=False, blank=False)
    language = models.IntegerField(null=False, blank=False)
    categories = models.ManyToManyField(Category)
    text_translate = models.TextField(null=True, blank=True)


""" Fragment."""


class Fragment(models.Model):
    text_id = models.ForeignKey(Text, on_delete=models.SET_NULL,
                                null=True)
    body = models.TextField(null=False, blank=False)
    price = models.FloatField(default=0)
    state = models.CharField(max_length=12, choices=CHOICES,
                             default='To translate', null=False, blank=False)
    total_reviews = models.IntegerField(default=0)
    fragment_translate = models.TextField(null=True, blank=True)
    
    
    observer_list = models.CharField(max_length=1000, null=True)


    def change_state(self, next_state):
        oberserver_author = ConcreteObserverAuthor()
        oberserver_translator = ConcreteObserverTranslator()
        oberserver_revisor = ConcreteObserverRevisor()

        

        list_observer = [oberserver_author, oberserver_revisor, oberserver_translator]
        for i in list_observer:
            if self.observer_list is None:
                print("Socorro Jesus")
                defined = json.dumps([i.observer_type])
                self.observer_list = defined
            else:
                print("Socorro Jah")
                defined = json.loads(self.observer_list)
                defined.append(i.observer_type)
                self.observer_list = json.dumps(defined)
            i.notify(self.pk, self.state, next_state)


        



    # observer_list = models.CharField(max_length=1000, null=True)

    # def attach_observer(self, observer):
    #     if self.observer_list == None:
    #         instanced_list = [observer]
    #     else:
    #         instanced_list = json.loads(self.observer_list)
    #         instanced_list.append(observer)
    #     self.observer_list = json.dumps(instanced_list)

    # def add_observers(self):
    #     oberserver_author = ConcreteObserverAuthor()
    #     oberserver_translator = ConcreteObserverTranslator()
    #     oberserver_revisor = ConcreteObserverRevisor()
    #     self.attach_observer(oberserver_author)
    #     self.attach_observer(oberserver_translator)
    #     self.attach_observer(oberserver_revisor)


""" Review."""


class Review(models.Model):
    fragment_id = models.ForeignKey(Fragment, on_delete=models.SET_NULL,
                                    null=True)
    review_username = models.CharField(max_length=50, null=False, blank=False)
    comment = models.TextField()
    approve = models.BooleanField(default=False)



""" Notification """

class Observer(models.Model):

    observer_type = models.CharField(max_length=50, default='Nada')

    def notify(self, fragment_id, previous_state, actual_state) -> None:
        pass

    class Meta:
        abstract = True


class ConcreteObserverAuthor(Observer):

    observer_type = "Author"

    def notify(self, ragment_id, previous_state, actual_state) -> Fragment:
        if (previous_state == 'To translate' and actual_state == 'Translating'):
            data = Fragment.objects.filter(id=2)
        else: 
            data = Fragment.objects.filter(id=3)  
        return data

class ConcreteObserverTranslator(Observer):
    
    observer_type = "Translator"

    def notify(self,  fragment_id, previous_state, actual_state) -> Fragment:
        if (previous_state == 'To translate' and actual_state == 'Translating'):
            data = Fragment.objects.filter(id=2)
        else: 
            data = Fragment.objects.filter(id=3)  
        return data

class ConcreteObserverRevisor(Observer):
    
    observer_type = "Revisor"

    def notify(self,  fragment_id, previous_state, actual_state) -> Fragment:
        if (previous_state == 'To translate' and actual_state == 'Translating'):
            data = Fragment.objects.filter(id=2)
        else: 
            data = Fragment.objects.filter(id=3)  
        return data


    

class Notification(models.Model):
    text_id = models.ForeignKey(Text, on_delete=models.SET_NULL,
                                null=True)
    target_username = models.CharField(max_length=50, null=False, blank=False)
    message = models.CharField(max_length=500, null=False, blank=False)
    is_seen = models.BooleanField(default=False)



# fragment = Fragment.objects.filter(id=fragment_id)
# text = Text.objects.filter(id=fragment.text_id)
# data = None

# class NotificationList(models.Model):
#     text_id = models.ForeignKey(Text, on_delete=models.SET_NULL,
#                                 null=True)
#     new_notifications = models.CharField(max_lenght=1000)
#     seen_notifications = models.CharField(max_lenght=1000)
    
#     def add_notification(self, notification_id):
#         if self.new_notifications == None
#             new_list = [notification_id]
#             self.new_notifications = json.dumps(new_list)
#         else 
#             notifications_list = json.loads(self.new_notifications)
#             notifications_list.append(notification_id)
#             self.new_notifications = json.dumps(notifications_list)
