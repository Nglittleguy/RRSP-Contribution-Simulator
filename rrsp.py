import pandas as pd
import matplotlib.pyplot as plt
import math as m
import csv

# Variables:
starting_annual_income = 85000
annual_income_cap = 350000
promotion_amount_per_year = 1.05
rrsp_inv_growth_per_year = 0.12
self_inv_growth_per_year = [0.12, 0.15, 0.18, 0.25, 0.3]
company_rrsp_match_percent = 0.03
years = list(range(23, 41, 1))

# Tax Brackets:
fed_tax_rates = [0.14, 0.205, 0.26, 0.29, 0.33]
fed_tax_brackets = [0, 57375, 114750, 177882, 253414]

prov_tax_rates = [0.0505, 0.0915, 0.1116, 0.1216, 0.1316]
prov_tax_brackets = [0, 52886, 105775, 150000, 220000]

# RRSP Specific:
rrsp_annual_add = 0.18
rrsp_annual_add_max = 33810




def pay_taxes(income):
    tax = 0

    for i in range(0, len(fed_tax_brackets)):
        if income > fed_tax_brackets[i]:
            if i < len(fed_tax_brackets) - 1:
                applicable_amount = min(fed_tax_brackets[i+1], income)
            else:
                applicable_amount = income
            taxable_amount = applicable_amount - fed_tax_brackets[i]

            # print(f"At Fed bracket, above: ${fed_tax_brackets[i]} - {fed_tax_rates[i]*100}% | Paid: ${fed_tax_rates[i] * taxable_amount} on ${taxable_amount}")

            tax += fed_tax_rates[i] * taxable_amount

    for i in range(0, len(prov_tax_brackets)):
        if income > prov_tax_brackets[i]:
            if i < len(prov_tax_brackets) - 1:
                applicable_amount = min(prov_tax_brackets[i+1], income)
            else:
                applicable_amount = income
            taxable_amount = applicable_amount - prov_tax_brackets[i]

            # print(f"At Prov bracket, above: ${prov_tax_brackets[i]} - {prov_tax_rates[i]*100}% | Paid: ${prov_tax_rates[i] * taxable_amount} on ${taxable_amount}")
            tax += prov_tax_rates[i] * taxable_amount
    return tax

def pay_taxes_and_stocks(income, stocks):
    tax = 0
    stock_tax_bracket = 0

    for i in range(0, len(fed_tax_brackets)):
        if income > fed_tax_brackets[i]:
            if i < len(fed_tax_brackets) - 1:
                applicable_amount = min(fed_tax_brackets[i+1], income)
            else:
                applicable_amount = income
            taxable_amount = applicable_amount - fed_tax_brackets[i]

            # print(f"At Fed bracket, above: ${fed_tax_brackets[i]:,} - {fed_tax_rates[i]*100:.2f}% | Paid: ${fed_tax_rates[i] * taxable_amount:,.2f} on ${taxable_amount:,.2f}")

            tax += fed_tax_rates[i] * taxable_amount
            stock_tax_bracket = i

    stocks_remaining = stocks
    while stocks_remaining > 0:
        if stock_tax_bracket < len(fed_tax_brackets)-1:
            applicable_amount = min(
                    fed_tax_brackets[stock_tax_bracket+1],
                    income + stocks
                ) - max(
                    income, 
                    fed_tax_brackets[stock_tax_bracket]
                )
        else:
            applicable_amount = stocks_remaining

        # print(f"At Fed stock bracket, above: ${fed_tax_brackets[stock_tax_bracket]:,} - {fed_tax_rates[stock_tax_bracket]*100/2:.2f}% | Paid: ${fed_tax_rates[stock_tax_bracket] / 2 * applicable_amount:,.2f} on ${applicable_amount:,.2f}")
        tax += applicable_amount * (fed_tax_rates[stock_tax_bracket]/2)
        stocks_remaining -= applicable_amount
        stock_tax_bracket += 1

    stock_tax_bracket = 0
    for i in range(0, len(prov_tax_brackets)):
        if income > prov_tax_brackets[i]:
            if i < len(prov_tax_brackets) - 1:
                applicable_amount = min(prov_tax_brackets[i+1], income)
            else:
                applicable_amount = income
            taxable_amount = applicable_amount - prov_tax_brackets[i]

            # print(f"At Prov bracket, above: ${prov_tax_brackets[i]} - {prov_tax_rates[i]*100}% | Paid: ${prov_tax_rates[i] * taxable_amount} on ${taxable_amount}")
            tax += prov_tax_rates[i] * taxable_amount

    stocks_remaining = stocks
    while stocks_remaining > 0:
        if stock_tax_bracket < len(prov_tax_brackets)-1:
            applicable_amount = min(
                    prov_tax_brackets[stock_tax_bracket+1],
                    income + stocks
                ) - max(
                    income, 
                    prov_tax_brackets[stock_tax_bracket]
                )
        else:
            applicable_amount = stocks_remaining

        # print(f"At Prov stock bracket, above: ${prov_tax_brackets[stock_tax_bracket]:,} - {prov_tax_rates[stock_tax_bracket]*100/2:.2f}% | Paid: ${prov_tax_rates[stock_tax_bracket] / 2 * applicable_amount:,.2f} on ${applicable_amount:,.2f}")
        tax += applicable_amount * (prov_tax_rates[stock_tax_bracket]/2)
        stocks_remaining -= applicable_amount
        stock_tax_bracket += 1

    return tax

def contribute_max_rrsp(income, last_income):
    room = min(rrsp_annual_add * last_income, rrsp_annual_add_max)
    return room


def calculate_rrsp_earnings(self_growth_percentage, writer):

    annual_income = []
    annual_net = []
    annual_rrsp_max = []
    annual_tax_paid = []
    cumulative_amount_earned = []
    cumulative_tax_paid = []
    cumulative_rrsp_earned_max = []
    cumulative_total = []


    annual_net_self = []
    annual_rrsp_self = []
    annual_tax_paid_self = []
    annual_stocks_self = []
    cumulative_amount_earned_self = []
    cumulative_tax_paid_self = []
    cumulative_rrsp_earned_self = []
    cumulative_stocks_self = []
    cumulative_stocks_rrsp_self = []
    cumulative_total_self = []


    annual_net_wait = []
    annual_rrsp_wait = []
    annual_tax_paid_wait = []
    annual_stocks_wait = []
    stored_rrsp_room_wait = 0
    annual_rrsp_room_wait = []
    cumulative_amount_earned_wait = []
    cumulative_tax_paid_wait = []
    cumulative_rrsp_earned_wait = []
    cumulative_stocks_wait = []
    cumulative_stocks_rrsp_wait = []
    cumulative_total_wait = []

    for y in years:
        # Every year I get income
        cy_income = min(annual_income[-1] * promotion_amount_per_year if y > 23 else starting_annual_income, annual_income_cap)
        
        # Every year, I calculate my RRSP contribution room
        max_contribution_room = contribute_max_rrsp(cy_income, annual_income[-1] if y > 23 else starting_annual_income)
        
        ############################################################################
        # Case 1: Contribute Max

        cy_rrsp_max = max_contribution_room
        company_rrsp_match = company_rrsp_match_percent * cy_income
        cy_my_rrsp_spend = cy_rrsp_max - company_rrsp_match

        # Every year I get taxed on it (independently)
        cy_tax = pay_taxes(cy_income - cy_rrsp_max)

        # Every year takehome (net)
        cy_takehome = cy_income - cy_tax - cy_my_rrsp_spend


        
        annual_net.append(cy_takehome)
        annual_rrsp_max.append(cy_rrsp_max)
        annual_tax_paid.append(cy_tax)

        # Iteration (+ takehome, + taxes, + rrsp)
        cumulative_amount_earned.append((cumulative_amount_earned[-1] if y > 23 else 0) + cy_takehome)
        cumulative_tax_paid.append((cumulative_tax_paid[-1] if y > 23 else 0) + cy_tax)
        cumulative_rrsp_earned_max.append((cumulative_rrsp_earned_max[-1] if y > 23 else 0) * (1+rrsp_inv_growth_per_year) + cy_rrsp_max)
        cumulative_total.append(cumulative_amount_earned[-1] + cumulative_rrsp_earned_max[-1])

        ############################################################################

        annual_income.append(cy_income)


        ############################################################################
        # Case 2: Contribute Minimum, Invest the Rest

        cy_rrsp_self = 2 * cy_income * company_rrsp_match_percent
        cy_rrsp_self_spent = cy_income * company_rrsp_match_percent

        cy_stocks = max_contribution_room - cy_rrsp_self

        cy_stocks_growth = cumulative_stocks_self[-1]*self_growth_percentage if y > 23 else 0

        # Every year I get taxed (plus stocks now)
        cy_tax_self = pay_taxes_and_stocks(cy_income - cy_rrsp_self_spent, cy_stocks_growth)

        # Every year takehome (net)
        cy_takehome_self = cy_income - cy_tax_self - cy_my_rrsp_spend # amount taken out as RRSP amount should be same


        annual_net_self.append(cy_takehome_self)
        annual_rrsp_self.append(cy_rrsp_self)
        annual_stocks_self.append(cy_stocks)
        annual_tax_paid_self.append(cy_tax_self)

        # Iteration (+ takehome, + taxes, + rrsp, + stocks)
        cumulative_amount_earned_self.append((cumulative_amount_earned_self[-1] if y > 23 else 0) + cy_takehome_self)
        cumulative_tax_paid_self.append((cumulative_tax_paid_self[-1] if y > 23 else 0) + cy_tax_self)
        cumulative_rrsp_earned_self.append((cumulative_rrsp_earned_self[-1] if y > 23 else 0) * (1+rrsp_inv_growth_per_year) + cy_rrsp_self)
        cumulative_stocks_self.append((cumulative_stocks_self[-1] if y > 23 else 0) * (1+self_growth_percentage) + cy_stocks)
        cumulative_stocks_rrsp_self.append(cumulative_rrsp_earned_self[-1] + cumulative_stocks_self[-1])
        cumulative_total_self.append(cumulative_amount_earned_self[-1] + cumulative_stocks_rrsp_self[-1])
        ############################################################################


        ############################################################################
        # Case 3: Contribute Minimum, Invest the Rest - Until You Pass the Higher Tax Bracket

        if cy_income > fed_tax_brackets[2] and stored_rrsp_room_wait > 0:
            cy_rrsp_wait = min(stored_rrsp_room_wait, cy_income - fed_tax_brackets[2])
            stored_rrsp_room_wait -= cy_rrsp_wait

        else:
            cy_rrsp_wait = 2 * cy_income * company_rrsp_match_percent
            cy_rrsp_wait_spent = cy_income * company_rrsp_match_percent
            stored_rrsp_room_wait += (max_contribution_room - cy_rrsp_wait)

        cy_stocks = max_contribution_room - cy_rrsp_wait

        cy_stocks_growth = cumulative_stocks_wait[-1]*self_growth_percentage if y > 23 else 0

        # Every year I get taxed (plus stocks now)
        cy_tax_wait = pay_taxes_and_stocks(cy_income - cy_rrsp_wait_spent, cy_stocks_growth)

        # Every year takehome (net)
        cy_takehome_wait = cy_income - cy_tax_wait - cy_my_rrsp_spend # amount taken out as RRSP amount should be same


        annual_net_wait.append(cy_takehome_wait)
        annual_rrsp_wait.append(cy_rrsp_wait)
        annual_stocks_wait.append(cy_stocks)
        annual_rrsp_room_wait.append(stored_rrsp_room_wait)
        annual_tax_paid_wait.append(cy_tax_wait)

        # Iteration (+ takehome, + taxes, + rrsp, + stocks)
        cumulative_amount_earned_wait.append((cumulative_amount_earned_wait[-1] if y > 23 else 0) + cy_takehome_wait)
        cumulative_tax_paid_wait.append((cumulative_tax_paid_wait[-1] if y > 23 else 0) + cy_tax_wait)
        cumulative_rrsp_earned_wait.append((cumulative_rrsp_earned_wait[-1] if y > 23 else 0) * (1+rrsp_inv_growth_per_year) + cy_rrsp_wait)
        cumulative_stocks_wait.append((cumulative_stocks_wait[-1] if y > 23 else 0) * (1+self_growth_percentage) + cy_stocks)
        cumulative_stocks_rrsp_wait.append(cumulative_rrsp_earned_wait[-1] + cumulative_stocks_wait[-1])
        cumulative_total_wait.append(cumulative_amount_earned_wait[-1] + cumulative_stocks_rrsp_wait[-1])
        ############################################################################
        # print(f"  Year: {y} \t| Income: ${cy_income:,.2f} \t| Stocks: {cy_stocks} | Stock Growth: {cy_stocks_growth} | RRSP: {cy_rrsp_self}")
        # print(f"Year {y} | Income: {cy_income:,.2f} \t| Built Up Contribution Rooms: {stored_rrsp_room_self:,.2f}")

        if y%10 == 0:
            print(f"Max  Year: {y} \t| Cumulative RRSP: {cumulative_rrsp_earned_max[-1]:,.2f} | Tax: {cumulative_tax_paid[-1]:,.2f} | Earnings After Tax: {(cumulative_amount_earned[-1] ):,.2f} | Total: {cumulative_total[-1]:,.2f}")
            print(f"Self Year: {y} \t| Cumulative RRSP+Stocks: {cumulative_stocks_rrsp_self[-1]:,.2f} | Tax: {cumulative_tax_paid_self[-1]:,.2f} | Earnings After Tax: {(cumulative_amount_earned_self[-1] ):,.2f} | Total: {cumulative_total_self[-1]:,.2f}")
            print(f"                | RRSP: {cumulative_rrsp_earned_self[-1]:,.2f} | Stocks: {cumulative_stocks_self[-1]:,.2f}")
            print(f"Wait Year: {y} \t| Cumulative RRSP+Stocks: {cumulative_stocks_rrsp_wait[-1]:,.2f} | Tax: {cumulative_tax_paid_wait[-1]:,.2f} | Earnings After Tax: {(cumulative_amount_earned_wait[-1] ):,.2f} | Total: {cumulative_total_wait[-1]:,.2f}")
            print(f"                | RRSP: {cumulative_rrsp_earned_wait[-1]:,.2f} | Stocks: {cumulative_stocks_wait[-1]:,.2f}")
            print("")

            writer.writerow([rate, y, 'Max', f"{cumulative_rrsp_earned_max[-1]:,.2f}", "0.00", f"{cumulative_tax_paid[-1]:,.2f}", f"{cumulative_total[-1]:,.2f}"])
            writer.writerow([rate, y, 'Self', f"{cumulative_rrsp_earned_self[-1]:,.2f}", f"{cumulative_stocks_self[-1]:,.2f}", f"{cumulative_amount_earned_self[-1]:,.2f}", f"{cumulative_total_self[-1]:,.2f}"])
            writer.writerow([rate, y, 'Wait', f"{cumulative_rrsp_earned_wait[-1]:,.2f}", f"{cumulative_stocks_wait[-1]:,.2f}", f"{cumulative_amount_earned_wait[-1]:,.2f}", f"{cumulative_total_wait[-1]:,.2f}"])


    # Create DataFrame
    df = pd.DataFrame({
        # 'Annual Income': annual_income,
        # # 'Annual Takehome': annual_net,
        # 'Annual RRSP Max': annual_rrsp_max,
        # 'Earned Takehome': cumulative_amount_earned,
        # 'Annual Tax Paid': annual_tax_paid,
        # 'Taxes Paid': cumulative_tax_paid,
        'Max: RRSP': cumulative_rrsp_earned_max,
        'Max: Total': cumulative_total,

        # 'Annual Takehome Self': annual_net_self,
        # 'Annual RRSP Self': annual_rrsp_self,
        # 'Annual Stocks Self': annual_stocks_self,
        # 'Annual Tax Paid Self': annual_tax_paid_self,
        # 'cumulative Stocks': cumulative_stocks_self,
        # 'cumulative RRSP Self': cumulative_rrsp_earned_self,
        'Self: Stocks + RRSP': cumulative_stocks_rrsp_self,
        'Self: Total': cumulative_total_self,
        # 'Annual RRSP Room': annual_rrsp_room_self,


        'Wait: Stocks + RRSP': cumulative_stocks_rrsp_wait,
        'Wait: Total': cumulative_total_wait,

    },
        index = years
    )

    ax = df.plot.line()
    plt.title(f"Earnings at {rate*100}%")
    plt.xlabel("Age")
    plt.ylabel("Value ($)")
    plt.ylim(bottom=0)
    plt.xlim(left=23)
    plt.show()


with open('./rrsp_comparison.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Growth Rate', 'Year', 'Scenario', 'Cumulative RRSP', 'Stocks', 'Total Tax Paid', 'Total Wealth'])
    for rate in self_inv_growth_per_year:
        calculate_rrsp_earnings(rate, writer)
