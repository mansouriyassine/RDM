def calculate_monthly_payment(principal, annual_rate, loan_term_years):
    """Calculer le paiement hypothécaire mensuel."""
    monthly_rate = annual_rate / 12
    num_payments = loan_term_years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return monthly_payment

def simulate_full_repayment(principal, annual_rate, loan_term_years, monthly_income, monthly_expenses, savings_rate_annual):
    """Simuler la période de remboursement avec intérêt du compte d'épargne et rachat total à la fin."""
    monthly_payment = calculate_monthly_payment(principal, annual_rate, loan_term_years)
    remaining_loan = principal
    months_passed = 0
    savings_balance = 0
    savings_rate_monthly = savings_rate_annual / 12
    total_months = 0

    while savings_balance < remaining_loan:
        # Calculer le revenu net après paiement des mensualités et des charges
        net_income = monthly_income - monthly_payment - monthly_expenses
        savings_balance += net_income  # Ajouter le revenu net au compte d'épargne

        # Appliquer les intérêts d'épargne
        savings_balance *= (1 + savings_rate_monthly)

        # Incrémenter le nombre de mois écoulés et le total des mois
        months_passed += 1
        total_months += 1

        # Réduire le solde restant du prêt chaque mois
        remaining_loan -= (monthly_payment - (remaining_loan * (annual_rate / 12)))
    
    return total_months, savings_balance

def find_optimal_loan_option(options, monthly_income, monthly_expenses, savings_rate_annual):
    """Trouver l'option de prêt optimale en fonction de la période de remboursement la plus courte pour un rachat total."""
    optimal_option = None
    shortest_repayment_period = float('inf')

    for option in options:
        principal, annual_rate, loan_term_years = option
        total_months, final_savings = simulate_full_repayment(
            principal, annual_rate, loan_term_years, monthly_income, monthly_expenses, savings_rate_annual
        )
        
        if total_months < shortest_repayment_period:
            shortest_repayment_period = total_months
            optimal_option = option
    
    return optimal_option, shortest_repayment_period

# Collecte des entrées utilisateur
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

    optimal_option, optimal_period = find_optimal_loan_option(
        loan_options, monthly_income, monthly_expenses, savings_rate_annual
    )

    print(f"\nLa meilleure option de crédit est: Principal: {optimal_option[0]:,.2f} MAD, Taux d'intérêt annuel: {optimal_option[1] * 100:.2f}%, Durée: {optimal_option[2]} ans.")
    print(f"Durée de remboursement estimée avec rachat total : {optimal_period} mois (environ {optimal_period // 12} ans et {optimal_period % 12} mois).")

else:
    print("Aucune option de crédit n'a été saisie.")