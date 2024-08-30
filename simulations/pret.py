def calculate_mortgage(amount, rate, years):
        monthly_rate = rate / 100 / 12
            num_payments = years * 12
                monthly_payment = (amount * monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
                    total_payment = monthly_payment * num_payments
                        return monthly_payment, total_payment

                    def calculate_partial_repayments(amount, rate, years):
                            base_monthly_payment, base_total_payment = calculate_mortgage(amount, rate, years)
                                partial_repayments = []
                                    for percent in [0.1, 0.2, 0.3]:
                                                repayment_amount = amount * percent
                                                        new_amount = amount - repayment_amount
                                                                new_monthly_payment, _ = calculate_mortgage(new_amount, rate, years)
                                                                        savings = base_monthly_payment - new_monthly_payment
                                                                                partial_repayments.append({
                                                                                                "percent": percent * 100,
                                                                                                            "repayment_amount": repayment_amount,
                                                                                                                        "new_monthly_payment": new_monthly_payment,
                                                                                                                                    "savings": savings
                                                                                                                                            })
                                                                                    return base_monthly_payment, base_total_payment, partial_repayments

                                                                                def display_results(house_price, interest_rate):
                                                                                        durations = [10, 15, 25]
                                                                                            for duration in durations:
                                                                                                        base_monthly_payment, base_total_payment, partial_repayments = calculate_partial_repayments(house_price, interest_rate, duration)
                                                                                                                print(f"\nDurée: {duration} ans")
                                                                                                                        print(f"Mensualité de base: {base_monthly_payment:.2f} MAD")
                                                                                                                                print(f"Coût total: {base_total_payment:.2f} MAD")
                                                                                                                                        print("\nRachats partiels:")
                                                                                                                                                print(f"{'Pourcentage':<15}{'Montant':<15}{'Nouvelle mensualité':<20}{'Économie mensuelle':<20}")
                                                                                                                                                        for repayment in partial_repayments:
                                                                                                                                                                        print(f"{repayment['percent']}%{repayment['repayment_amount']:.2f} MAD{repayment['new_monthly_payment']:.2f} MAD{repayment['savings']:.2f} MAD")

                                                                                                                                                                        def main():
                                                                                                                                                                                house_price = float(input("Entrez le prix de la maison (MAD) : "))
                                                                                                                                                                                    interest_rate = float(input("Entrez le taux d'intérêt (%) : "))
                                                                                                                                                                                        display_results(house_price, interest_rate)

                                                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                                                main()
                                                                                                                                                        
