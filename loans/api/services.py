import requests


# Class to get loan approval from Moni's API
class LoanApproval():
    url = 'https://api.moni.com.ar/api/v4/scoring/pre-score/'
    credential = 'ZGpzOTAzaWZuc2Zpb25kZnNubm5u'
    headers = {'credential': credential}

    def get_loan_approval(self, dni):
        # url + dni
        final_url = self.url + str(dni)
        request = requests.get(final_url, headers=self.headers)
        if request.json()['status'] == 'approve':
            # Loan approved
            return True
        elif request.json()['status'] == 'rejected':
            # Loan rejected
            return False
        else:
            # The status value is 'error'
            return 'error'
