from django.contrib import admin

# Register your models here.
# Register your models here.

from graphqlendpoint.models import Agent,Event, Call, Transfer,LoggedInUser, ActiveCalls, Ticket, Category
        
class AgentAdmin(admin.ModelAdmin):

    list_display = ('ext', 'firstname', 'lastname', 'phone_login', 'phone_state', 'phone_active', 'active', 'current_call')

class CallAdmin(admin.ModelAdmin):
    list_display = ('ucid', 'state', 'isContactCenterCall', 'history', 'end', 'origin')
    list_filter = ('end', 'state','current_agent')

class EventAdmin(admin.ModelAdmin):
    list_display = ('ot_id', 'applicant', 'ticket')
    list_filter = ('creationdate', 'applicant')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'state')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'searchcode', 'ot_id')


admin.site.register(Category, CategoryAdmin)

admin.site.register(Call, CallAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Transfer)
admin.site.register(LoggedInUser)
admin.site.register(ActiveCalls)
admin.site.register(Ticket, TicketAdmin)