#PS1-2a.py

balance = float(raw_input("Enter balance: $"))
AnnualInterest = float(raw_input("Enter annual interest rate as decimal: $"))

MonthlyInterest = float(AnnualInterest / 12.0)

MinMonthlyPay = 0
IsFound = False

while(IsFound == False):
	MinMonthlyPay += 10
	tryBalance = balance
	for i in range(1, 13):
		tryBalance = tryBalance * (1 + MonthlyInterest) - MinMonthlyPay
		if(tryBalance <= 0.0):
			IsFound = True
			break


print "RESULT:"
print "Monthly payment to pay off debt in 1 year:", str(MinMonthlyPay)
print "Number of Month needed:", str(i)
print "Balance:", str(round(tryBalance, 2))


