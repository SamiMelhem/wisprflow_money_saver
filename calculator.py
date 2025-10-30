class SavingsCalculator:
    def __init__(self):
        # Subscription costs per month
        self.subscription_costs = {
            'student': 7.00,        # $7/month
            'pro_monthly': 15.00,   # $15/month  
            'pro_annually': 12.00   # $12/month (annual plan)
        }
        
        # Minutes per month
        self.minutes_per_month = (365 / 12) * 24 * 60  # 43800 minutes
        
    def calculate_annual_savings(self, daily_words, speaking_wpm, typing_wpm, subscription_type, hourly_rate=25.0):
        """
        Calculate annual savings based on daily usage patterns.
        """
        # Calculate daily time savings
        daily_speaking_time = daily_words / speaking_wpm
        daily_typing_time = daily_words / typing_wpm
        daily_time_saved = daily_typing_time - daily_speaking_time
        
        # Calculate daily value saved
        daily_value_saved = daily_time_saved * (hourly_rate / 60)
        
        # Calculate annual projections
        annual_words = daily_words * 365.25
        annual_time_saved_hours = (daily_time_saved * 365.25) / 60
        annual_value_saved = daily_value_saved * 365.25
        
        # Calculate subscription costs
        annual_subscription_cost = self.subscription_costs[subscription_type] * 12
        
        # Calculate net annual savings
        net_annual_savings = annual_value_saved - annual_subscription_cost
        
        # Calculate ROI
        roi_percentage = (net_annual_savings / annual_subscription_cost) * 100
        
        return {
            'daily_time_saved_minutes': daily_time_saved,
            'daily_value_saved': daily_value_saved,
            'annual_words': annual_words,
            'annual_time_saved_hours': annual_time_saved_hours,
            'annual_value_saved': annual_value_saved,
            'annual_subscription_cost': annual_subscription_cost,
            'net_annual_savings': net_annual_savings,
            'roi_percentage': roi_percentage,
        }
    
    def calculate_complete_savings(self, words_spoken, speaking_wpm, typing_wpm, subscription_type, hourly_rate=25.0, daily_words=None):
        """
        Calculate complete savings (time + cost) for a single session and annual projections.
        
        Args:
            words_spoken (int): Number of words spoken
            speaking_wpm (int): Speaking speed in words per minute
            typing_wpm (int): Typing speed in words per minute
            subscription_type (str): Subscription type
            hourly_rate (float): Your estimated hourly rate/value of time
            daily_words (int): Average daily words for annual projections (optional)
            
        Returns:
            dict: Complete savings analysis
        """
        # Time spent speaking
        speaking_time_minutes = words_spoken / speaking_wpm
        
        # Time that would have been spent typing
        typing_time_minutes = words_spoken / typing_wpm
        
        # Time saved
        time_saved_minutes = typing_time_minutes - speaking_time_minutes

        
        # Calculate cost savings
        cost_per_minute = self.subscription_costs[subscription_type] / 60
        cost_savings = time_saved_minutes * cost_per_minute


        # Calculate break-even requirements
        
        # Calculate time saved per word spoken
        time_per_word_speaking = 1 / speaking_wpm  # minutes per word when speaking
        time_per_word_typing = 1 / typing_wpm       # minutes per word when typing
        time_saved_per_word = time_per_word_typing - time_per_word_speaking
        
        # Calculate value saved per word
        value_saved_per_word = time_saved_per_word * (hourly_rate / 60)
        
        # Calculate words needed to break even
        words_to_break_even = self.subscription_costs[subscription_type] / value_saved_per_word
        minutes_to_break_even = words_to_break_even / speaking_wpm

        # Calculate annual projections if daily words provided
        annual_data = self.calculate_annual_savings(daily_words, speaking_wpm, typing_wpm, subscription_type, hourly_rate)
        
        # Combine results
        return {
            'annual_data': annual_data,
            'summary': {
                'speaking_time_minutes': speaking_time_minutes,
                'typing_time_minutes': typing_time_minutes,
                'time_saved_minutes': time_saved_minutes,
                'cost_savings': cost_savings,
                'words_to_break_even': words_to_break_even,
                'minutes_to_break_even': minutes_to_break_even,
                'value_saved_per_word': value_saved_per_word,
                'subscription_type': subscription_type
            }
        }
    
    def format_results(self, results, hourly_rate, monthly_subscription_cost, words_spoken, speaking_wpm, typing_wpm, daily_words):
        """
        Format results for display in CLI.
        """
        annual = results.get('annual_data')
        summary = results.get('summary')
        
        output = []
        output.append("="*60)
        output.append("💰 WISPRFLOW SAVINGS ANALYSIS")
        output.append("="*60)
        output.append(f"📊 Session Data:")
        output.append(f"   Words spoken: {words_spoken}")
        output.append(f"   Speaking speed: {speaking_wpm} WPM")
        output.append(f"   Typing speed: {typing_wpm} WPM")
        output.append("")
        output.append(f"⏱️ Time Analysis:")
        output.append(f"   Time spent speaking: {summary['speaking_time_minutes']:.2f} minutes")
        output.append(f"   Time would have spent typing: {summary['typing_time_minutes']:.2f} minutes")
        output.append(f"   Time saved: {summary['time_saved_minutes']:.2f} minutes ({summary['time_saved_minutes'] / 60:.2f} hours)")
        output.append("")
        output.append(f"💵 Cost Analysis:")
        output.append(f"   Subscription: {summary['subscription_type'].replace('_', ' ').title()}")
        output.append(f"   Monthly cost: ${monthly_subscription_cost:.2f}")
        output.append(f"   Your hourly rate: ${hourly_rate:.2f}")
        output.append(f"   Value of time saved: ${summary['cost_savings']:.4f}")
        output.append("")
        output.append(f"🎯 Break-Even Analysis:")
        if summary['words_to_break_even'] != float('inf'):
            output.append(f"   Words needed to break even: {summary['words_to_break_even']:,.0f}")
            output.append(f"   Speaking time needed: {summary['minutes_to_break_even']:.1f} minutes ({summary['minutes_to_break_even'] / 60:.2f} hours)")
            output.append(f"   Value saved per word: ${summary['value_saved_per_word']:.6f}")
            
            # Calculate daily requirements
            daily_words = summary['words_to_break_even'] / 30
            daily_minutes = summary['minutes_to_break_even'] / 30
            output.append(f"   Daily requirement: {daily_words:.0f} words ({daily_minutes:.1f} minutes)")
        else:
            output.append(f"   ⚠️ Speaking slower than typing - cannot break even")
            output.append(f"   Consider improving your speaking speed or typing speed")
        
        # Add annual projections if available
        if annual:
            output.append("")
            output.append(f"📈 Annual Projections (Based on {daily_words} words/day):")
            output.append(f"   Annual words spoken: {annual['annual_words']:,}")
            output.append(f"   Annual time saved: {annual['annual_time_saved_hours']:.1f} hours")
            output.append(f"   Annual value saved: ${annual['annual_value_saved']:,.2f}")
            output.append(f"   Annual subscription cost: ${annual['annual_subscription_cost']:.2f}")
            output.append(f"   Net annual savings: ${annual['net_annual_savings']:,.2f}")
            output.append(f"   ROI: {annual['roi_percentage']:.1f}%")
            
            # Show salary equivalent
            annual_salary = hourly_rate * 2080  # 2080 working hours per year
            output.append(f"   Equivalent to {annual['net_annual_savings']/annual_salary*100:.2f}% of a ${annual_salary:,.0f} salary")
        
        output.append("="*60)
        
        return "\n".join(output)

def test_calculator():
    """
    Test the savings calculator with sample data.
    """
    print("🧮 Testing Savings Calculator...")
    
    calculator = SavingsCalculator()
    
    # Test data (similar to your WisprFlow metrics)
    words_spoken = 372
    speaking_wpm = 124
    typing_wpm = 90
    subscription_type = 'pro_monthly'
    
    # Calculate savings with $100k salary ($48.08/hour)
    hourly_rate = 50.49  # $105k salary converted to hourly
    daily_words = 500  # Assume 500 words per day usage
    
    results = calculator.calculate_complete_savings(
        words_spoken, speaking_wpm, typing_wpm, subscription_type, hourly_rate, daily_words
    )
    
    # Display results
    formatted_output = calculator.format_results(
        results,
        hourly_rate,
        calculator.subscription_costs[subscription_type],
        words_spoken,
        speaking_wpm,
        typing_wpm,
        daily_words
    )
    print(formatted_output)
    
    return results

if __name__ == "__main__":
    test_calculator()