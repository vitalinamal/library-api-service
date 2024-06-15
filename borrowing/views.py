from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from borrowing.models import Borrowing, Book
from borrowing.serializers import BorrowingSerializer


class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id is not None:
            queryset = queryset.filter(user=user_id)

        if is_active is not None:
            is_active = is_active.lower() in ("true", "1")
            if is_active:
                queryset = queryset.filter(actual_return_date__isnull=True)
            else:
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        book.inventory -= 1
        book.save()

        return super().create(request, *args, **kwargs)


class BorrowingDetailAPIView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


@api_view(["POST"])
def return_borrowing(request: Request, pk: int) -> Response:
    """
    Handle the return of a borrowed book.
    """
    try:
        borrowing = Borrowing.objects.get(pk=pk)
    except Borrowing.DoesNotExist:
        return Response(
            {"error": "Borrowing not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if borrowing.actual_return_date is not None:
        return Response(
            {"error": "Borrowing already returned"},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

    return Response(
        {"status": "Return date set and inventory updated"},
        status=status.HTTP_200_OK
    )
