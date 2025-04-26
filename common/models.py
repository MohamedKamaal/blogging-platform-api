from django.db import models
import uuid


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating 'created' and 'updated' fields,
    along with UUID and auto-incrementing primary key fields.
    
    Attributes:
        pkid (BigAutoField): An auto-incrementing primary key field.
        id (UUIDField): A unique identifier field with UUID format.
        created (DateTimeField): A field that automatically records creation date/time.
        updated (DateTimeField): A field that automatically records last update date/time.
    """
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for the TimeStampedModel.
        
        Attributes:
            abstract (bool): Indicates this is an abstract base class (won't create database table).
            ordering (list): Default ordering for queries ('-created' then '-updated').
        """
        abstract = True
        ordering = ['-created', '-updated']