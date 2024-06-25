from decimal import Decimal

from borrowing.models import Borrowing

FINE_MULTIPLIER = 2


def calculate_total_price(borrowing: Borrowing) -> Decimal:
    """
    Calculate the total price for borrowing a book.
    """
    delta = borrowing.expected_return_date - borrowing.borrow_date
    days_borrowed = delta.days
    total_price = days_borrowed * borrowing.book.daily_fee
    return Decimal(total_price)


def calculate_fine(borrowing: Borrowing) -> Decimal:
    """
    Calculate the fine for overdue borrowing of a book.
    """
    days_overdue = (borrowing.actual_return_date
                    - borrowing.expected_return_date).days
    daily_fee = borrowing.book.daily_fee
    fine_amount = days_overdue * daily_fee * FINE_MULTIPLIER
    return Decimal(fine_amount)
