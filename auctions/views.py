from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from rest_framework import generics
from .models import Category, Auction, Bid, Comment, Rating
from .serializers import (
    CategoryListCreateSerializer,
    CategoryDetailSerializer,
    AuctionListCreateSerializer,
    AuctionDetailSerializer,
    BidListCreateSerializer,
    BidDetailSerializer,
    CommentListCreateSerializer, 
    CommentDetailSerializer,
    RatingListCreateSerializer,
    RatingDetailSerializer,
)
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin, IsAuthenticatedOrReadOnly, IsAdminOrReadOnly

class CategoryListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer


class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class AuctionListCreate(generics.ListCreateAPIView):
    serializer_class = AuctionListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Auction.objects.all()
        params = self.request.GET

        text = params.get("text")
        if text:
            queryset = queryset.filter(
                Q(title__icontains=text) | Q(description__icontains=text)
            )

        category = params.get("category")
        if category:
            queryset = queryset.filter(category__name__iexact=category)

        price_min = params.get("priceMin")
        price_max = params.get("priceMax")
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        auctioneer_name = params.get("auctioneer")
        if auctioneer_name:
            queryset = queryset.filter(auctioneer=auctioneer_name)
        

        return queryset


class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer


class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Bid.objects.filter(auction=self.kwargs["auction_id"])


class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidDetailSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return Bid.objects.filter(auction=self.kwargs["auction_id"])


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(auction=self.kwargs["auction_id"])


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return Comment.objects.filter(auction=self.kwargs["auction_id"])
    
class RatingListCreate(generics.ListCreateAPIView):
    serializer_class = RatingListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Rating.objects.filter(auction=self.kwargs["auction_id"])


class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingDetailSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return Rating.objects.filter(auction=self.kwargs["auction_id"])



class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)
