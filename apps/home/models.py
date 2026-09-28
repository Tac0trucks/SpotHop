from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# ==========================================
# 1. USERS
# ==========================================
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password_hash = models.CharField(max_length=128)
    full_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    preferred_noise_level = models.CharField(max_length=20, blank=True, null=True)
    preferred_outlet_density = models.CharField(max_length=20, blank=True, null=True)
    min_wifi_speed_mbps = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


# ==========================================
# 2. STUDY SPOTS
# ==========================================
class StudySpot(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    price_tier = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        db_table = "study_spots"
        verbose_name = "Study Spot"
        verbose_name_plural = "Study Spots"

    def __str__(self):
        return self.name


# ==========================================
# 3. SPOT AMENITIES (1:1 with StudySpot)
# ==========================================
class SpotAmenity(models.Model):
    spot = models.OneToOneField(
        StudySpot,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="amenities",
        db_column="spot_id",
    )
    avg_wifi_speed_mbps = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )
    outlet_density = models.CharField(max_length=20, blank=True, null=True)
    predominant_noise = models.CharField(max_length=20, blank=True, null=True)
    last_recalculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "spot_amenities"
        verbose_name = "Spot Amenity"
        verbose_name_plural = "Spot Amenities"

    def __str__(self):
        return f"Amenities for {self.spot.name}"


# ==========================================
# 4. REVIEWS (1:M from User & StudySpot)
# ==========================================
class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    spot = models.ForeignKey(
        StudySpot,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="spot_id",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_column="user_id",
    )
    overall_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    outlet_rating = models.CharField(max_length=20, blank=True, null=True)
    noise_level = models.CharField(max_length=20, blank=True, null=True)
    download_speed_mbps = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )
    upload_speed_mbps = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )
    review_text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "reviews"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.user.username} on {self.spot.name}"


# ==========================================
# 5. CHECK INS (1:M from User & StudySpot)
# ==========================================
class CheckIn(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="check_ins",
        db_column="user_id",
    )
    spot = models.ForeignKey(
        StudySpot,
        on_delete=models.CASCADE,
        related_name="check_ins",
        db_column="spot_id",
    )
    checked_in_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "check_ins"
        verbose_name = "Check In"
        verbose_name_plural = "Check Ins"

    def __str__(self):
        return f"{self.user.username} at {self.spot.name}"


# ==========================================
# 6. SAVED SPOTS (Junction Table)
# ==========================================
class SavedSpot(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_spots",
        db_column="user_id",
    )
    spot = models.ForeignKey(
        StudySpot,
        on_delete=models.CASCADE,
        related_name="saved_by_users",
        db_column="spot_id",
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "saved_spots"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "spot"], name="unique_user_saved_spot"
            )
        ]
        verbose_name = "Saved Spot"
        verbose_name_plural = "Saved Spots"

    def __str__(self):
        return f"{self.user.username} saved {self.spot.name}"