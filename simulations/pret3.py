import numpy as np

def calculate_monthly_payment(principal, annual_rate, loan_term_years):
    """Calculate the monthly mortgage payment."""
    monthly_rate = annual_rate / 12
    num_payments = loan_term_years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return monthly_payment

def simulate_repayment(principal, annual_rate, loan_term_years, monthly_income, monthly_expenses, savings_rate_annual):
    """Simulate the repayment period with savings account interest and annual partial repayments."""
    monthly_payment = calculate_monthly_payment(principal, annual_rate, loan_term_years)
    remaining_loan = principal
    months_passed = 0
    savings_balance = 0
    savings_rate_monthly = savings_rate_annual / 12
    total_months = 0
    times_of_repurchase = 0
    optimal_repurchase_moments = []

    while remaining_loan > 0:
        net_income = monthly_income - monthly_payment - monthly_expenses
        savings_balance += net_income  # Add net income to savings account
        
        # Apply savings interest
        savings_balance *= (1 + savings_rate_monthly)

        # Increment the months passed and total months
        months_passed += 1
        total_months += 1

        # Check if it's time for a repurchase (once a year)
        if months_passed % 12 == 0 and savings_balance > 0:
            # Repurchase part of the loan
            remaining_loan -= savings_balance
            optimal_repurchase_moments.append((months_passed, savings_balance, remaining_loan))
            savings_balance = 0  # Reset savings after repurchase
            times_of_repurchase += 1

            # Recalculate monthly payment based on new remaining loan balance
            if remaining_loan > 0:
                remaining_term_months = loan_term_years * 12 - months_passed
                monthly_payment = calculate_monthly_payment(remaining_loan, annual_rate, remaining_term_months / 12)
        
    return total_months, times_of_repurchase, optimal_repurchase_moments

def find_optimal_loan_option(options, monthly_income, monthly_expenses, savings_rate_annual):
    """Find the optimal loan option based on the shortest repayment period."""
    optimal_option = None
    shortest_repayment_period = float('inf')
    optimal_repurchase_moments = []

    for option in options:
        principal, annual_rate, loan_term_years = option
        total_months, times_of_repurchase, repurchase_moments = simulate_repayment(
            principal, annual_rate, loan_term_years, monthly_income, monthly_expenses, savings_rate_annual
        )
        
        if total_months < shortest_repayment_period:
            shortest_repayment_period = total_months
            optimal_option = option
            optimal_repurchase_moments = repurchase_moments
    
    return optimal_option, shortest_repayment_period, optimal_repurchase_moments

# Collecting user inputs
loan_options = []

print("Entrez les options de crédit. Entrez 'stop' pour terminer la saisie.")
while True:
    try:
        principal = input("Entrez le montant du prêt (MAD) ou 'stop' pour finir: ")
        if principal.lower() == 'stop':
            break
        principal = float(principal)
        annual_rate = float(input("Entrez le taux d'intérêt annuel (%) : ")) / 100
        loan_term_years = int(input("Entrez la durée du prêt (en années) : "))
        loan_options.append((principal, annual_rate, loan_term_years))
    except ValueError:
        print("Veuillez entrer une valeur valide.")

if loan_options:
    monthly_income = float(input("Entrez le revenu mensuel (MAD) : "))
    monthly_expenses = float(input("Entrez les charges mensuelles (MAD) : "))
    savings_rate_annual = float(input("Entrez le taux d'intérêt annuel du compte d'épargne (%) : ")) / 100

    optimal_option, optimal_period, optimal_repurchase_moments = find_optimal_loan_option(
        loan_options, monthly_income, monthly_expenses, savings_rate_annual
    )

    print(f"\nLa meilleure option de crédit est: Principal: {optimal_option[0]:,.2f} MAD, Taux d'intérêt annuel: {optimal_option[1] * 100:.2f}%, Durée: {optimal_option[2]} ans.")
    print(f"Durée de remboursement estimée : {optimal_period} mois (environ {optimal_period // 12} ans et {optimal_period % 12} mois).")
    
    print("\nMoments optimaux pour les rachats partiels (annuels) :")
    for moment in optimal_repurchase_moments:
        print(f" - Après {moment[0]} mois : Rachat de {moment[1]:,.2f} MAD, Nouveau solde restant du prêt : {moment[2]:,.2f} MAD")

else:
    print("Aucune option de crédit n'a été saisie.")