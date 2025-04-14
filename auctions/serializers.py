from rest_framework import serializers
from django.utils import timezone
from .models import Category, Auction, Bid
from drf_spectacular.utils import extend_schema_field


class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True
    )
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = "__all__"

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate_closing_date(self, value):
        if value <= timezone.now() + timezone.timedelta(days=15):
            raise serializers.ValidationError(
                "Closing date must be greater than now + 15 days."
            )
        return value


class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True
    )
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = "__all__"

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate_closing_date(self, value):
        if value <= timezone.now() + timezone.timedelta(days=15):
            raise serializers.ValidationError(
                "Closing date must be greater than now + 15 days."
            )
        return value


class BidListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True
    )

    class Meta:
        model = Bid
        fields = "__all__"

    def validate(self, data):
        auction = data.get("auction")
        price = data.get("price")

        if auction.closing_date <= timezone.now():
            raise serializers.ValidationError(
                "La subasta está cerrada. No se puede pujar."
            )

        highest_bid = Bid.objects.filter(auction=auction).order_by("-price").first()
        if highest_bid and price <= highest_bid.price:
            raise serializers.ValidationError(
                f"La puja debe ser mayor que la anterior ({highest_bid.price} €)."
            )

        return data


class BidDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True
    )

    class Meta:
        model = Bid
        fields = "__all__"
