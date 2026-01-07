"""
Coast FIRE Calculator

A personal finance modeling tool to determine if your current investments
will grow to meet your retirement goals without additional contributions.

Definition:
Coast FIRE occurs when your current corpus, through compound interest,
will fully fund your retirement by your target retirement age.
"""

from typing import NamedTuple


class CoastFIREInput(NamedTuple):
    """Input parameters for Coast FIRE calculation."""
    current_age: int
    retirement_age: int
    current_investment: float
    expected_annual_return: float
    expected_monthly_expense_at_retirement: float
    inflation_rate: float = 0.0


class CoastFIREResult(NamedTuple):
    """Output results of Coast FIRE calculation."""
    years_to_grow: int
    annual_expense_at_retirement: float
    fire_number_required: float
    future_value_at_retirement: float
    surplus_or_shortfall: float
    has_achieved_coast_fire: bool


def validate_inputs(inputs: CoastFIREInput) -> None:
    """
    Validate Coast FIRE input parameters.
    
    Args:
        inputs: CoastFIREInput containing all parameters
        
    Raises:
        ValueError: If any input is invalid
    """
    if inputs.current_age < 0:
        raise ValueError("current_age must be non-negative")
    
    if inputs.retirement_age <= inputs.current_age:
        raise ValueError("retirement_age must be greater than current_age")
    
    if inputs.current_investment < 0:
        raise ValueError("current_investment must be non-negative")
    
    if inputs.expected_annual_return < -1:
        raise ValueError("expected_annual_return must be greater than -100%")
    
    if inputs.expected_monthly_expense_at_retirement < 0:
        raise ValueError("expected_monthly_expense_at_retirement must be non-negative")
    
    if inputs.inflation_rate < 0:
        raise ValueError("inflation_rate must be non-negative")


def calculate_years_to_grow(current_age: int, retirement_age: int) -> int:
    """
    Calculate years until retirement.
    
    Args:
        current_age: Current age in years
        retirement_age: Target retirement age in years
        
    Returns:
        Number of years until retirement
    """
    return retirement_age - current_age


def calculate_annual_expense_at_retirement(
    monthly_expense: float,
    inflation_rate: float,
    years_to_grow: int
) -> float:
    """
    Calculate annual retirement expense adjusted for inflation.
    
    The calculation uses compound inflation:
    Future_Expense = Current_Expense × (1 + inflation_rate)^years
    
    Args:
        monthly_expense: Current monthly expense amount
        inflation_rate: Annual inflation rate (as decimal, e.g., 0.03 for 3%)
        years_to_grow: Number of years until retirement
        
    Returns:
        Annual expense at retirement, inflation-adjusted
    """
    annual_expense = monthly_expense * 12
    
    # Adjust for inflation
    inflation_multiplier = (1 + inflation_rate) ** years_to_grow
    future_annual_expense = annual_expense * inflation_multiplier
    
    return future_annual_expense


def calculate_fire_number(annual_expense_at_retirement: float) -> float:
    """
    Calculate the FIRE number using the 4% rule.
    
    The 4% rule suggests you can safely withdraw 4% of your portfolio annually.
    Therefore: Portfolio = Annual_Expense / 0.04 = Annual_Expense × 25
    
    This rule is based on historical market data and assumes a diversified
    portfolio of stocks and bonds.
    
    Args:
        annual_expense_at_retirement: Annual expense at retirement
        
    Returns:
        Required portfolio value (FIRE number)
    """
    SAFE_WITHDRAWAL_RATE = 0.04
    return annual_expense_at_retirement / SAFE_WITHDRAWAL_RATE


def calculate_future_value(
    present_value: float,
    annual_return: float,
    years: int
) -> float:
    """
    Calculate future value of an investment using compound interest.
    
    Formula: FV = PV × (1 + r)^n
    
    Args:
        present_value: Current investment amount
        annual_return: Annual return rate (as decimal, e.g., 0.07 for 7%)
        years: Number of years
        
    Returns:
        Future value of the investment
    """
    if years == 0:
        return present_value
    
    return present_value * ((1 + annual_return) ** years)


def calculate_coast_fire(inputs: CoastFIREInput) -> CoastFIREResult:
    """
    Calculate whether the user has achieved Coast FIRE.
    
    Args:
        inputs: CoastFIREInput with all required parameters
        
    Returns:
        CoastFIREResult containing all calculated values and conclusion
        
    Raises:
        ValueError: If any input validation fails
    """
    validate_inputs(inputs)
    
    # Step 1: Calculate time horizon
    years_to_grow = calculate_years_to_grow(
        inputs.current_age,
        inputs.retirement_age
    )
    
    # Step 2: Calculate retirement expenses adjusted for inflation
    annual_expense_at_retirement = calculate_annual_expense_at_retirement(
        inputs.expected_monthly_expense_at_retirement,
        inputs.inflation_rate,
        years_to_grow
    )
    
    # Step 3: Calculate FIRE number (using 4% rule)
    fire_number_required = calculate_fire_number(annual_expense_at_retirement)
    
    # Step 4: Calculate future value of current investment
    future_value_at_retirement = calculate_future_value(
        inputs.current_investment,
        inputs.expected_annual_return,
        years_to_grow
    )
    
    # Step 5: Determine success
    surplus_or_shortfall = future_value_at_retirement - fire_number_required
    has_achieved_coast_fire = future_value_at_retirement >= fire_number_required
    
    return CoastFIREResult(
        years_to_grow=years_to_grow,
        annual_expense_at_retirement=annual_expense_at_retirement,
        fire_number_required=fire_number_required,
        future_value_at_retirement=future_value_at_retirement,
        surplus_or_shortfall=surplus_or_shortfall,
        has_achieved_coast_fire=has_achieved_coast_fire
    )


def calculate_required_monthly_investment(
    fire_number_required: float,
    annual_return: float,
    years_to_grow: int
) -> float:
    """
    Calculate the monthly investment amount needed to reach FIRE number.
    
    Uses Future Value of Annuity formula:
    FV = PMT × [((1 + r)^n - 1) / r]
    
    Solving for PMT:
    PMT = FV / [((1 + r)^n - 1) / r]
    
    Args:
        fire_number_required: Target portfolio value (FIRE number)
        annual_return: Annual return rate (as decimal, e.g., 0.07 for 7%)
        years_to_grow: Number of years until retirement
        
    Returns:
        Required monthly investment amount
    """
    if years_to_grow == 0:
        return 0.0
    
    # Convert annual return to monthly return
    monthly_return = annual_return / 12
    total_months = years_to_grow * 12
    
    # Avoid division by zero
    if monthly_return == 0:
        return fire_number_required / total_months
    
    # Calculate using Future Value of Annuity formula
    # FV = PMT × [((1 + r)^n - 1) / r]
    # PMT = FV / [((1 + r)^n - 1) / r]
    fv_factor = ((1 + monthly_return) ** total_months - 1) / monthly_return
    required_monthly = fire_number_required / fv_factor
    
    return required_monthly


def format_currency(amount: float) -> str:
    """
    Format a number as currency (Indian Rupees).
    
    Args:
        amount: Numeric value to format
        
    Returns:
        Currency-formatted string
    """
    return f"₹{amount:,.2f}"


def calculate_average_return(
    initial_return: float,
    annual_decrease: float,
    years: int
) -> float:
    """
    Calculate average annual return when return decreases each year.
    
    The return decreases linearly from initial_return to final_return:
    Year 1: initial_return
    Year 2: initial_return - annual_decrease
    Year 3: initial_return - 2*annual_decrease
    ...
    Year n: initial_return - (n-1)*annual_decrease
    
    Args:
        initial_return: Initial annual return rate (as decimal)
        annual_decrease: Annual decrease in return (as decimal)
        years: Number of years
        
    Returns:
        Average annual return over the period
    """
    if years == 0:
        return initial_return
    
    # Final return at the end of the period
    final_return = max(initial_return - (years - 1) * annual_decrease, 0)
    
    # Average of initial and final return (linear change)
    average_return = (initial_return + final_return) / 2
    
    return average_return


def calculate_coast_fire_age(
    current_age: int,
    retirement_age: int,
    monthly_investment: float,
    initial_return: float,
    annual_return_decrease: float,
    fire_number: float
) -> int:
    """
    Calculate the age at which you can stop investing (Coast FIRE age).
    
    Given a monthly investment amount, finds the age when your accumulated
    portfolio will grow to meet your FIRE number by retirement.
    
    Args:
        current_age: Current age in years
        retirement_age: Target retirement age in years
        monthly_investment: Monthly investment amount (SIP)
        initial_return: Initial annual return rate (as decimal)
        annual_return_decrease: Annual decrease in return (as decimal)
        fire_number: Target FIRE number needed
        
    Returns:
        Coast FIRE age (age when you can stop investing)
    """
    for test_age in range(current_age, retirement_age + 1):
        years_to_invest = test_age - current_age
        years_to_grow_after = retirement_age - test_age
        
        # Calculate what you'll have accumulated by test_age
        avg_return_phase1 = calculate_average_return(initial_return, annual_return_decrease, years_to_invest)
        
        # FV of annuity (monthly investments)
        if years_to_invest == 0:
            accumulated = 0
        else:
            monthly_return = avg_return_phase1 / 12
            total_months = years_to_invest * 12
            
            if monthly_return == 0:
                accumulated = monthly_investment * total_months
            else:
                fv_factor = ((1 + monthly_return) ** total_months - 1) / monthly_return
                accumulated = monthly_investment * fv_factor
        
        # Calculate what this will grow to by retirement
        starting_return_phase2 = max(initial_return - (years_to_invest) * annual_return_decrease, 0)
        avg_return_phase2 = calculate_average_return(starting_return_phase2, annual_return_decrease, years_to_grow_after)
        
        future_value = calculate_future_value(accumulated, avg_return_phase2, years_to_grow_after)
        
        # Check if we've reached FIRE number
        if future_value >= fire_number:
            return test_age
    
    # If we reach here, can't achieve Coast FIRE with given investment
    return retirement_age


def print_coast_fire_age_report(
    current_age: int,
    retirement_age: int,
    monthly_investment: float,
    initial_return: float,
    annual_return_decrease: float,
    coast_fire_age: int,
    fire_number: float
) -> None:
    """
    Print report for Coast FIRE age calculation.
    
    Args:
        current_age: Current age
        retirement_age: Target retirement age
        monthly_investment: Monthly investment amount
        initial_return: Initial return rate
        annual_return_decrease: Annual return decrease
        coast_fire_age: Calculated Coast FIRE age
        fire_number: FIRE number needed
    """
    print("\n" + "="*70)
    print("COAST FIRE AGE CALCULATOR")
    print("="*70)
    
    years_to_invest = coast_fire_age - current_age
    years_to_grow_after = retirement_age - coast_fire_age
    
    print(f"\n📊 YOUR PARAMETERS:")
    print(f"  • Current Age:                    {current_age} years")
    print(f"  • Retirement Age:                 {retirement_age} years")
    print(f"  • Monthly Investment (SIP):       {format_currency(monthly_investment)}")
    print(f"  • Initial Annual Return:          {initial_return * 100:.2f}%")
    print(f"  • Annual Return Decrease:         {annual_return_decrease * 100:.2f}%")
    print(f"  • FIRE Number Required:           {format_currency(fire_number)}")
    
    print(f"\n🎯 RESULT:")
    print(f"  ✅ Coast FIRE Age:                {coast_fire_age} years")
    print(f"  ✅ Years to Invest:               {years_to_invest} years")
    print(f"  ✅ Years to Grow (no investing):  {years_to_grow_after} years")
    
    print(f"\n📋 PLAN BREAKDOWN:")
    print(f"  • Phase 1 (Investment): Age {current_age}-{coast_fire_age} ({years_to_invest} years)")
    print(f"    → Invest {format_currency(monthly_investment)} every month")
    
    avg_return_phase1 = calculate_average_return(initial_return, annual_return_decrease, years_to_invest)
    final_return_phase1 = max(initial_return - (years_to_invest - 1) * annual_return_decrease, 0)
    
    print(f"    → Starting Return (Age {current_age}):   {initial_return * 100:.2f}%")
    print(f"    → Ending Return (Age {coast_fire_age}):     {final_return_phase1 * 100:.2f}%")
    print(f"    → Average Return:              {avg_return_phase1 * 100:.2f}%")
    
    # Calculate accumulated amount
    if years_to_invest == 0:
        accumulated = 0
    else:
        monthly_return = avg_return_phase1 / 12
        total_months = years_to_invest * 12
        if monthly_return == 0:
            accumulated = monthly_investment * total_months
        else:
            fv_factor = ((1 + monthly_return) ** total_months - 1) / monthly_return
            accumulated = monthly_investment * fv_factor
    
    print(f"    → Accumulated by age {coast_fire_age}: {format_currency(accumulated)}")
    
    print(f"\n  • Phase 2 (Growth): Age {coast_fire_age}-{retirement_age} ({years_to_grow_after} years)")
    print(f"    → Stop investing, let money grow")
    
    starting_return_phase2 = max(initial_return - (years_to_invest) * annual_return_decrease, 0)
    avg_return_phase2 = calculate_average_return(starting_return_phase2, annual_return_decrease, years_to_grow_after)
    final_return_phase2 = max(starting_return_phase2 - (years_to_grow_after - 1) * annual_return_decrease, 0)
    
    print(f"    → Starting Return (Age {coast_fire_age}):   {starting_return_phase2 * 100:.2f}%")
    print(f"    → Ending Return (Age {retirement_age}):     {final_return_phase2 * 100:.2f}%")
    print(f"    → Average Return:              {avg_return_phase2 * 100:.2f}%")
    
    future_value = calculate_future_value(accumulated, avg_return_phase2, years_to_grow_after)
    print(f"    → {format_currency(accumulated)} will grow to {format_currency(future_value)}")
    
    print(f"\n💡 SUMMARY:")
    print(f"  By investing ₹{monthly_investment:,.0f} per month for {years_to_invest} years,")
    print(f"  you can achieve Coast FIRE at age {coast_fire_age}!")
    print(f"  Then let it grow for {years_to_grow_after} more years to {format_currency(fire_number)}")
    
    print("\n" + "="*70 + "\n")


def print_coast_fire_report(inputs: CoastFIREInput, result: CoastFIREResult) -> None:
    """
    Print a formatted Coast FIRE report.
    
    Args:
        inputs: Original input parameters
        result: Calculated Coast FIRE results
    """
    print("\n" + "="*70)
    print("COAST FIRE ANALYSIS REPORT")
    print("="*70)
    
    print("\n📊 INPUT PARAMETERS:")
    print(f"  • Current Age:                    {inputs.current_age} years")
    print(f"  • Target Retirement Age:          {inputs.retirement_age} years")
    print(f"  • Current Investment:             {format_currency(inputs.current_investment)}")
    print(f"  • Expected Annual Return:         {inputs.expected_annual_return * 100:.2f}%")
    print(f"  • Monthly Expense (current):      {format_currency(inputs.expected_monthly_expense_at_retirement)}")
    if inputs.inflation_rate > 0:
        print(f"  • Inflation Rate:                 {inputs.inflation_rate * 100:.2f}%")
    
    print("\n📈 CALCULATED VALUES:")
    print(f"  • Years to Grow:                  {result.years_to_grow} years")
    print(f"  • Annual Expense at Retirement:   {format_currency(result.annual_expense_at_retirement)}")
    print(f"  • FIRE Number Required (4% rule): {format_currency(result.fire_number_required)}")
    print(f"  • Future Value of Investment:     {format_currency(result.future_value_at_retirement)}")
    
    print("\n💰 RESULT:")
    if result.surplus_or_shortfall >= 0:
        print(f"  ✅ SURPLUS: {format_currency(result.surplus_or_shortfall)}")
    else:
        print(f"  ❌ SHORTFALL: {format_currency(abs(result.surplus_or_shortfall))}")
    
    print("\n🎯 COAST FIRE STATUS:")
    if result.has_achieved_coast_fire:
        print(f"  ✅ YES - You have achieved Coast FIRE!")
        print(f"     Your current investment of {format_currency(inputs.current_investment)}")
        print(f"     will grow to {format_currency(result.future_value_at_retirement)}")
        print(f"     at {inputs.expected_annual_return * 100:.2f}% annual return.")
        print(f"     You can stop investing and let compound interest do the work!")
    else:
        print(f"  ❌ NO - You have not achieved Coast FIRE yet.")
        print(f"     You need {format_currency(result.fire_number_required)}")
        print(f"     but will have {format_currency(result.future_value_at_retirement)}")
        print(f"     Continue investing to reach your goal.")
    
    print("\n" + "="*70 + "\n")


def main() -> None:
    """
    Main function for Coast FIRE calculator.
    """
    # Interactive user input
    print("\n>>> Coast FIRE Calculator")
    print("\nChoose an option:")
    print("1. Calculate if you've achieved Coast FIRE (with current investment)")
    print("2. Calculate Coast FIRE age (given monthly investment)")
    
    try:
        choice = input("\nEnter choice (1 or 2) [1]: ") or "1"
        
        current_age = int(input("Current age [35]: ") or "35")
        retirement_age = int(input("Retirement age [60]: ") or "60")
        initial_return = float(input("Expected annual return at current age (%) [7]: ") or "7") / 100
        annual_return_decrease = float(input("Annual decrease in return (%) [0.1]: ") or "0.1") / 100
        monthly_expense = float(input("Monthly expense at retirement [₹4,000]: ") or "4000")
        inflation_rate = float(input("Inflation rate (%) [3, optional]: ") or "3") / 100
        
        # Calculate FIRE number (same for both modes)
        years_to_retirement = retirement_age - current_age
        annual_expense = monthly_expense * 12
        inflation_multiplier = (1 + inflation_rate) ** years_to_retirement
        future_annual_expense = annual_expense * inflation_multiplier
        fire_number = future_annual_expense / 0.04
        
        if choice == "1":
            # Mode 1: Coast FIRE with current investment
            current_investment = float(input("Current investment [₹250,000]: ") or "250000")
            
            average_return = calculate_average_return(initial_return, annual_return_decrease, years_to_retirement)
            
            user_inputs = CoastFIREInput(
                current_age=current_age,
                retirement_age=retirement_age,
                current_investment=current_investment,
                expected_annual_return=average_return,
                expected_monthly_expense_at_retirement=monthly_expense,
                inflation_rate=inflation_rate
            )
            
            user_result = calculate_coast_fire(user_inputs)
            print_coast_fire_report(user_inputs, user_result)
            
            # Show return breakdown
            final_return = max(initial_return - (years_to_retirement - 1) * annual_return_decrease, 0)
            print(f"📊 Return Schedule:")
            print(f"  • Starting Return (Age {current_age}):    {initial_return * 100:.2f}%")
            print(f"  • Ending Return (Age {retirement_age}):     {final_return * 100:.2f}%")
            print(f"  • Average Return:                {average_return * 100:.2f}%")
            print()
        
        elif choice == "2":
            # Mode 2: Calculate Coast FIRE age given monthly investment
            monthly_investment = float(input("Monthly investment (SIP) [₹25,000]: ") or "25000")
            
            coast_fire_age = calculate_coast_fire_age(
                current_age,
                retirement_age,
                monthly_investment,
                initial_return,
                annual_return_decrease,
                fire_number
            )
            
            print_coast_fire_age_report(
                current_age,
                retirement_age,
                monthly_investment,
                initial_return,
                annual_return_decrease,
                coast_fire_age,
                fire_number
            )
        
    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()
