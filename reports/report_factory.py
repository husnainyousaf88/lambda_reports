from reports.riders_fill_report.fill_rate_report import get_rider_fill_rate as fill_rate_report
from reports.riders_salary_report.rider_salary_report import get_rider_salary as rider_salary
from reports.riders_receivable_report.rider_receivable_report import get_rider_receivables as rider_receivables
from reports.riders_cash_collection.rider_cash_collection import rider_cash_collection as cash_collection
from reports.riders_status_change_report.riders_status_change_report import rider_states as rider_status
from reports.riders_covid_19_sops.rider_covid_sops import covid_19_sops as sops_report
from reports.riders_loyalty_report.loyalty_report import rider_loyalty as loyalty_report
from reports.riders_shift_report.shift_report import rider_shifts as shift_report
from reports.riders_app_time_summary.rider_app_time_summary import rider_app_time_summary as app_time_summary
from reports.riders_insurance_report.insurance_report import rider_insurance as riders_insurance
from reports.riders_on_time_rate_report.on_time_rate import on_time_rate as rider_on_time
from reports.riders_settlement_request.settlement_report import settlement_requests as rider_settlement
from reports.riders_detail_report.detail_report import rider_details as rider_detail
from reports.rider_force_deliverable_orders.force_delivery_orders import force_deliverable_orders as force_order


ReportsLookup = {
    1: rider_receivables,
    2: app_time_summary,
    3: force_order,
    4: rider_salary,
    5: cash_collection,
    6: sops_report,
    7: rider_settlement,
    8: rider_on_time,
    9: fill_rate_report,
    10: rider_detail,
    11: shift_report,
    12: rider_status,
    13: loyalty_report,
    14: riders_insurance
 }


class ReportFactory:
    """
    Main Reports Factory Class...
    """

    def __init__(self, start_date, end_date, email, report_type, wallet_type=1):
        self.start_date = start_date
        self.end_date = end_date
        self.email = email
        self.report_type = report_type
        self.wallet_type = wallet_type

    def generate_report(self):
        """
        Get Rider Shifts Details Between Given Date Range
        Parameters
        ----------
        Returns
        -------
        None:
        """
        current_report = ReportsLookup[self.report_type]
        current_report(self.start_date, self.end_date, self.email, self.wallet_type)
