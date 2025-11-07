import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="BudgetBuddy AI - Poverty Alleviation",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .ai-recommendation {
        background-color: #e8f4fd;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .resource-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .resource-link {
        color: #1f77b4;
        text-decoration: none;
        font-weight: bold;
    }
    .resource-link:hover {
        color: #0056b3;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

class AIBudgetAdvisor:
    def __init__(self):
        self.income_categories = ['Salary', 'Business', 'Agriculture', 'Daily Wage', 'Other']
        self.expense_categories = ['Food', 'Housing', 'Transport', 'Healthcare', 'Education', 'Utilities', 'Other']
        
        # Country and currency data
        self.country_data = {
            'India': {'currency': '₹', 'currency_name': 'Indian Rupee', 'symbol': '₹'},
            'United States': {'currency': '$', 'currency_name': 'US Dollar', 'symbol': '$'},
            'United Kingdom': {'currency': '£', 'currency_name': 'British Pound', 'symbol': '£'},
            'European Union': {'currency': '€', 'currency_name': 'Euro', 'symbol': '€'},
            'Japan': {'currency': '¥', 'currency_name': 'Japanese Yen', 'symbol': '¥'},
            'Canada': {'currency': 'C$', 'currency_name': 'Canadian Dollar', 'symbol': 'C$'},
            'Australia': {'currency': 'A$', 'currency_name': 'Australian Dollar', 'symbol': 'A$'},
            'Nigeria': {'currency': '₦', 'currency_name': 'Nigerian Naira', 'symbol': '₦'},
            'Kenya': {'currency': 'KSh', 'currency_name': 'Kenyan Shilling', 'symbol': 'KSh'},
            'Custom': {'currency': '', 'currency_name': 'Custom Currency', 'symbol': ''}
        }
        
        # Real resources database
        self.resources = {
            'India': {
                'financial_literacy': [
                    {"name": "National Centre for Financial Education", "url": "https://www.ncfe.org.in", "description": "Free financial literacy courses and resources"},
                    {"name": "Pocket Money Management App", "url": "https://groww.in", "description": "Indian investment and savings platform"},
                ],
                'government_schemes': [
                    {"name": "PM Jan Dhan Yojana", "url": "https://pmjdy.gov.in", "description": "Zero-balance bank accounts for all"},
                    {"name": "MGNREGA Employment", "url": "https://nrega.nic.in", "description": "Rural employment guarantee scheme"},
                ],
                'community_support': [
                    {"name": "Goonj - Resource Mobilization", "url": "https://goonj.org", "description": "Community development and resource sharing"},
                    {"name": "GiveIndia", "url": "https://giveindia.org", "description": "Platform for donors and NGOs"},
                ]
            },
            'United States': {
                'financial_literacy': [
                    {"name": "MyMoney.gov", "url": "https://www.mymoney.gov", "description": "US government financial education"},
                    {"name": "Consumer Financial Protection Bureau", "url": "https://www.consumerfinance.gov", "description": "Financial tools and resources"},
                ],
                'government_schemes': [
                    {"name": "SNAP Benefits", "url": "https://www.fns.usda.gov/snap", "description": "Supplemental Nutrition Assistance Program"},
                    {"name": "Medicaid", "url": "https://www.medicaid.gov", "description": "Healthcare for low-income families"},
                ],
                'community_support': [
                    {"name": "Feeding America", "url": "https://www.feedingamerica.org", "description": "National food bank network"},
                    {"name": "United Way", "url": "https://www.unitedway.org", "description": "Community support services"},
                ]
            },
            'United Kingdom': {
                'financial_literacy': [
                    {"name": "Money Helper", "url": "https://www.moneyhelper.org.uk", "description": "Free financial guidance"},
                    {"name": "Citizens Advice", "url": "https://www.citizensadvice.org.uk", "description": "Money and legal advice"},
                ],
                'government_schemes': [
                    {"name": "Universal Credit", "url": "https://www.gov.uk/universal-credit", "description": "Social security payment"},
                    {"name": "Food Banks - Trussell Trust", "url": "https://www.trusselltrust.org", "description": "Emergency food support"},
                ],
                'community_support': [
                    {"name": "Local Food Banks", "url": "https://www.foodbank.org.uk", "description": "Find nearby food banks"},
                    {"name": "Shelter UK", "url": "https://www.shelter.org.uk", "description": "Housing and homelessness charity"},
                ]
            },
            'General': {
                'online_learning': [
                    {"name": "Khan Academy - Personal Finance", "url": "https://www.khanacademy.org/college-careers-more/personal-finance", "description": "Free financial education courses"},
                    {"name": "Coursera Financial Literacy", "url": "https://www.coursera.org/courses?query=financial%20literacy", "description": "Free and paid finance courses"},
                ],
                'budgeting_tools': [
                    {"name": "Google Sheets Templates", "url": "https://docs.google.com/spreadsheets", "description": "Free budget templates"},
                    {"name": "Excel Budget Templates", "url": "https://templates.office.com/en-us/budgets", "description": "Microsoft Office templates"},
                ],
                'emergency_support': [
                    {"name": "Local Community Centers", "url": "#", "description": "Check your local municipal website"},
                    {"name": "Religious Organizations", "url": "#", "description": "Many offer food and support services"},
                ]
            }
        }
    
    def get_currency_symbol(self, country):
        """Get currency symbol for selected country"""
        return self.country_data.get(country, {'currency': '$', 'symbol': '$'})['currency']
    
    def get_currency_display(self, country):
        """Get full currency display info"""
        return self.country_data.get(country, {'currency': '$', 'currency_name': 'US Dollar', 'symbol': '$'})
    
    def get_country_specific_tips(self, country, income_level):
        """Get country-specific financial tips"""
        tips = []
        
        if country == 'India':
            tips.extend([
                "🇮🇳 **India Specific**: Explore PMJDY for zero-balance accounts",
                "🍚 **Food**: Use PDS ration shops for subsidized grains",
            ])
        elif country == 'United States':
            tips.extend([
                "🇺🇸 **US Specific**: Explore SNAP benefits for food assistance",
                "🏠 **Housing**: Check Section 8 housing programs",
            ])
        elif country == 'United Kingdom':
            tips.extend([
                "🇬🇧 **UK Specific**: Check Universal Credit benefits",
                "🏠 **Housing**: Explore housing benefit schemes",
            ])
        
        # General tips for all countries
        tips.extend([
            "📱 **Digital Tools**: Use mobile banking to track expenses",
            "🏘️ **Community**: Join local savings groups",
        ])
        
        return tips
    
    def get_country_resources(self, country):
        """Get resources for specific country, fallback to General if not found"""
        return self.resources.get(country, self.resources['General'])
    
    def analyze_spending_patterns(self, income, expenses, country, family_size):
        """AI-powered analysis of spending patterns with country context"""
        total_income = sum(income.values())
        total_expenses = sum(expenses.values())
        savings = total_income - total_expenses
        
        # AI Recommendation Engine
        recommendations = []
        
        # Basic financial health assessment
        savings_ratio = savings / total_income if total_income > 0 else 0
        
        # Country-specific poverty line approximations (monthly for family of 4)
        poverty_lines = {
            'India': 5000, 'United States': 25000, 'United Kingdom': 18000,
            'European Union': 20000, 'Japan': 22000, 'Canada': 20000,
            'Australia': 22000, 'Nigeria': 4000, 'Kenya': 3500, 'Custom': 5000
        }
        
        poverty_line = poverty_lines.get(country, 5000)
        adjusted_poverty_line = poverty_line * (family_size / 4)  # Adjust for family size
        
        # Financial health assessment
        if total_income < adjusted_poverty_line:
            recommendations.append(f"🎯 **Priority**: Focus on essential needs first and explore assistance programs.")
        
        if savings_ratio < 0.1:
            recommendations.append("💡 **Emergency Fund**: Try to save at least 10% of your income for emergencies")
        
        if expenses.get('Food', 0) / total_income > 0.4:
            recommendations.append("🍲 **Food Budget**: Consider buying in bulk or exploring local markets")
        
        if savings_ratio > 0.2:
            recommendations.append("🌟 **Great Job!**: You're saving well. Consider small investments")
        
        # Add country-specific tips
        recommendations.extend(self.get_country_specific_tips(country, total_income))
        
        return {
            'savings': savings,
            'savings_ratio': savings_ratio,
            'recommendations': recommendations,
            'financial_health': 'Good' if savings_ratio >= 0.1 else 'Needs Improvement',
            'poverty_line': adjusted_poverty_line,
            'above_poverty_line': total_income >= adjusted_poverty_line
        }

def display_resources_section(country, currency_symbol):
    """Display actual useful resources with links"""
    ai_advisor = AIBudgetAdvisor()
    country_resources = ai_advisor.get_country_resources(country)
    
    st.markdown("---")
    st.subheader("🎯 Actionable Resources & Next Steps")
    st.info(f"**Selected Country**: {country} | **Resources tailored for your location**")
    
    # Create tabs for different resource types
    tab1, tab2, tab3 = st.tabs(["💰 Financial Education", "🏛️ Government Schemes", "🤝 Community Support"])
    
    with tab1:
        st.subheader("Learn Financial Skills")
        resources = country_resources.get('financial_literacy', []) + ai_advisor.resources['General']['online_learning']
        
        for resource in resources:
            with st.container():
                st.markdown(f"""
                <div class="resource-card">
                    <h4>🔗 {resource['name']}</h4>
                    <p>{resource['description']}</p>
                    <a href="{resource['url']}" target="_blank" class="resource-link">Visit Website →</a>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Government Assistance Programs")
        resources = country_resources.get('government_schemes', [])
        
        if resources:
            for resource in resources:
                with st.container():
                    st.markdown(f"""
                    <div class="resource-card">
                        <h4>🏛️ {resource['name']}</h4>
                        <p>{resource['description']}</p>
                        <a href="{resource['url']}" target="_blank" class="resource-link">Learn More →</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Check your local government website for assistance programs")
    
    with tab3:
        st.subheader("Local Community Support")
        resources = country_resources.get('community_support', []) + ai_advisor.resources['General']['emergency_support']
        
        for resource in resources:
            with st.container():
                if resource['url'] != '#':
                    link_html = f'<a href="{resource["url"]}" target="_blank" class="resource-link">Get Help →</a>'
                else:
                    link_html = '<span style="color: #666;">Search locally for this resource</span>'
                
                st.markdown(f"""
                <div class="resource-card">
                    <h4>🤝 {resource['name']}</h4>
                    <p>{resource['description']}</p>
                    {link_html}
                </div>
                """, unsafe_allow_html=True)
        
        # Additional quick tips
        st.markdown("### 💡 Quick Actions You Can Take Today:")
        quick_actions = [
            "📞 **Call local helpline** for immediate assistance",
            "🔍 **Google** '[Your City] + food bank' or '[Your City] + financial assistance'",
            "📱 **Download** a free budgeting app from your app store",
            "🏦 **Visit** your local bank for basic savings account options"
        ]
        
        for action in quick_actions:
            st.write(f"• {action}")

def main():
    st.markdown('<h1 class="main-header">💰 BudgetBuddy AI - Smart Financial Planning</h1>', unsafe_allow_html=True)
    st.markdown("### 🌍 AI-Powered Budgeting for Families Worldwide")
    
    # Initialize AI advisor
    ai_advisor = AIBudgetAdvisor()
    
    # Initialize session state
    if 'analyze' not in st.session_state:
        st.session_state.analyze = False
    if 'country' not in st.session_state:
        st.session_state.country = 'India'
    
    # Sidebar for user input
    with st.sidebar:
        st.header("🌎 Your Profile")
        
        # Country Selection
        country = st.selectbox(
            "Select Your Country",
            list(ai_advisor.country_data.keys()),
            index=0  # Default to India
        )
        
        # Display currency information
        currency_info = ai_advisor.get_currency_display(country)
        st.info(f"**Currency**: {currency_info['currency_name']} ({currency_info['symbol']})")
        
        # Family size and location for better recommendations
        family_size = st.slider("Family Size", 1, 10, 4)
        location_type = st.selectbox("Location Type", ["Urban", "Rural", "Semi-Urban"])
        
        st.header("📊 Your Financial Profile")
        
        # Get currency symbol for inputs
        currency_symbol = ai_advisor.get_currency_symbol(country)
        
        # Monthly Income
        st.subheader("Monthly Income")
        income = {}
        for category in ai_advisor.income_categories:
            income[category] = st.number_input(
                f"{category} ({currency_symbol})", 
                min_value=0, 
                value=0, 
                key=f"inc_{category}"
            )
        
        # Monthly Expenses
        st.subheader("Monthly Expenses")
        expenses = {}
        for category in ai_advisor.expense_categories:
            expenses[category] = st.number_input(
                f"{category} ({currency_symbol})", 
                min_value=0, 
                value=0, 
                key=f"exp_{category}"
            )
        
        if st.button("🔍 Analyze My Budget", type="primary"):
            st.session_state.analyze = True
            st.session_state.country = country

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.analyze:
            # AI Analysis
            analysis = ai_advisor.analyze_spending_patterns(
                income, expenses, 
                st.session_state.country, 
                family_size
            )
            
            # Financial Summary
            st.subheader("📈 Financial Summary")
            
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                total_income = sum(income.values())
                st.metric("Total Monthly Income", f"{currency_symbol}{total_income:,}")
            
            with summary_col2:
                total_expenses = sum(expenses.values())
                st.metric("Total Monthly Expenses", f"{currency_symbol}{total_expenses:,}")
            
            with summary_col3:
                savings = analysis['savings']
                st.metric("Monthly Savings", f"{currency_symbol}{savings:,}", 
                         delta=f"{analysis['savings_ratio']:.1%}")
            
            with summary_col4:
                poverty_status = "Above" if analysis['above_poverty_line'] else "Below"
                poverty_color = "normal" if analysis['above_poverty_line'] else "off"
                st.metric(
                    "Poverty Line Status", 
                    poverty_status,
                    delta=f"Est: {currency_symbol}{analysis['poverty_line']:,.0f}",
                    delta_color=poverty_color
                )
            
            # Visualizations
            tab1, tab2 = st.tabs(["Income vs Expenses", "Spending Breakdown"])
            
            with tab1:
                # Income vs Expenses chart
                fig_compare = go.Figure()
                fig_compare.add_trace(go.Bar(
                    name='Income',
                    x=['Total'],
                    y=[total_income],
                    marker_color='green'
                ))
                fig_compare.add_trace(go.Bar(
                    name='Expenses',
                    x=['Total'],
                    y=[total_expenses],
                    marker_color='red'
                ))
                fig_compare.update_layout(
                    title=f"Income vs Expenses ({currency_symbol})",
                    yaxis_title=f"Amount ({currency_symbol})"
                )
                st.plotly_chart(fig_compare, use_container_width=True)
            
            with tab2:
                # Expense breakdown
                expense_data = {k: v for k, v in expenses.items() if v > 0}
                if expense_data:
                    fig_expenses = px.pie(
                        values=list(expense_data.values()),
                        names=list(expense_data.keys()),
                        title=f"Expense Distribution ({currency_symbol})"
                    )
                    st.plotly_chart(fig_expenses, use_container_width=True)
                else:
                    st.info("No expense data to display")
    
    with col2:
        if st.session_state.analyze:
            # Country Info
            st.subheader(f"🇺🇳 {st.session_state.country}")
            st.write(f"**Currency**: {currency_info['currency_name']} ({currency_symbol})")
            
            # AI Recommendations
            st.subheader("🤖 AI Recommendations")
            
            for recommendation in analysis['recommendations']:
                st.markdown(f'<div class="ai-recommendation">{recommendation}</div>', 
                           unsafe_allow_html=True)
            
            # Financial Health Score
            st.subheader("🏥 Financial Health")
            health_score = min(100, max(0, int(analysis['savings_ratio'] * 200)))
            
            if health_score >= 70:
                st.success(f"Score: {health_score}/100 - 👍 Good")
            elif health_score >= 40:
                st.warning(f"Score: {health_score}/100 - ⚠️ Fair")
            else:
                st.error(f"Score: {health_score}/100 - 🚨 Needs Attention")
            
            # Quick Budget Tips
            st.subheader("💡 Quick Tips")
            tips = [
                "Track every expense for 30 days",
                "Cook at home instead of eating out",
                "Use public transportation when possible",
                "Buy generic brands for daily essentials"
            ]
            
            for tip in tips:
                st.write(f"• {tip}")
    
    # Display resources section only when analysis is done
    if st.session_state.analyze:
        display_resources_section(st.session_state.country, currency_symbol)

if __name__ == "__main__":
    main()
