from datetime import date
from django.db.models import Sum
from .models import CashIn, CashOut, DailyRecord


def generate_daily_records():
    today = date.today()

    # Get or create the daily record for the current date
    daily_record, created = DailyRecord.objects.get_or_create(date=today)

    # Calculate the total cash-in and cash-out amounts for the current date
    cash_in_total = CashIn.objects.filter(date_added__date=today).aggregate(total=Sum('cash_in'))['total'] or 0
    cash_out_total = CashOut.objects.filter(date_added__date=today).aggregate(total=Sum('cash_out'))['total'] or 0

    # Update the cash-in and cash-out totals of the daily record
    daily_record.cash_in_total = cash_in_total
    daily_record.cash_out_total = cash_out_total
    daily_record.save()

    return daily_record

