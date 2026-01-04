from django.db import models

# Create your models here.


class PandharRaste(models.Model):
    """
    Model for पांढर रस्ते scheme data.
    Data is aggregated taluka-wise (one row per taluka).
    """
    taluka = models.CharField(max_length=100, verbose_name="तालुका")
    geo_tag_roads = models.IntegerField(default=0, verbose_name="Geo-tag केलेले रस्ते")
    geo_tag_length_km = models.FloatField(default=0.0, verbose_name="अतिक्रमित व Geo-tag रस्त्यांची लांबी (कि.मी.)")
    cleared_roads = models.IntegerField(default=0, verbose_name="अतिक्रमण काढलेले रस्ते")
    cleared_length_km = models.FloatField(default=0.0, verbose_name="अतिक्रमण काढलेली लांबी (कि.मी.)")
    farmers_benefited = models.IntegerField(default=0, verbose_name="लाभार्थी शेतकरी")
    
    class Meta:
        verbose_name = "पांढर रस्ते"
        verbose_name_plural = "पांढर रस्ते"
        ordering = ['taluka']
    
    def __str__(self):
        return f"{self.taluka}"


class EHaqq(models.Model):
    """
    Model for ई-हक्क scheme data.
    Data is aggregated taluka-wise (one row per taluka).
    """
    taluka = models.CharField(max_length=100, unique=True, verbose_name="तालुका")
    
    # Application counts
    total_applications = models.IntegerField(default=0, verbose_name="एकूण अर्ज")
    approved_applications = models.IntegerField(default=0, verbose_name="स्वीकारित अर्ज")
    rejected_applications = models.IntegerField(default=0, verbose_name="अस्वीकारित अर्ज")
    pending_applications = models.IntegerField(default=0, verbose_name="प्रलंबित अर्ज")
    
    # Application percentages
    approved_percentage = models.FloatField(default=0.0, verbose_name="स्वीकारित अर्ज (%)")
    rejected_percentage = models.FloatField(default=0.0, verbose_name="अस्वीकारित अर्ज (%)")
    pending_percentage = models.FloatField(default=0.0, verbose_name="प्रलंबित अर्ज (%)")
    
    # Period work count (28.10.2025 ते 03.11.2025 कालावधीतील कामकाज)
    period_work_count = models.IntegerField(default=0, verbose_name="कालावधीतील कामकाज")
    
    class Meta:
        verbose_name = "ई-हक्क"
        verbose_name_plural = "ई-हक्क"
        ordering = ['taluka']
    
    def __str__(self):
        return f"{self.taluka}"


class AgriStack(models.Model):
    """
    Model for ॲग्रीस्टॅक scheme data.
    Data is aggregated taluka-wise (one row per taluka).
    """
    taluka = models.CharField(max_length=100, unique=True, verbose_name="तालुका")
    
    # Village and farmer counts
    total_villages = models.IntegerField(default=0, verbose_name="एकूण गावे")
    total_farmers = models.IntegerField(default=0, verbose_name="एकूण शेतकरी")
    
    # Farmer ID creation status
    farmers_with_id_created = models.IntegerField(default=0, verbose_name="फार्मर आयडी तयार केलेले शेतकरी")
    farmers_pending_id = models.IntegerField(default=0, verbose_name="फार्मर आयडी तयार करण्यावर शिल्लक शेतकरी")
    
    # Completion percentage
    completion_percentage = models.FloatField(default=0.0, verbose_name="टक्केवारी")
    
    class Meta:
        verbose_name = "ॲग्रीस्टॅक"
        verbose_name_plural = "ॲग्रीस्टॅक"
        ordering = ['taluka']
    
    def __str__(self):
        return f"{self.taluka}"