from django.contrib import admin

# Register your models here.
# Register your models here.

from graphqlendpoint.models import Agent,Event, Call, Transfer,LoggedInUser, ActiveCalls
        
class AgentAdmin(admin.ModelAdmin):

    list_display = ('ext', 'firstname', 'lastname', 'phone_login', 'phone_state', 'phone_active', 'active', 'current_call')


class CallAdmin(admin.ModelAdmin):
    list_display = ('ucid', 'state', 'isContactCenterCall', 'history', 'end', 'origin')
    list_filter = ('end', 'state','current_agent')

class EventAdmin(admin.ModelAdmin):
    list_display = ('ot_id', 'applicant', 'ticket')
    list_filter = ('creationdate', 'responsible')
			


admin.site.register(Call, CallAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Transfer)
admin.site.register(LoggedInUser)
admin.site.register(ActiveCalls)