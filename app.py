import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="BudgetBuddy AI - Smart Financial Planning",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations and responsive design
st.markdown("""
<style>
    /* Main Styles */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        animation: fadeIn 1s ease-in;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
        animation: slideUp 1s ease-out;
    }
    
    /* Animation Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-10px);}
        60% {transform: translateY(-5px);}
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeIn 1.5s ease-in;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        height: 100%;
        animation: slideUp 0.8s ease-out;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        border-color: #667eea;
        animation: pulse 2s infinite;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: bounce 2s infinite;
    }
    
    /* Interactive Elements */
    .ai-recommendation {
        background: linear-gradient(135deg, #e8f4fd 0%, #d4e7fa 100%);
        padding: 1.5rem;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        border-radius: 10px;
        transition: all 0.3s ease;
        animation: slideUp 0.6s ease-out;
    }
    
    .ai-recommendation:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .resource-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: slideUp 0.7s ease-out;
    }
    
    .resource-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .resource-link {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    
    .resource-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        color: white;
        text-decoration: none;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        transition: all 0.3s ease;
        animation: slideUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    .stat-card:hover::before {
        transform: rotate(45deg) translate(50%, 50%);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-in;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Sidebar Enhancements */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .sidebar-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .sidebar-section:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Progress Bars */
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 1rem 0;
        position: relative;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #28a745, #20c997);
        height: 100%;
        transition: width 1s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(400%); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .hero-title {
            font-size: 2rem;
        }
        
        .feature-card {
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class AIBudgetAdvisor:
    def __init__(self):
        self.income_categories = ['Salary', 'Business', 'Agriculture', 'Daily Wage', 'Other']
        self.expense_categories = ['Food', 'Housing', 'Transport', 'Healthcare', 'Education', 'Utilities', 'Other']
        
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
        
        self.learning_resources = {
            'beginner': [
                {
                    'title': 'Khan Academy - Personal Finance',
                    'url': 'https://www.khanacademy.org/college-careers-more/personal-finance',
                    'description': 'Free comprehensive personal finance course',
                    'level': 'Beginner',
                    'duration': '20 hours',
                    'icon': '🎓'
                },
                {
                    'title': 'Coursera - Financial Planning',
                    'url': 'https://www.coursera.org/learn/financial-planning',
                    'description': 'Professional financial planning course',
                    'level': 'Beginner',
                    'duration': '15 hours',
                    'icon': '📊'
                }
            ],
            'intermediate': [
                {
                    'title': 'edX - Personal Finance',
                    'url': 'https://www.edx.org/learn/personal-finance',
                    'description': 'University-level personal finance courses',
                    'level': 'Intermediate',
                    'duration': '30 hours',
                    'icon': '🏫'
                },
                {
                    'title': 'Udemy - Budgeting Masterclass',
                    'url': 'https://www.udemy.com/courses/finance-and-accounting/personal-finance/',
                    'description': 'Practical budgeting techniques and strategies',
                    'level': 'Intermediate',
                    'duration': '10 hours',
                    'icon': '💡'
                }
            ],
            'advanced': [
                {
                    'title': 'Investopedia Academy',
                    'url': 'https://academy.investopedia.com',
                    'description': 'Advanced investment and wealth management strategies',
                    'level': 'Advanced',
                    'duration': '25 hours',
                    'icon': '💼'
                },
                {
                    'title': 'MIT OpenCourseWare - Finance',
                    'url': 'https://ocw.mit.edu/courses/finance/',
                    'description': 'Advanced financial theory and applications',
                    'level': 'Advanced',
                    'duration': '40 hours',
                    'icon': '🎯'
                }
            ]
        }

    def get_currency_symbol(self, country):
        return self.country_data.get(country, {'currency': '$', 'symbol': '$'})['currency']
    
    def get_currency_display(self, country):
        return self.country_data.get(country, {'currency': '$', 'currency_name': 'US Dollar', 'symbol': '$'})
    
    def analyze_spending_patterns(self, income, expenses, country, family_size):
        total_income = sum(income.values())
        total_expenses = sum(expenses.values())
        savings = total_income - total_expenses
        
        recommendations = []
        savings_ratio = savings / total_income if total_income > 0 else 0
        
        poverty_lines = {
            'India': 5000, 'United States': 25000, 'United Kingdom': 18000,
            'European Union': 20000, 'Japan': 22000, 'Canada': 20000,
            'Australia': 22000, 'Nigeria': 4000, 'Kenya': 3500, 'Custom': 5000
        }
        
        poverty_line = poverty_lines.get(country, 5000)
        adjusted_poverty_line = poverty_line * (family_size / 4)
        
        if total_income < adjusted_poverty_line:
            recommendations.append("🎯 **Priority**: Focus on essential needs first and explore assistance programs.")
        
        if savings_ratio < 0.1:
            recommendations.append("💡 **Emergency Fund**: Try to save at least 10% of your income for emergencies")
        
        if expenses.get('Food', 0) / total_income > 0.4:
            recommendations.append("🍲 **Food Budget**: Consider buying in bulk or exploring local markets")
        
        if savings_ratio > 0.2:
            recommendations.append("🌟 **Great Job!**: You're saving well. Consider small investments")
        
        # Add more specific recommendations based on expense patterns
        if expenses.get('Transport', 0) / total_income > 0.2:
            recommendations.append("🚌 **Transport**: Consider carpooling or public transport to reduce costs")
        
        if expenses.get('Utilities', 0) / total_income > 0.15:
            recommendations.append("⚡ **Utilities**: Look into energy-efficient appliances and practices")
        
        return {
            'savings': savings,
            'savings_ratio': savings_ratio,
            'recommendations': recommendations,
            'financial_health': 'Good' if savings_ratio >= 0.1 else 'Needs Improvement',
            'poverty_line': adjusted_poverty_line,
            'above_poverty_line': total_income >= adjusted_poverty_line,
            'total_income': total_income,
            'total_expenses': total_expenses
        }

class UserStatistics:
    def __init__(self):
        self.user_data = []
    
    def add_user_data(self, country, income_level, savings_ratio, financial_health):
        self.user_data.append({
            'country': country,
            'income_level': income_level,
            'savings_ratio': savings_ratio,
            'financial_health': financial_health,
            'timestamp': datetime.now()
        })
    
    def get_statistics(self):
        if not self.user_data:
            return None
            
        df = pd.DataFrame(self.user_data)
        
        stats = {
            'total_users': len(self.user_data),
            'countries_represented': df['country'].nunique(),
            'avg_savings_ratio': df['savings_ratio'].mean(),
            'financial_health_distribution': df['financial_health'].value_counts().to_dict(),
            'top_countries': df['country'].value_counts().head(5).to_dict()
        }
        return stats

def display_hero_section():
    """Display beautiful hero section"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Take Control of Your Financial Future</div>
        <div class="hero-subtitle">AI-powered budgeting insights to help you save more, spend wisely, and achieve your financial goals</div>
    </div>
    """, unsafe_allow_html=True)

def display_features():
    """Display feature cards"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h2 style="color: #333; margin-bottom: 2rem;">Why Choose BudgetBuddy?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered Insights</h3>
            <p>Get personalized recommendations based on your spending patterns and financial goals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <h3>Global Perspective</h3>
            <p>Compare your financial health with users worldwide and get country-specific advice</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Visual Analytics</h3>
            <p>Beautiful charts and graphs to help you understand your financial situation at a glance</p>
        </div>
        """, unsafe_allow_html=True)

def display_learning_resources(ai_advisor):
    """Display external learning resources with all levels"""
    st.markdown("---")
    st.header("🎓 Continue Your Financial Journey")
    st.info("Enhance your financial knowledge with these trusted learning platforms:")
    
    # Create tabs for different levels
    tab1, tab2, tab3 = st.tabs(["🚀 Beginner", "📈 Intermediate", "🎯 Advanced"])
    
    with tab1:
        st.subheader("Start Your Financial Education")
        for resource in ai_advisor.learning_resources['beginner']:
            with st.container():
                st.markdown(f"""
                <div class="resource-card">
                    <h4>{resource['icon']} {resource['title']}</h4>
                    <p><strong>Description:</strong> {resource['description']}</p>
                    <p><strong>Level:</strong> {resource['level']} • <strong>Duration:</strong> {resource['duration']}</p>
                    <a href="{resource['url']}" target="_blank" class="resource-link">Start Learning →</a>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Build Advanced Financial Skills")
        for resource in ai_advisor.learning_resources['intermediate']:
            with st.container():
                st.markdown(f"""
                <div class="resource-card">
                    <h4>{resource['icon']} {resource['title']}</h4>
                    <p><strong>Description:</strong> {resource['description']}</p>
                    <p><strong>Level:</strong> {resource['level']} • <strong>Duration:</strong> {resource['duration']}</p>
                    <a href="{resource['url']}" target="_blank" class="resource-link">Continue Learning →</a>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Master Personal Finance")
        for resource in ai_advisor.learning_resources['advanced']:
            with st.container():
                st.markdown(f"""
                <div class="resource-card">
                    <h4>{resource['icon']} {resource['title']}</h4>
                    <p><strong>Description:</strong> {resource['description']}</p>
                    <p><strong>Level:</strong> {resource['level']} • <strong>Duration:</strong> {resource['duration']}</p>
                    <a href="{resource['url']}" target="_blank" class="resource-link">Master Skills →</a>
                </div>
                """, unsafe_allow_html=True)

def display_statistics(user_stats):
    """Display user statistics"""
    st.markdown("---")
    st.header("📊 Global Community Insights")
    st.info("Anonymous insights from BudgetBuddy users worldwide")
    
    stats = user_stats.get_statistics()
    if not stats:
        st.info("No statistics available yet. Be the first to contribute!")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>👥</h3>
            <h2>{stats['total_users']}</h2>
            <p>Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>🌍</h3>
            <h2>{stats['countries_represented']}</h2>
            <p>Countries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>💰</h3>
            <h2>{stats['avg_savings_ratio']:.1%}</h2>
            <p>Avg Savings Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        healthy_users = stats['financial_health_distribution'].get('Good', 0)
        healthy_percent = (healthy_users / stats['total_users']) * 100
        st.markdown(f"""
        <div class="stat-card">
            <h3>❤️</h3>
            <h2>{healthy_percent:.0f}%</h2>
            <p>Financial Health</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional charts
    if stats['financial_health_distribution']:
        col1, col2 = st.columns(2)
        with col1:
            health_data = pd.DataFrame({
                'Health Status': list(stats['financial_health_distribution'].keys()),
                'Count': list(stats['financial_health_distribution'].values())
            })
            fig_health = px.pie(health_data, values='Count', names='Health Status', 
                              title='Financial Health Distribution')
            st.plotly_chart(fig_health, use_container_width=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analyze' not in st.session_state:
        st.session_state.analyze = False
    if 'country' not in st.session_state:
        st.session_state.country = 'India'
    if 'user_stats' not in st.session_state:
        st.session_state.user_stats = UserStatistics()

def main():
    # Main header with animations
    st.markdown('<h1 class="main-header">💰 BudgetBuddy AI</h1>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Smart Financial Planning for Everyone</div>', unsafe_allow_html=True)
    
    # Initialize systems
    ai_advisor = AIBudgetAdvisor()
    initialize_session_state()
    
    # Show hero section and features when no analysis is done
    if not st.session_state.analyze:
        display_hero_section()
        display_features()
        
        # Quick start CTA
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center;">
                <h3>Ready to Transform Your Finances?</h3>
                <p>Get started with our AI-powered budget analysis in just a few clicks!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # This button should work now
            if st.button("🚀 Start Your Analysis Now", use_container_width=True, type="primary"):
                st.session_state.analyze = True
                st.rerun()
        
        # Show learning resources on homepage
        display_learning_resources(ai_advisor)
    
    # Sidebar - Always visible and enhanced
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #333;">🌎 Your Profile</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Country Selection
        country = st.selectbox(
            "Select Your Country",
            list(ai_advisor.country_data.keys()),
            index=0
        )
        
        # Display currency information
        currency_info = ai_advisor.get_currency_display(country)
        st.markdown(f"""
        <div class="sidebar-section">
            <h4>💰 Currency</h4>
            <p>{currency_info['currency_name']} ({currency_info['symbol']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Family information
        family_size = st.slider("Family Size", 1, 10, 4, key="family_size")
        location_type = st.selectbox("Location Type", ["Urban", "Rural", "Semi-Urban"], key="location")
        
        # Financial inputs
        st.markdown("""
        <div class="sidebar-section">
            <h4>📊 Monthly Income</h4>
        </div>
        """, unsafe_allow_html=True)
        
        currency_symbol = ai_advisor.get_currency_symbol(country)
        income = {}
        for category in ai_advisor.income_categories:
            income[category] = st.number_input(
                f"{category} ({currency_symbol})", 
                min_value=0, 
                value=0, 
                key=f"inc_{category}"
            )
        
        st.markdown("""
        <div class="sidebar-section">
            <h4>💸 Monthly Expenses</h4>
        </div>
        """, unsafe_allow_html=True)
        
        expenses = {}
        for category in ai_advisor.expense_categories:
            expenses[category] = st.number_input(
                f"{category} ({currency_symbol})", 
                min_value=0, 
                value=0, 
                key=f"exp_{category}"
            )
        
        # Analysis button
        if st.button("🔍 Analyze My Budget", use_container_width=True, type="primary"):
            st.session_state.analyze = True
            st.session_state.country = country
            st.rerun()
    
    # Main content when analysis is done
    if st.session_state.analyze:
        # AI Analysis
        analysis = ai_advisor.analyze_spending_patterns(
            income, expenses, 
            st.session_state.country, 
            family_size
        )
        
        # Add to statistics
        st.session_state.user_stats.add_user_data(
            st.session_state.country,
            analysis['total_income'],
            analysis['savings_ratio'],
            analysis['financial_health']
        )
        
        # Financial Summary with enhanced visuals
        st.header("📈 Your Financial Analysis")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("Total Monthly Income", f"{currency_symbol}{analysis['total_income']:,}")
        
        with summary_col2:
            st.metric("Total Monthly Expenses", f"{currency_symbol}{analysis['total_expenses']:,}")
        
        with summary_col3:
            st.metric("Monthly Savings", f"{currency_symbol}{analysis['savings']:,}", 
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
        col1, col2 = st.columns(2)
        
        with col1:
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Bar(
                name='Income',
                x=['Total'],
                y=[analysis['total_income']],
                marker_color='#28a745'
            ))
            fig_compare.add_trace(go.Bar(
                name='Expenses',
                x=['Total'],
                y=[analysis['total_expenses']],
                marker_color='#dc3545'
            ))
            fig_compare.update_layout(
                title=f"Income vs Expenses ({currency_symbol})",
                yaxis_title=f"Amount ({currency_symbol})"
            )
            st.plotly_chart(fig_compare, use_container_width=True)
        
        with col2:
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
        
        # AI Recommendations with enhanced styling
        st.header("🤖 Your Personalized Recommendations")
        for recommendation in analysis['recommendations']:
            st.markdown(f'<div class="ai-recommendation">{recommendation}</div>', 
                       unsafe_allow_html=True)
        
        # Financial Health Score with progress bar
        st.subheader("🏥 Financial Health Score")
        health_score = min(100, max(0, int(analysis['savings_ratio'] * 200)))
        
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-fill" style="width: {health_score}%"></div>
        </div>
        <p style="text-align: center; font-weight: bold; margin-top: 0.5rem;">{health_score}/100</p>
        """, unsafe_allow_html=True)
        
        if health_score >= 70:
            st.success("👍 Excellent Financial Health - You're doing great!")
        elif health_score >= 40:
            st.warning("⚠️ Fair - There's room for improvement")
        else:
            st.error("🚨 Needs Attention - Let's work on improving your financial health")
        
        # Display additional sections
        display_statistics(st.session_state.user_stats)
        display_learning_resources(ai_advisor)

if __name__ == "__main__":
    main()
