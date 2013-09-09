#PS1-2b.py

balance = float(raw_input("Enter balance: $"))
AnnualInterest = float(raw_input("Enter annual interest rate as decimal: $"))

MonthlyInterest = float(AnnualInterest / 12.0)

lowerBound = balance / 12.0
upperBound = (balance * (1 + MonthlyInterest)**12.0) / 12.0


MinMonthlyPay = 0
Precise = -0.5

while(True):
	MinMonthlyPay = round((lowerBound + upperBound) / 2.0, 2)
	tryBalance = balance
	for i in range(1, 13):
		tryBalance = tryBalance * (1 + MonthlyInterest) - MinMonthlyPay

	if tryBalance <= 0.0 and tryBalance > Precise:
		break
	elif tryBalance > 0.0:
		lowerBound = MinMonthlyPay
	else:
		upperBound = MinMonthlyPay

print "RESULT:"
print "Monthly payment to pay off debt in 1 year:", str(MinMonthlyPay)
print "Number of Month needed: 12"
print "Balance:", str(round(tryBalance, 2))
