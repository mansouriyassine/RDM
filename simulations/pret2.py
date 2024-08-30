import numpy as np

def calculate_monthly_payment(principal, annual_rate, loan_term_years):
    """Calculate the monthly mortgage payment."""
    monthly_rate = annual_rate / 12
    num_payments = loan_term_years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return monthly_payment

def simulate_repayment(principal, annual_rate, loan_term_years, monthly_income, monthly_expenses):
    """Simulate the repayment period based on monthly income and expenses."""
    monthly_payment = calculate_monthly_payment(principal, annual_rate, loan_term_years)
    remaining_loan = principal
    months_passed = 0
    total_months = 0
    times_of_repurchase = 0
    
    while remaining_loan > 0:
        net_income = monthly_income - monthly_payment - monthly_expenses
        months_passed += 1
        total_months += 1

        if net_income > 0:
            remaining_loan -= net_income
            times_of_repurchase += 1
        
        if remaining_loan > 0:
            remaining_term_months = loan_term_years * 12 - months_passed
            monthly_payment = remaining_loan * (annual_rate / 12 * (1 + annual_rate / 12) ** remaining_term_months) / ((1 + annual_rate / 12) ** remaining_term_months - 1)
    
    return total_months, times_of_repurchase

def find_optimal_loan_option(options, monthly_income, monthly_expenses):
    """Find the optimal loan option based on the shortest repayment period."""
    optimal_option = None
    shortest_repayment_period = float('inf')
    
    for option in options:
        principal, annual_rate, loan_term_years = option
        total_months, _ = simulate_repayment(principal, annual_rate, loan_term_years, monthly_income, monthly_expenses)
        
        if total_months < shortest_repayment_period:
            shortest_repayment_period = total_months
            optimal_option = option
    
    return optimal_option, shortest_repayment_period

# User inputs for different loan options
loan_options = [
    (1000000, 4.5 / 100, 15),
    (1000000, 3.8 / 100, 20),
    (1000000, 5.0 / 100, 10),
    # Add more options if needed
]

# User inputs for monthly income and expenses
monthly_income = 25000
monthly_expenses = 4300

optimal_option, optimal_period = find_optimal_loan_option(loan_options, monthly_income, monthly_expenses)

print(f"La meilleure option de crédit est: Principal: {optimal_option[0]} MAD, Taux d'intérêt annuel: {optimal_option[1] * 100}%, Durée: {optimal_option[2]} ans.")
print(f"Durée de remboursement estimée : {optimal_period} mois (environ {optimal_period // 12} ans et {optimal_period % 12} mois).")