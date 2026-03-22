## README: RRSP vs. Non-Registered Stock Simulation (2026 Edition)

This simulation compares three distinct financial strategies for managing the **18% of earned income** that the CRA allows for RRSP contributions. It is designed specifically for the **2026 Canadian tax landscape**, accounting for the lower **14% federal base rate** and the **cancellation of the 66.7% capital gains inclusion hike**.

### The Core Assumption
In all three cases, you are committed to "spending" the same amount of gross income (**18%**) on your future. Whether that money goes into a tax-sheltered RRSP or a taxable brokerage account, your **lifestyle cash flow remains identical** across all scenarios.

---

### The Three Scenarios

#### 1. Case: Max (The Immediate Sheltering)
* **Strategy:** You contribute the full 18% (up to the annual limit of **$33,810**) to your RRSP every single year.
* **Tax Impact:** Your taxable income is reduced immediately. You pay the least amount of tax today.
* **Growth:** 100% of the contribution grows tax-free inside the RRSP.
* **Best For:** High-income earners looking to dodge the top tax brackets immediately.

#### 2. Case: Self (The Hybrid/Balanced)
* **Strategy:** You only contribute enough to your RRSP to get your full employer match (assumed 3% personal + 3% company). The remaining of your "future fund" is put into **non-registered stocks**.
* **Tax Impact:** You pay tax on 97% of your salary. Additionally, because you are "perpetually liquidating" your stocks, you pay tax annually on **50% of your capital gains**.
* **Growth:** Your RRSP grows tax-free, but your stock portfolio is "tax-dragged"—the money to pay the capital gains tax is pulled from your take-home pay.
* **Best For:** Those who want a mix of locked-in retirement funds and accessible (though taxed) liquid wealth.

#### 3. Case: Wait (The Strategic Deferral)
* **Strategy:** You ignore the RRSP (except for the 3% match) while your income is lower. You stockpile all that 15% "room" into stocks. Once your income hits a high-tax threshold (set at **$117,045** for 2026), you begin aggressively moving money from your stocks into your RRSP to "catch up."
* **Tax Impact:** You pay high taxes early on. Later, you receive massive tax relief by dumping huge sums into your RRSP during your highest-earning years.
* **Growth:** You benefit from high stock growth early, then "wash" the taxes by moving the gains into a sheltered environment later.
* **Best For:** Professionals expecting a significant "hockey stick" increase in their salary over 10+ years.

---
* **Liquidation Logic:** All stock growth is treated as realized annual income, meaning the "Total Wealth" shown is truly yours (after the tax man has taken his cut of the gains).

### How to Use
1.  Run the script to generate `rrsp_modeling_2026.csv`.
2.  The CSV will break down results for 5 different growth rates (**12% to 30%**).
3.  Compare the **Total Wealth** column at the 15 and 25-year marks to see which strategy wins at your expected rate of return.
