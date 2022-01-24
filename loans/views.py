from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

# Import Loan model
from .models import Loan
# Import Loan form
from .forms import LoanForm


# Home template
class Home(TemplateView):
    template_name = 'index.html'


# View to create new loan
class CreateLoan(SuccessMessageMixin, CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loans/create_loan.html'
    success_url = reverse_lazy('loans:loan_result')
    success_message = "%(result)s"

    def get_success_message(self, cleaned_data):
        # Define success message to show approved or not in loan_result
        if self.object.status:
            return 'approved'
        else:
            return 'rejected'


# View to logical delete loans
class DeleteLoan(DeleteView):
    model = Loan
    success_url = reverse_lazy('loans:list_loan')

    # Override POST method to do logic delete
    def post(self, request, pk, *args, **kwargs):
        object = Loan.objects.get(id=pk)
        object.state = False
        object.save()
        return redirect('loans:list_loan')


# Template that shows the result of the loan application
class ResultApproved(TemplateView):
    template_name = 'loans/loan_result.html'


# View to list loans
class ListLoan(ListView):
    template_name = 'loans/list_loans.html'
    context_object_name = 'loans'
    queryset = Loan.objects.filter(state=True)
