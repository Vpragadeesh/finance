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
    Main function for Coast FIRE calculation.
    """
    # Interactive user input
    print("\n>>> Coast FIRE Calculator")
    
    try:
        current_age = int(input("Current age [35]: ") or "35")
        retirement_age = int(input("Retirement age [60]: ") or "60")
        current_investment = float(input("Current investment [₹250,000]: ") or "250000")
        initial_return = float(input("Expected annual return at current age (%) [7]: ") or "7") / 100
        annual_return_decrease = float(input("Annual decrease in return (%) [0.1]: ") or "0.1") / 100
        monthly_expense = float(input("Monthly expense at retirement [₹4,000]: ") or "4000")
        inflation_rate = float(input("Inflation rate (%) [3, optional]: ") or "3") / 100
        
        years_to_retirement = retirement_age - current_age
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
        
    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()
