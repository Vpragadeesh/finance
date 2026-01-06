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
    Main function demonstrating Coast FIRE calculator usage.
    """
    # Interactive user input
    print("\n>>> Interactive Calculator")
    print("\nChoose an option:")
    print("1. Calculate if you've achieved Coast FIRE (with lump sum)")
    print("2. Calculate required monthly investment to reach FIRE number")
    print("3. Calculate investment needed until Coast FIRE age")
    
    try:
        choice = input("\nEnter choice (1, 2, or 3) [1]: ") or "1"
        
        current_age = int(input("Current age [35]: ") or "35")
        retirement_age = int(input("Retirement age [60]: ") or "60")
        annual_return = float(input("Expected annual return (%) [7]: ") or "7") / 100
        monthly_expense = float(input("Monthly expense at retirement [₹4,000]: ") or "4000")
        inflation_rate = float(input("Inflation rate (%) [3, optional]: ") or "3") / 100
        
        if choice == "1":
            # Coast FIRE with lump sum
            current_investment = float(input("Current investment [₹250,000]: ") or "250000")
            
            user_inputs = CoastFIREInput(
                current_age=current_age,
                retirement_age=retirement_age,
                current_investment=current_investment,
                expected_annual_return=annual_return,
                expected_monthly_expense_at_retirement=monthly_expense,
                inflation_rate=inflation_rate
            )
            
            user_result = calculate_coast_fire(user_inputs)
            print_coast_fire_report(user_inputs, user_result)
        
        elif choice == "2":
            # Calculate required monthly SIP
            current_investment = float(input("Current investment [₹0]: ") or "0")
            years_to_grow = retirement_age - current_age
            
            # First calculate FIRE number
            annual_expense = monthly_expense * 12
            inflation_multiplier = (1 + inflation_rate) ** years_to_grow
            future_annual_expense = annual_expense * inflation_multiplier
            fire_number = future_annual_expense / 0.04
            
            # Calculate current investment growth
            current_future_value = calculate_future_value(
                current_investment,
                annual_return,
                years_to_grow
            )
            
            # Calculate required monthly investment
            required_monthly = calculate_required_monthly_investment(
                fire_number,
                annual_return,
                years_to_grow
            )
            
            print("\n" + "="*70)
            print("COAST FIRE ANALYSIS + MONTHLY INVESTMENT CALCULATOR")
            print("="*70)
            print(f"\n📊 YOUR PARAMETERS:")
            print(f"  • Current Age:                    {current_age} years")
            print(f"  • Target Retirement Age:          {retirement_age} years")
            print(f"  • Years to Grow:                  {years_to_grow} years")
            print(f"  • Current Investment:             {format_currency(current_investment)}")
            print(f"  • Expected Annual Return:         {annual_return * 100:.2f}%")
            print(f"  • Monthly Expense (current):      {format_currency(monthly_expense)}")
            print(f"  • Inflation Rate:                 {inflation_rate * 100:.2f}%")
            
            print(f"\n📈 CALCULATED VALUES:")
            print(f"  • Future Annual Expense:          {format_currency(future_annual_expense)}")
            print(f"  • FIRE Number Required (4% rule): {format_currency(fire_number)}")
            print(f"  • Current investment will grow to: {format_currency(current_future_value)}")
            
            shortfall = fire_number - current_future_value
            
            print(f"\n🎯 COAST FIRE STATUS:")
            if current_future_value >= fire_number:
                print(f"  ✅ YES - You have achieved Coast FIRE!")
                print(f"     Your current investment of {format_currency(current_investment)}")
                print(f"     will grow to {format_currency(current_future_value)}")
                print(f"     which exceeds your FIRE number by {format_currency(current_future_value - fire_number)}")
                print(f"     You can stop investing and let compound interest do the work!")
                print(f"\n  ℹ️  No monthly investment needed!")
            else:
                print(f"  ❌ NO - You have not achieved Coast FIRE yet.")
                print(f"     Your current investment will grow to: {format_currency(current_future_value)}")
                print(f"     You need: {format_currency(fire_number)}")
                print(f"     Shortfall: {format_currency(shortfall)}")
                
                print(f"\n💰 MONTHLY INVESTMENT REQUIRED:")
                print(f"  ✅ Monthly SIP Amount:            {format_currency(required_monthly)}")
                print(f"\n  This means if you invest {format_currency(required_monthly)} every month")
                print(f"  for {years_to_grow} years at {annual_return * 100:.1f}% annual return,")
                print(f"  combined with your current {format_currency(current_investment)},")
                print(f"  you'll accumulate {format_currency(fire_number)} by age {retirement_age}!")
            
            print("\n" + "="*70 + "\n")
        
        elif choice == "3":
            # Calculate investment needed until Coast FIRE age (stop investing age)
            coast_fire_age = int(input("Coast FIRE age (when you'll stop investing) [40]: ") or "40")
            
            if coast_fire_age <= current_age:
                print("\n❌ Error: Coast FIRE age must be greater than current age")
                return
            
            if coast_fire_age > retirement_age:
                print("\n❌ Error: Coast FIRE age must be before retirement age")
                return
            
            years_to_invest = coast_fire_age - current_age
            years_to_grow_after = retirement_age - coast_fire_age
            
            # Calculate FIRE number
            annual_expense = monthly_expense * 12
            inflation_multiplier = (1 + inflation_rate) ** (retirement_age - current_age)
            future_annual_expense = annual_expense * inflation_multiplier
            fire_number = future_annual_expense / 0.04
            
            # Calculate what the amount needs to be at coast_fire_age
            # to grow to fire_number by retirement_age
            # fire_number = amount_at_coast_fire_age * (1 + annual_return)^years_to_grow_after
            # amount_at_coast_fire_age = fire_number / (1 + annual_return)^years_to_grow_after
            
            if years_to_grow_after == 0:
                amount_at_coast_fire_age = fire_number
            else:
                amount_at_coast_fire_age = fire_number / ((1 + annual_return) ** years_to_grow_after)
            
            # Calculate required monthly investment to reach amount_at_coast_fire_age
            required_monthly = calculate_required_monthly_investment(
                amount_at_coast_fire_age,
                annual_return,
                years_to_invest
            )
            
            print("\n" + "="*70)
            print("COAST FIRE PLANNING CALCULATOR")
            print("="*70)
            print(f"\n📊 YOUR PARAMETERS:")
            print(f"  • Current Age:                    {current_age} years")
            print(f"  • Coast FIRE Age (stop investing): {coast_fire_age} years")
            print(f"  • Retirement Age:                 {retirement_age} years")
            print(f"  • Years to Invest:                {years_to_invest} years")
            print(f"  • Years to Grow (without investing): {years_to_grow_after} years")
            print(f"  • Monthly Expense (current):      {format_currency(monthly_expense)}")
            print(f"  • Expected Annual Return:         {annual_return * 100:.2f}%")
            print(f"  • Inflation Rate:                 {inflation_rate * 100:.2f}%")
            
            print(f"\n📈 CALCULATED VALUES:")
            print(f"  • Future Annual Expense:          {format_currency(future_annual_expense)}")
            print(f"  • FIRE Number Required (4% rule): {format_currency(fire_number)}")
            print(f"  • Amount needed at Coast FIRE age: {format_currency(amount_at_coast_fire_age)}")
            
            print(f"\n💰 INVESTMENT REQUIRED:")
            print(f"  ✅ Monthly SIP Amount:            {format_currency(required_monthly)}")
            
            print(f"\n📋 PLAN BREAKDOWN:")
            print(f"  • Phase 1 (Investment): Age {current_age}-{coast_fire_age} ({years_to_invest} years)")
            print(f"    → Invest {format_currency(required_monthly)} every month")
            print(f"    → This will grow to {format_currency(amount_at_coast_fire_age)}")
            
            print(f"\n  • Phase 2 (Growth): Age {coast_fire_age}-{retirement_age} ({years_to_grow_after} years)")
            print(f"    → Stop investing, let money grow")
            print(f"    → {format_currency(amount_at_coast_fire_age)} will grow to {format_currency(fire_number)}")
            print(f"    → Compound growth at {annual_return * 100:.1f}% annually")
            
            print(f"\n🎯 RESULT:")
            print(f"  ✅ By age {retirement_age}, you'll have {format_currency(fire_number)}")
            print(f"     which provides ₹{(fire_number * 0.04) / 12:,.0f}/month withdrawal")
            
            print("\n" + "="*70 + "\n")
        
    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()