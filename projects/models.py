from django.db import models
import uuid
from users.models import Profile




class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # null = True (Can be blank in DB) black=True (Allwed to submit a form with this value empty)
    description = models.TextField(null=True, blank=True)

    # IMAGE FILED THAT WILL SHOWCASE UPLOADED IMAGES
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")

    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # MANY TO MANY RELATIONSHIP
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ration = models.IntegerField(default=0, null=True, blank=True)
    # Generate a timestamp once this model was created
    created = models.DateTimeField(auto_now_add=True)
    # Django creates automatically INT IDs
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    
    def __str__(self):
        """
        RETURNS PROJECT TITLE (NAME) IN THE ADMIN PANEL.
        """
        return self.title
    

    class Meta:
        # The one with more votes will rank first
        ordering = ['-vote_ration', '-vote_total', 'title']


    # imageURL property can be accessed as an attribute in HTML tags
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url


    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    
    @property
    def getVoteCount(self):
        # Getting all reviews
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        # How many items are in the queryset
        totalVotes = reviews.count()

        ratio = (upVotes/ totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ration = ratio
        self.save()


class Review(models.Model):
    # DROPDOWN MENU
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body =  models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    # Django creates automatically INT IDs
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        """
        Model Meta is basically the inner class of your model class.
        Model Meta is basically used to change the behavior of your model fields like changing order options,
        verbose_name and lot of other options. It's completely optional to add Meta class in your model.
        """
        # EACH OWNER CAN ONLY LEAVE ONE REVIEW PER PROJECT
        unique_together = [['owner', 'project']]


    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    # Django creates automatically INT IDs
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.name
