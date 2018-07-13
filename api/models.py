from django.db import models



# class Roles(models.Model):
#     title = models.CharField(max_length=255, blank=True, default='')
#     created = models.DateTimeField(auto_now_add=True)


# class Permissions(models.Model):
#     title = models.CharField(max_length=255, blank=True, default='')
#     key = models.DateTimeField(max_length=255, blank=True, default='')
#     created = models.DateTimeField(auto_now_add=True)


# class Role_permissions(models.Model):
#     role = models.ForeignKey('roles', related_name='role_permissions')
#     permission = models.ForeignKey('auth.User', related_name='role_permissions')
#     created = models.DateTimeField(auto_now_add=True)


# class tokens(models.Model):
#     user = models.ForeignKey('auth.User', related_name='tokens', on_delete=models.CASCADE)
#     token = models.TextField(default='')
#     role = models.ForeignKey('auth.User', related_name='role_permissions')
#     permission = models.TextField(default='')
#     expired = models.DateTimeField()
#     created = models.DateTimeField(auto_now_add=True)
