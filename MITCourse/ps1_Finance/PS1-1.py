#PS1-1.py

balance = float(raw_input("Enter Balance:"))
AnnualInterest = float(raw_input("Enter annual interest rate as decimal:"))
MinMonthPayRate = float(raw_input("Enter minimum monthly payment rate as decimal:"))

MonthInterest = float(AnnualInterest / 12.0)

TotalPaid = 0

for month in range(1,13):
	print "Month", str(month)

	MinMonthPay = float(balance * MinMonthPayRate)
	print "Minimum monthly payment: $", str(round(MinMonthPay, 2))

	InterestPaid = float(balance * MonthInterest)
	PrincipalPaid = float(MinMonthPay - InterestPaid)
	print "Principle paid:$", str(round(PrincipalPaid, 2))

	TotalPaid += MinMonthPay
	balance = balance - PrincipalPaid
	print "Remaining balance: $", str(round(balance, 2))

print "RESULT:"
print "Total amount paid:$", str(round(TotalPaid, 2))
print "Remaining balance:$", str(round(balance, 2))


	

