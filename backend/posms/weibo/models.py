# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:  
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comment(models.Model):
    title_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    to_user = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    comment_text = models.TextField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class PeopleNews(models.Model):
    title_id = models.BigIntegerField(primary_key=True)
    originalname = models.CharField(db_column='originalName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_news'


class Title(models.Model):
    title_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    openurl = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    iscrawled = models.IntegerField(db_column='isCrawled', blank=True, null=True)  # Field name made lowercase.
    uid = models.CharField(max_length=255, blank=True, null=True)
    uname = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    read_num = models.IntegerField(blank=True, null=True)
    forward_num = models.IntegerField(blank=True, null=True)
    comment_num = models.IntegerField(blank=True, null=True)
    like_num = models.IntegerField(blank=True, null=True)
    comment_id = models.CharField(max_length=255, blank=True, null=True)
    comment_times = models.IntegerField(blank=True, null=True)
    sentiment = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'title'


class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    uname = models.CharField(max_length=255, blank=True, null=True)
    follow_count = models.CharField(max_length=255, blank=True, null=True)
    followers_count = models.CharField(max_length=255, blank=True, null=True)
    statuses_count = models.CharField(max_length=255, blank=True, null=True)
    verified = models.CharField(max_length=255, blank=True, null=True)
    fans_list_id = models.CharField(max_length=255, blank=True, null=True)
    more_list_id = models.CharField(max_length=255, blank=True, null=True)
    activefans_count = models.CharField(db_column='activeFans_count', max_length=255, blank=True, null=True)  # Field name made lowercase.
    verifiedfans_count = models.CharField(db_column='verifiedFans_count', max_length=255, blank=True, null=True)  # Field name made lowercase.
    original_count = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'


class Wangyiedu(models.Model):
    title_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wangyiedu'