    def get_response_time_by_tier(self, tier, event_type):
        """Calculate response time based on tier (Premium users get better performance)"""
        base_times = {
            'login': (500, 2000),
            'dashboard_view': (300, 1500),
            'advanced_analytics': (1000, 5000),
            'api_integration': (200, 1000),
            'error_event': (50, 500)
        }
        
        base_range = base_times.get(event_type, (300, 1800))
        
        # Performance multipliers by tier
        tier_multipliers = {
            'Premium': 0.7,    # 30% faster (better infrastructure)
            'Basic': 0.9,      # 10% faster than free
            'Free': 1.0,       # Baseline performance
            'Cancelled': 1.3   # Slower (degraded access)
        }
        
        multiplier = tier_multipliers.get(tier, 1.0)
        base_time = random.randint(*base_range)
        return int(base_time * multiplier)
    
    def get_payment_status(self, tier):
        """Get payment status based on tier"""
        if tier in ['Basic', 'Premium']:
            return random.choice(['current', 'past_due', 'failed'], p=[0.92, 0.06, 0.02])
        elif tier == 'Free':
            return 'n/a'
        else:  # Cancelled
            return 'cancelled'
    
    def calculate_churn_risk_score(self, tier, segment):
        """Calculate churn risk based on tier and segment"""
        base_scores = {
            'Premium': {'champion': 5, 'engaged': 10, 'casual': 25, 'at_risk': 60},
            'Basic': {'champion': 15, 'engaged': 25, 'casual': 45, 'at_risk': 75},
            'Free': {'conversion_ready': 20, 'engaged': 35, 'casual': 55, 'at_risk': 85},
            'Cancelled': {'at_risk': 95}
        }
        
        base_score = base_scores.get(tier, {}).get(segment, 50)
        return base_score + random.randint(-10, 15)
    
    def calculate_conversion_propensity(self, tier, segment, event_type):
        """Calculate conversion propensity (Free→Paid or Basic→Premium)"""
        if tier == 'Free':
            base_scores = {'conversion_ready': 75, 'engaged': 35, 'casual': 10, 'at_risk': 5}
            boost = 20 if event_type in ['usage_limit_hit', 'premium_feature_explore', 'pricing_page_view'] else 0
        elif tier == 'Basic':
            base_scores = {'champion': 60, 'engaged': 25, 'casual': 5, 'at_risk': 2}
            boost = 15 if event_type in ['enterprise_trial', 'team_management_view', 'api_exploration'] else 0
        else:
            return 0  # Premium and Cancelled users don't convert up
        
        base_score = base_scores.get(segment, 10)
        return min(95, base_score + boost + random.randint(-10, 10))
    
    def calculate_upsell_propensity(self, tier, segment, event_type):
        """Calculate upsell propensity (Basic→Premium)"""
        if tier != 'Basic':
            return 0  # Only Basic users can upsell to Premium
        
        base_scores = {'champion': 70, 'engaged': 40, 'casual': 15, 'at_risk': 5}
        boost = 20 if event_type in ['advanced_feature_usage', 'enterprise_trial', 'team_management_view'] else 0
        
        base_score = base_scores.get(segment, 20)
        return min(95, base_score + boost + random.randint(-5, 10))
    
    def calculate_retention_probability(self, tier, segment):
        """Calculate retention probability"""
        retention_scores = {
            'Premium': {'champion': 95, 'engaged': 90, 'casual': 80, 'at_risk': 60},
            'Basic': {'champion': 85, 'engaged': 75, 'casual': 60, 'at_risk': 40},
            'Free': {'conversion_ready': 70, 'engaged': 50, 'casual': 30, 'at_risk': 15},
            'Cancelled': {'at_risk': 5}
        }
        
        base_score = retention_scores.get(tier, {}).get(segment, 50)
        return base_score + random.randint(-10, 10)
    
    def get_next_best_action_by_scenario(self, plg_scenario, event_type):
        """Get next best action based on PLG scenario"""
        scenario_actions = {
            'CAC/Conversion': ['upgrade_trial_offer', 'usage_limit_education', 'value_demonstration', 'pricing_consultation'],
            'PLG/Upsell': ['premium_feature_demo', 'team_expansion_consultation', 'api_integration_support', 'enterprise_trial'],
            'Failed Conversion': ['retention_outreach', 'onboarding_restart', 'success_coaching', 'feature_education'],
            'Churn': ['immediate_intervention', 'value_recovery_program', 'win_back_offer', 'exit_interview'],
            'Winback': ['reactivation_offer', 'competitive_analysis', 'success_story_sharing', 'special_pricing'],
            'Retention': ['engagement_optimization', 'feature_recommendation', 'success_measurement', 'community_involvement']
        }
        
        actions = scenario_actions.get(plg_scenario, ['standard_engagement'])
        return random.choice(actions)
    
    def get_intervention_priority_by_tier(self, tier, segment, event_type):
        """Calculate intervention priority based on tier, segment, and event"""
        # High priority conditions
        if segment == 'at_risk' and tier in ['Basic', 'Premium']:
            return 'high'  # Paying customers at risk = high priority
        if tier == 'Free' and segment == 'conversion_ready' and event_type in ['usage_limit_hit', 'pricing_page_view']:
            return 'high'  # Hot conversion leads = high priority
        if event_type in ['support_ticket_create', 'payment_issue_check', 'competitor_comparison']:
            return 'high'  # Critical events = high priority
        
        # Medium priority conditions
        if tier in ['Basic', 'Premium'] and segment in ['engaged', 'casual']:
            return 'medium'  # Paying customers = medium priority
        if tier == 'Free' and segment in ['conversion_ready', 'engaged']:
            return 'medium'  # Potential converts = medium priority
        
        # Low priority (everything else)
        return 'low'
    
    def is_tier_transition_candidate(self, user_profile, event_type):
        """Determine if user is a candidate for tier transition"""
        tier = user_profile['tier']
        segment = user_profile['segment']
        
        if tier == 'Free' and segment == 'conversion_ready':
            return 'free_to_paid_candidate'
        elif tier == 'Basic' and segment == 'champion':
            return 'basic_to_premium_candidate'
        elif segment == 'at_risk' and tier in ['Basic', 'Premium']:
            return 'churn_risk_candidate'
        elif tier == 'Cancelled':
            return 'winback_candidate'
        else:
            return 'stable'
    
    def add_tier_specific_context(self, event, event_type, user_profile):
        """Add tier-specific context to events"""
        tier = user_profile['tier']
        
        # Free tier specific fields
        if tier == 'Free':
            if event_type == 'usage_limit_hit':
                event.update({
                    'limit_type': random.choice(['reports', 'data_export', 'api_calls', 'storage']),
                    'usage_percentage': random.randint(95    def generate_session_events(self, user_profile, session_count=1):
        """Generate events for a user session following tier-based PLG patterns"""
        events = []
        tier = user_profile['tier']
        segment = user_profile['segment']
        
        for session_num in range(session_count):
            # Get tier-specific session patterns
            tier_patterns = self.tier_session_patterns.get(tier, self.tier_session_patterns['Free'])
            segment_patterns = tier_patterns.get(segment, {'basic_usage': ['login', 'dashboard_view', 'logout']})
            
            # Select pattern randomly from available patterns for this tier/segment
            if segment_patterns:
                pattern_name = random.choice(list(segment_patterns.keys()))
                event_sequence = segment_patterns[pattern_name]
            else:
                pattern_name = 'basic_usage'
                event_sequence = ['login', 'dashboard_view', 'logout']
            #!/usr/bin/env python3
"""
PLG Product Telemetry Data Generator
Generates 1000 realistic telemetry records for Salesforce Data Cloud demo
Based on Product Led Growth behavioral patterns and user segmentation

Run in Google Colab: https://colab.research.google.com/
"""

import pandas as pd
import numpy as np
import random
import uuid
from datetime import datetime, timedelta
import json

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

class PLGTelemetryGenerator:
    def __init__(self):
        # Tier Distribution (based on typical SaaS metrics)
        self.tier_weights = {
            'Free': 0.60,        # 60% - Freemium users (conversion targets)
            'Basic': 0.25,       # 25% - Paid tier 1 (upsell targets)  
            'Premium': 0.12,     # 12% - Paid tier 2 (retention focus)
            'Cancelled': 0.03    # 3% - Churned users (win-back targets)
        }
        
        # PLG Scenario Mapping based on Tier combinations
        self.plg_scenarios = {
            'CAC/Conversion': {
                'from_tier': 'Free',
                'to_tier': ['Basic', 'Premium'],
                'behavioral_indicators': ['usage_limit_hit', 'premium_feature_explore', 'pricing_page_view']
            },
            'PLG/Upsell': {
                'from_tier': 'Basic', 
                'to_tier': 'Premium',
                'behavioral_indicators': ['advanced_feature_usage', 'team_management_view', 'enterprise_feature_trial']
            },
            'Failed Conversion': {
                'from_tier': 'Free',
                'to_tier': 'Cancelled', 
                'behavioral_indicators': ['feature_abandon', 'error_event', 'support_ticket_create']
            },
            'Churn': {
                'from_tier': ['Basic', 'Premium'],
                'to_tier': 'Cancelled',
                'behavioral_indicators': ['declining_usage', 'payment_failed', 'competitor_evaluation']
            }
        }
        
        # User Segment Distribution - now mapped to tiers
        self.segment_tier_mapping = {
            'Free': {
                'conversion_ready': 0.15,  # Ready to convert to paid
                'engaged': 0.25,           # Getting value, might convert
                'casual': 0.50,            # Light usage
                'at_risk': 0.10            # Likely to cancel
            },
            'Basic': {
                'champion': 0.10,          # Power users ready for Premium
                'engaged': 0.60,           # Satisfied Basic users
                'casual': 0.25,            # Light Basic usage  
                'at_risk': 0.05            # Churn risk
            },
            'Premium': {
                'champion': 0.70,          # Most Premium users are champions
                'engaged': 0.25,           # Solid Premium users
                'casual': 0.03,            # Unlikely but possible
                'at_risk': 0.02            # Very low churn on Premium
            },
            'Cancelled': {
                'at_risk': 1.0             # All cancelled users are at-risk (for win-back)
            }
        }
        
        # Session patterns now organized by tier and scenario
        self.tier_session_patterns = {
            'Free': {
                'conversion_ready': {
                    'conversion_signal': ['login', 'core_feature_usage', 'usage_limit_hit', 'premium_feature_explore', 'pricing_page_view', 'paywall_encounter', 'logout'],
                    'value_realization': ['login', 'workflow_start', 'data_analysis', 'insight_discovery', 'share_result', 'usage_limit_hit', 'logout']
                },
                'engaged': {
                    'steady_usage': ['login', 'dashboard_check', 'basic_analytics', 'report_generate', 'logout'],
                    'exploration': ['login', 'feature_discovery', 'workflow_attempt', 'basic_success', 'logout']
                },
                'casual': {
                    'basic_usage': ['login', 'dashboard_view', 'basic_feature_try', 'logout'],
                    'onboarding': ['login', 'welcome_tour', 'basic_feature_try', 'help_view', 'logout']
                },
                'at_risk': {
                    'declining_session': ['login', 'dashboard_view', 'feature_attempt', 'error_event', 'feature_abandon', 'logout'],
                    'frustration': ['login', 'feature_attempt', 'error_event', 'help_search', 'logout']
                }
            },
            'Basic': {
                'champion': {
                    'upsell_exploration': ['login', 'advanced_feature_usage', 'team_management_view', 'premium_feature_explore', 'enterprise_trial', 'logout'],
                    'power_usage': ['login', 'advanced_analytics', 'data_export', 'team_sharing', 'api_exploration', 'logout']
                },
                'engaged': {
                    'steady_usage': ['login', 'dashboard_analytics', 'report_generate', 'team_collaborate', 'logout'],
                    'feature_adoption': ['login', 'new_feature_try', 'workflow_success', 'share_result', 'logout']
                },
                'casual': {
                    'basic_usage': ['login', 'dashboard_check', 'simple_report', 'logout'],
                    'maintenance': ['login', 'account_settings', 'basic_feature', 'logout']
                },
                'at_risk': {
                    'declining_usage': ['login', 'dashboard_view', 'payment_issue_check', 'logout'],
                    'support_heavy': ['login', 'feature_attempt', 'error_event', 'support_ticket_create', 'logout']
                }
            },
            'Premium': {
                'champion': {
                    'power_session': ['login', 'advanced_analytics', 'custom_dashboard_create', 'api_integration', 'team_admin', 'automation_setup', 'logout'],
                    'collaboration': ['login', 'team_workspace', 'advanced_sharing', 'cross_team_analytics', 'enterprise_reporting', 'logout'],
                    'viral_behavior': ['login', 'success_showcase', 'external_demo', 'referral_program', 'thought_leadership', 'logout']
                },
                'engaged': {
                    'advanced_usage': ['login', 'premium_analytics', 'advanced_reporting', 'team_management', 'logout'],
                    'optimization': ['login', 'workflow_optimization', 'advanced_features', 'performance_tuning', 'logout']
                },
                'casual': {
                    'premium_basic': ['login', 'premium_dashboard', 'standard_analytics', 'logout']
                },
                'at_risk': {
                    'value_questioning': ['login', 'basic_feature_only', 'cost_review', 'competitor_comparison', 'logout']
                }
            },
            'Cancelled': {
                'at_risk': {
                    'winback_attempt': ['login', 'account_reactivation_view', 'special_offer_view', 'logout'],
                    'data_export': ['login', 'data_export_final', 'account_closure_prep', 'logout']
                }
            }
        }
        
        # Feature sophistication mapping (from PLG behavioral modeling)
        self.feature_sophistication = {
            'basic': ['login', 'logout', 'dashboard_view', 'basic_feature_try', 'help_view'],
            'intermediate': ['data_analysis', 'report_generate', 'workflow_attempt', 'core_feature_usage'],
            'advanced': ['advanced_analytics', 'custom_dashboard_create', 'api_integration', 'team_sharing'],
            'expert': ['custom_configuration', 'automation_setup', 'enterprise_feature_trial', 'admin_settings_explore']
        }
        
        # Updated feature mapping with tier-specific features
        self.feature_mapping = {
            # Authentication & Core
            'login': 'Authentication System',
            'logout': 'Authentication System',
            'dashboard_view': 'Executive Dashboard',
            'dashboard_check': 'Quick Dashboard Check',
            'dashboard_analytics': 'Analytics Dashboard',
            'premium_dashboard': 'Premium Dashboard Suite',
            
            # Free Tier Features
            'basic_feature_try': 'Basic Analytics',
            'basic_analytics': 'Basic Reporting',
            'workflow_attempt': 'Basic Workflow Engine',
            'welcome_tour': 'Product Onboarding',
            'feature_discovery': 'Feature Discovery',
            
            # Conversion Signals (Free → Paid)
            'core_feature_usage': 'Core Analytics Engine',
            'usage_limit_hit': 'Usage Limit System',
            'premium_feature_explore': 'Premium Feature Preview',
            'pricing_page_view': 'Pricing Information',
            'paywall_encounter': 'Upgrade Prompts',
            
            # Basic Tier Features
            'advanced_analytics': 'Advanced Analytics Suite',
            'team_collaborate': 'Team Collaboration',
            'data_export': 'Data Export Engine',
            'report_generate': 'Report Generator',
            'new_feature_try': 'Feature Adoption',
            
            # Upsell Signals (Basic → Premium)  
            'team_management_view': 'Team Management Console',
            'enterprise_trial': 'Enterprise Feature Trial',
            'api_exploration': 'API Gateway Preview',
            'advanced_feature_usage': 'Advanced Feature Suite',
            
            # Premium Tier Features
            'custom_dashboard_create': 'Custom Dashboard Builder',
            'api_integration': 'API Integration Hub',
            'automation_setup': 'Workflow Automation',
            'team_admin': 'Team Administration',
            'enterprise_reporting': 'Enterprise Reporting Suite',
            'cross_team_analytics': 'Cross-Team Analytics',
            'advanced_sharing': 'Advanced Sharing & Permissions',
            
            # Churn/Risk Indicators
            'error_event': 'Error Handling System',
            'feature_abandon': 'User Experience Analytics',
            'support_ticket_create': 'Support System',
            'payment_issue_check': 'Payment Management',
            'competitor_comparison': 'Competitive Analysis',
            'cost_review': 'Cost Analysis Tools',
            
            # Success/Value Events
            'insight_discovery': 'AI Insights Engine',
            'workflow_success': 'Success Analytics',
            'share_result': 'Results Sharing',
            'success_showcase': 'Success Showcase',
            'external_demo': 'External Demonstration',
            
            # Cancelled/Winback
            'account_reactivation_view': 'Account Reactivation',
            'special_offer_view': 'Winback Offers',
            'data_export_final': 'Data Export & Migration',
            'account_closure_prep': 'Account Closure'
        }
        
        # Base data arrays
        self.product_names = ['CloudTech Analytics Platform', 'DataViz Pro', 'Enterprise Dashboard']
        self.device_types = ['desktop', 'mobile', 'tablet', 'api_client']
        self.browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
        self.operating_systems = ['Windows 11', 'macOS', 'iOS', 'Android', 'Linux']
        self.regions = ['CA', 'NY', 'TX', 'WA', 'FL', 'IL', 'GA', 'MA', 'OR', 'CO']
        self.cities = ['San Francisco', 'New York', 'Austin', 'Seattle', 'Miami', 'Chicago', 'Atlanta', 'Boston', 'Portland', 'Denver']
        
        # Sample names for demo users (using example.com domain)
        self.first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Quinn', 'Avery', 'Cameron', 'Drew',
                           'Blake', 'Sage', 'River', 'Phoenix', 'Skyler', 'Rowan', 'Finley', 'Harper', 'Emery', 'Parker']
        self.last_names = ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez']
        
    def generate_user_profile(self, user_index):
        """Generate a user profile with tier and segment assignment"""
        # Select tier based on realistic distribution
        tier = np.random.choice(list(self.tier_weights.keys()), p=list(self.tier_weights.values()))
        
        # Select segment based on tier
        segment_weights = self.segment_tier_mapping.get(tier, {'casual': 1.0})
        segment = np.random.choice(list(segment_weights.keys()), p=list(segment_weights.values()))
        
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        
        return {
            'user_id': f'user_{first_name.lower()}_{last_name.lower()}_{user_index:04d}',
            'external_id': f'EXT_{user_index:06d}',
            'first_name': first_name,
            'last_name': last_name,
            'email': f'{first_name.lower()}.{last_name.lower()}@example.com',
            'tier': tier,
            'segment': segment,
            'title': self.get_title_for_tier_segment(tier, segment),
            'department': random.choice(['Sales', 'Marketing', 'IT', 'Operations', 'Finance', 'HR']),
            'phone': f'555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'plg_scenario': self.determine_plg_scenario(tier, segment)
        }
    
    def get_title_for_tier_segment(self, tier, segment):
        """Assign realistic titles based on tier and segment"""
        if tier == 'Premium':
            if segment == 'champion':
                return random.choice(['VP Sales', 'Director of Analytics', 'Head of Data', 'Chief Revenue Officer', 'VP Marketing'])
            else:
                return random.choice(['Senior Manager', 'Director', 'Principal Analyst', 'Senior Director'])
        elif tier == 'Basic':
            if segment == 'champion':
                return random.choice(['Manager', 'Senior Manager', 'Team Lead', 'Analytics Manager'])
            else:
                return random.choice(['Manager', 'Senior Analyst', 'Team Lead', 'Specialist'])
        elif tier == 'Free':
            return random.choice(['Analyst', 'Associate', 'Coordinator', 'Specialist', 'Junior Manager'])
        else:  # Cancelled
            return random.choice(['Former Manager', 'Ex-Analyst', 'Previous User'])
    
    def determine_plg_scenario(self, tier, segment):
        """Determine the PLG scenario this user represents"""
        if tier == 'Free' and segment == 'conversion_ready':
            return 'CAC/Conversion'
        elif tier == 'Basic' and segment == 'champion':
            return 'PLG/Upsell'
        elif tier == 'Free' and segment == 'at_risk':
            return 'Failed Conversion'
        elif tier in ['Basic', 'Premium'] and segment == 'at_risk':
            return 'Churn'
        elif tier == 'Cancelled':
            return 'Winback'
        else:
            return 'Retention'
    
    def get_feature_sophistication(self, event_type):
        """Determine feature sophistication level"""
        for level, events in self.feature_sophistication.items():
            if event_type in events:
                return level
        return 'intermediate'
    
    def calculate_engagement_depth(self, event_type, user_segment):
        """Calculate engagement depth based on event and user segment"""
        depth_weights = {
            'champion': {'surface': 0.1, 'moderate': 0.3, 'deep': 0.6},
            'engaged': {'surface': 0.2, 'moderate': 0.6, 'deep': 0.2},
            'casual': {'surface': 0.7, 'moderate': 0.3, 'deep': 0.0},
            'at_risk': {'surface': 0.9, 'moderate': 0.1, 'deep': 0.0},
            'conversion_ready': {'surface': 0.1, 'moderate': 0.4, 'deep': 0.5}
        }
        
        weights = depth_weights.get(user_segment, depth_weights['casual'])
        return np.random.choice(list(weights.keys()), p=list(weights.values()))
    
    def get_current_plan_tier(self, tier):
        """Map tier to plan for backwards compatibility"""
        tier_mapping = {
            'Free': 'free',
            'Basic': 'basic', 
            'Premium': 'premium',
            'Cancelled': 'cancelled'
        }
        return tier_mapping.get(tier, 'free')
    
    def calculate_mrr_contribution(self, tier):
        """Calculate MRR based on tier"""
        mrr_values = {
            'Free': 0,
            'Basic': 99,        # $99/month Basic plan
            'Premium': 299,     # $299/month Premium plan  
            'Cancelled': 0
        }
        return mrr_values.get(tier, 0)
    
    def calculate_business_metrics(self, user_profile, event_type, session_start):
        """Calculate comprehensive SaaS business metrics based on tier"""
        tier = user_profile['tier']
        segment = user_profile['segment']
        plan_tier = self.get_current_plan_tier(tier)
        mrr = self.calculate_mrr_contribution(tier)
        
        # Account health metrics - adjusted by tier
        health_score_ranges = {
            'Premium': {'champion': (80, 100), 'engaged': (70, 90), 'casual': (60, 80), 'at_risk': (30, 50)},
            'Basic': {'champion': (70, 90), 'engaged': (60, 80), 'casual': (40, 70), 'at_risk': (20, 40)},
            'Free': {'conversion_ready': (50, 80), 'engaged': (40, 70), 'casual': (20, 50), 'at_risk': (10, 30)},
            'Cancelled': {'at_risk': (5, 20)}
        }
        
        score_range = health_score_ranges.get(tier, {}).get(segment, (30, 60))
        health_score = random.randint(score_range[0], score_range[1])
        
        # Usage metrics by tier
        usage_patterns = {
            'Premium': {
                'seat_utilization': (0.7, 0.95),
                'storage_utilization': (0.6, 0.9),
                'api_usage': (500, 2000),
                'integrations': (3, 8),
                'support_tickets': (0, 2)
            },
            'Basic': {
                'seat_utilization': (0.5, 0.8),
                'storage_utilization': (0.3, 0.7), 
                'api_usage': (50, 500),
                'integrations': (1, 4),
                'support_tickets': (0, 3)
            },
            'Free': {
                'seat_utilization': (0.2, 0.6),
                'storage_utilization': (0.1, 0.4),
                'api_usage': (0, 50),
                'integrations': (0, 1),
                'support_tickets': (0, 4)
            },
            'Cancelled': {
                'seat_utilization': (0.0, 0.1),
                'storage_utilization': (0.0, 0.1),
                'api_usage': (0, 0),
                'integrations': (0, 0),
                'support_tickets': (1, 5)
            }
        }
        
        patterns = usage_patterns.get(tier, usage_patterns['Free'])
        
        # Calculate engagement scores by tier + segment
        engagement_base = {
            'Premium': {'champion': 85, 'engaged': 75, 'casual': 60, 'at_risk': 40},
            'Basic': {'champion': 75, 'engaged': 65, 'casual': 45, 'at_risk': 25},
            'Free': {'conversion_ready': 70, 'engaged': 50, 'casual': 30, 'at_risk': 15},
            'Cancelled': {'at_risk': 10}
        }
        
        base_engagement = engagement_base.get(tier, {}).get(segment, 30)
        engagement_score = base_engagement + random.randint(-10, 15)
        
        return {
            'current_plan_tier': plan_tier,
            'subscription_tier': tier,  # New field for tier tracking
            'mrr_contribution': mrr,
            'arr_contribution': mrr * 12,
            'customer_lifetime_value': mrr * {'Premium': 36, 'Basic': 24, 'Free': 0, 'Cancelled': 0}.get(tier, 12),
            'account_health_score': health_score,
            'engagement_score': max(0, min(100, engagement_score)),
            'seat_utilization': round(random.uniform(*patterns['seat_utilization']), 2),
            'storage_utilization': round(random.uniform(*patterns['storage_utilization']), 2),
            'api_usage_monthly': random.randint(*patterns['api_usage']) if event_type in ['api_integration', 'api_exploration'] else 0,
            'integration_count': random.randint(*patterns['integrations']),
            'support_ticket_count': random.randint(*patterns['support_tickets'])
        }
    
    def generate_session_events(self, user_profile, session_count=1):
        """Generate events for a user session following PLG patterns"""
        events = []
        segment = user_profile['segment']
        
        for session_num in range(session_count):
            # Choose session pattern based on user segment
            pattern_weights = {
                'champion': {'champion_power_session': 0.4, 'champion_collaboration': 0.35, 'viral_behavior': 0.25},
                'engaged': {'value_realization': 0.45, 'steady_usage': 0.35, 'premium_exploration': 0.20},
                'casual': {'basic_usage': 0.5, 'onboarding_exploration': 0.3, 'value_discovery': 0.2},
                'at_risk': {'declining_session': 0.4, 'frustrated_session': 0.2, 'minimal_engagement': 0.4},
                'conversion_ready': {'conversion_signal': 0.6, 'value_realization': 0.4}
            }
            
            available_patterns = self.session_patterns.get(segment, self.session_patterns['casual'])
            weights = pattern_weights.get(segment, {'basic_usage': 1.0})
            
            # Select pattern
            pattern_name = np.random.choice(list(weights.keys()), p=list(weights.values()))
            event_sequence = available_patterns.get(pattern_name, ['login', 'dashboard_view', 'logout'])
            
    def generate_session_events(self, user_profile, session_count=1):
        """Generate events for a user session following tier-based PLG patterns"""
        events = []
        tier = user_profile['tier']
        segment = user_profile['segment']
        
        for session_num in range(session_count):
            # Get tier-specific session patterns
            tier_patterns = self.tier_session_patterns.get(tier, self.tier_session_patterns['Free'])
            segment_patterns = tier_patterns.get(segment, {'basic_usage': ['login', 'dashboard_view', 'logout']})
            
            # Select pattern randomly from available patterns for this tier/segment
            if segment_patterns:
                pattern_name = random.choice(list(segment_patterns.keys()))
                event_sequence = segment_patterns[pattern_name]
            else:
                pattern_name = 'basic_usage'
                event_sequence = ['login', 'dashboard_view', 'logout']
            
            # Generate session timing
            session_start = datetime.now() - timedelta(days=random.randint(0, 30))
            session_start = session_start.replace(
                hour=random.randint(7, 19),  # Business hours + some evening
                minute=random.randint(0, 59),
                second=0,
                microsecond=0
            )
            
            session_id = f'sess_{uuid.uuid4().hex[:12]}'
            current_time = session_start
            
            # Generate events in sequence
            for i, event_type in enumerate(event_sequence):
                if i > 0:
                    # Add realistic time gaps between events based on tier
                    gap_ranges = {
                        'Premium': (0.5, 3.0),    # Fast, efficient users
                        'Basic': (1.0, 5.0),     # Moderate pacing
                        'Free': (2.0, 8.0),      # Slower, more exploratory
                        'Cancelled': (5.0, 15.0) # Hesitant, unfamiliar
                    }
                    gap_range = gap_ranges.get(tier, (1.0, 5.0))
                    gap_minutes = random.uniform(*gap_range)
                    current_time += timedelta(minutes=gap_minutes)
                
                event = self.create_telemetry_event(user_profile, event_type, current_time, session_id, session_start, pattern_name)
                events.append(event)
        
        return events
    
    def calculate_engagement_depth(self, event_type, tier, segment):
        """Calculate engagement depth based on event, tier, and segment"""
        depth_weights = {
            'Premium': {
                'champion': {'surface': 0.05, 'moderate': 0.25, 'deep': 0.70},
                'engaged': {'surface': 0.10, 'moderate': 0.50, 'deep': 0.40},
                'casual': {'surface': 0.30, 'moderate': 0.60, 'deep': 0.10},
                'at_risk': {'surface': 0.70, 'moderate': 0.30, 'deep': 0.00}
            },
            'Basic': {
                'champion': {'surface': 0.10, 'moderate': 0.40, 'deep': 0.50},
                'engaged': {'surface': 0.20, 'moderate': 0.60, 'deep': 0.20},
                'casual': {'surface': 0.50, 'moderate': 0.40, 'deep': 0.10},
                'at_risk': {'surface': 0.80, 'moderate': 0.20, 'deep': 0.00}
            },
            'Free': {
                'conversion_ready': {'surface': 0.15, 'moderate': 0.45, 'deep': 0.40},
                'engaged': {'surface': 0.30, 'moderate': 0.50, 'deep': 0.20},
                'casual': {'surface': 0.70, 'moderate': 0.30, 'deep': 0.00},
                'at_risk': {'surface': 0.90, 'moderate': 0.10, 'deep': 0.00}
            },
            'Cancelled': {
                'at_risk': {'surface': 0.95, 'moderate': 0.05, 'deep': 0.00}
            }
        }
        
        weights = depth_weights.get(tier, {}).get(segment, {'surface': 0.7, 'moderate': 0.3, 'deep': 0.0})
        return np.random.choice(list(weights.keys()), p=list(weights.values()))
    
    def get_plg_signals(self, event_type, tier, segment, plg_scenario):
        """Generate PLG behavioral signals based on tier and scenario"""
        signals = {
            'premium_feature_exposure': False,
            'usage_limit_proximity': 'low',
            'value_realization_event': False,
            'viral_behavior': False,
            'expansion_signal': False,
            'friction_encountered': False,
            'help_seeking_behavior': False,
            'churn_risk_indicator': False,
            'conversion_signal': False
        }
        
        # Premium feature exposure
        premium_events = ['premium_feature_explore', 'enterprise_trial', 'advanced_analytics', 'api_integration', 'automation_setup']
        signals['premium_feature_exposure'] = event_type in premium_events
        
        # Usage limits (mainly for Free tier)
        if tier == 'Free' and segment == 'conversion_ready':
            if event_type == 'usage_limit_hit':
                signals['usage_limit_proximity'] = 'exceeded'
            elif event_type in ['core_feature_usage', 'data_export']:
                signals['usage_limit_proximity'] = random.choice(['medium', 'high'])
        
        # Value realization
        value_events = ['insight_discovery', 'workflow_success', 'share_result', 'success_showcase', 'report_generate']
        signals['value_realization_event'] = event_type in value_events
        
        # Viral behavior
        viral_events = ['external_demo', 'advanced_sharing', 'thought_leadership', 'referral_program']
        signals['viral_behavior'] = event_type in viral_events
        
        # Expansion signals
        if tier == 'Free':
            expansion_events = ['premium_feature_explore', 'pricing_page_view', 'paywall_encounter']
            signals['expansion_signal'] = event_type in expansion_events
        elif tier == 'Basic':
            expansion_events = ['enterprise_trial', 'team_management_view', 'api_exploration', 'advanced_feature_usage']
            signals['expansion_signal'] = event_type in expansion_events
        
        # Friction indicators
        friction_events = ['error_event', 'feature_abandon', 'payment_issue_check', 'support_ticket_create']
        signals['friction_encountered'] = event_type in friction_events
        
        # Help seeking
        help_events = ['help_search', 'support_ticket_create', 'account_reactivation_view']
        signals['help_seeking_behavior'] = event_type in help_events
        
        # Churn risk
        churn_events = ['cost_review', 'competitor_comparison', 'declining_usage', 'data_export_final']
        signals['churn_risk_indicator'] = event_type in churn_events
        
        # Conversion signals (Free users showing buying intent)
        if tier == 'Free':
            conversion_events = ['usage_limit_hit', 'premium_feature_explore', 'pricing_page_view']
            signals['conversion_signal'] = event_type in conversion_events
        
        return signals
    
    def create_telemetry_event(self, user_profile, event_type, timestamp, session_id, session_start, session_pattern):
        """Create a comprehensive telemetry event with tier-based PLG fields"""
        event_id = f'evt_{timestamp.strftime("%Y%m%d")}_{uuid.uuid4().hex[:6]}'
        
        # Calculate session duration
        session_duration = (timestamp - session_start).total_seconds() / 60
        
        # Get business metrics
        business_metrics = self.calculate_business_metrics(user_profile, event_type, session_start)
        
        # Get PLG signals based on tier and scenario
        plg_signals = self.get_plg_signals(event_type, user_profile['tier'], user_profile['segment'], user_profile['plg_scenario'])
        
        # Build comprehensive event
        event = {
            # Core event fields
            'event_id': event_id,
            'user_id': user_profile['user_id'],
            'session_id': session_id,
            'event_type': event_type,
            'timestamp': timestamp.isoformat() + 'Z',
            'session_start_time': session_start.isoformat() + 'Z',
            'session_duration_minutes': round(session_duration, 2),
            
            # Product context
            'product_name': random.choice(self.product_names),
            'feature_name': self.feature_mapping.get(event_type, 'General Feature'),
            'page_url': f'/app/{event_type.replace("_", "-")}',
            'device_type': random.choice(self.device_types),
            'browser_name': random.choice(self.browsers),
            'operating_system': random.choice(self.operating_systems),
            'response_time_ms': self.get_response_time_by_tier(user_profile['tier'], event_type),
            
            # Geographic data
            'geography_country': 'US',
            'geography_region': random.choice(self.regions),
            'geography_city': random.choice(self.cities),
            'ip_address': f'192.168.{random.randint(1, 255)}.xxx',
            
            # User profile data (including tier)
            'contact_external_id': user_profile['external_id'],
            'user_email': user_profile['email'],
            'user_first_name': user_profile['first_name'],
            'user_last_name': user_profile['last_name'],
            'user_title': user_profile['title'],
            'user_department': user_profile['department'],
            'subscription_tier': user_profile['tier'],  # KEY FIELD for tier tracking
            
            # PLG behavioral intelligence (tier-aware)
            'user_segment': user_profile['segment'],
            'plg_scenario': user_profile['plg_scenario'],  # CAC/Conversion, PLG/Upsell, etc.
            'session_type': session_pattern,
            'engagement_depth': self.calculate_engagement_depth(event_type, user_profile['tier'], user_profile['segment']),
            'feature_sophistication': self.get_feature_sophistication(event_type),
            
            # Business context
            'business_hours_indicator': 8 <= timestamp.hour <= 18 and timestamp.weekday() < 5,
            'mobile_usage_indicator': random.choice(self.device_types) == 'mobile',
            'weekend_usage_indicator': timestamp.weekday() >= 5,
            
            # PLG signals (tier-specific)
            'premium_feature_exposure': plg_signals['premium_feature_exposure'],
            'usage_limit_proximity': plg_signals['usage_limit_proximity'],
            'value_realization_event': plg_signals['value_realization_event'],
            'viral_behavior': plg_signals['viral_behavior'],
            'expansion_signal': plg_signals['expansion_signal'],
            'conversion_signal': plg_signals['conversion_signal'],
            
            # Risk indicators
            'friction_encountered': plg_signals['friction_encountered'],
            'help_seeking_behavior': plg_signals['help_seeking_behavior'],
            'churn_risk_indicator': plg_signals['churn_risk_indicator'],
            'feature_adoption_success': not plg_signals['friction_encountered'],
            
            # Revenue & subscription metrics (tier-based)
            'current_plan_tier': business_metrics['current_plan_tier'],
            'mrr_contribution': business_metrics['mrr_contribution'],
            'arr_contribution': business_metrics['arr_contribution'],
            'customer_lifetime_value': business_metrics['customer_lifetime_value'],
            'payment_status': self.get_payment_status(user_profile['tier']),
            
            # Account health metrics (tier-adjusted)
            'account_health_score': business_metrics['account_health_score'],
            'engagement_score': business_metrics['engagement_score'],
            'seat_utilization': business_metrics['seat_utilization'],
            'storage_utilization': business_metrics['storage_utilization'],
            'integration_count': business_metrics['integration_count'],
            'support_ticket_count': business_metrics['support_ticket_count'],
            
            # Predictive features for Einstein Model Builder (tier-aware)
            'churn_risk_score': self.calculate_churn_risk_score(user_profile['tier'], user_profile['segment']),
            'conversion_propensity': self.calculate_conversion_propensity(user_profile['tier'], user_profile['segment'], event_type),
            'upsell_propensity': self.calculate_upsell_propensity(user_profile['tier'], user_profile['segment'], event_type),
            'retention_probability': self.calculate_retention_probability(user_profile['tier'], user_profile['segment']),
            
            # Agentforce context (scenario-specific)
            'next_best_action': self.get_next_best_action_by_scenario(user_profile['plg_scenario'], event_type),
            'intervention_priority': self.get_intervention_priority_by_tier(user_profile['tier'], user_profile['segment'], event_type),
            
            # Metadata
            'is_demo_data': True,
            'source_system': 'plg_telemetry_generator_v2.0_tier_aware',
            'custom_properties': json.dumps({
                'session_pattern': session_pattern,
                'plg_scenario': user_profile['plg_scenario'],
                'tier_transition_candidate': self.is_tier_transition_candidate(user_profile, event_type),
                'cohort': f'2024-{random.randint(1, 12):02d}',
                'experiment_variant': random.choice(['control', 'variant_a', 'variant_b'])
            })
        }
        
        # Add tier-specific event context
        self.add_tier_specific_context(event, event_type, user_profile)
        
        return event
    
    def add_tier_specific_context(self, event, event_type, user_profile):
        """Add tier-specific context to events"""
        tier = user_profile['tier']
        
        # Free tier specific fields
        if tier == 'Free':
            if event_type == 'usage_limit_hit':
                event.update({
                    'limit_type': random.choice(['reports', 'data_export', 'api_calls', 'storage']),
                    'usage_percentage': random.randint(95, 120),  # 95-120% of limit
                    'free_tier_limit': True,
                    'upgrade_prompt_shown': True
                })
            elif event_type == 'pricing_page_view':
                event.update({
                    'plans_viewed': random.choice([['Basic'], ['Premium'], ['Basic', 'Premium']]),
                    'time_on_page_seconds': random.randint(30, 300),
                    'conversion_intent_score': random.randint(60, 95)
                })
        
        # Basic tier specific fields
        elif tier == 'Basic':
            if event_type == 'enterprise_trial':
                event.update({
                    'trial_feature': random.choice(['advanced_analytics', 'api_access', 'team_management', 'custom_branding']),
                    'trial_days_remaining': random.randint(1, 14),
                    'premium_upgrade_eligible': True
                })
            elif event_type == 'team_management_view':
                event.update({
                    'current_team_size': random.randint(3, 15),
                    'team_limit_approached': random.choice([True, False]),
                    'premium_team_features_explored': True
                })
        
        # Premium tier specific fields
        elif tier == 'Premium':
            if event_type == 'automation_setup':
                event.update({
                    'automation_type': random.choice(['data_sync', 'report_scheduling', 'alert_system', 'workflow_trigger']),
                    'complexity_level': 'advanced',
                    'premium_feature_utilized': True
                })
            elif event_type == 'api_integration':
                event.update({
                    'api_calls_this_month': random.randint(1000, 5000),
                    'integration_type': random.choice(['crm', 'marketing_automation', 'data_warehouse', 'bi_tool']),
                    'enterprise_grade': True
                })
        
        # Cancelled tier specific fields
        elif tier == 'Cancelled':
            if event_type == 'account_reactivation_view':
                event.update({
                    'days_since_cancellation': random.randint(1, 90),
                    'cancellation_reason': random.choice(['cost', 'feature_gap', 'competitor', 'internal_change']),
                    'winback_offer_eligible': True
                })
            elif event_type == 'data_export_final':
                event.update({
                    'export_type': 'account_closure',
                    'data_retention_days': random.randint(7, 30),
                    'reactivation_window': True
                })
        
        # Add conversion value based on tier and event
        if event_type in ['insight_discovery', 'workflow_success', 'report_generate']:
            value_ranges = {
                'Premium': (200, 1000),
                'Basic': (50, 400), 
                'Free': (10, 100),
                'Cancelled': (0, 20)
            }
            range_values = value_ranges.get(tier, (10, 100))
            event['conversion_value'] = random.randint(*range_values)
        
        # Add error context for friction events
        if event_type == 'error_event':
            event.update({
                'error_code': random.choice(['ERR_404', 'ERR_500', 'ERR_TIMEOUT', 'ERR_AUTH', 'ERR_LIMIT']),
                'error_message': random.choice([
                    'Resource not found', 'Internal server error', 'Request timeout', 
                    'Authentication failed', 'Usage limit exceeded'
                ]),
                'tier_related_error': tier == 'Free' and random.choice([True, False])
            })
        
        # Add file operation context
        if event_type in ['data_export', 'data_export_final']:
            size_ranges = {
                'Premium': (5000000, 50000000),  # 5-50MB
                'Basic': (1000000, 10000000),    # 1-10MB
                'Free': (100000, 1000000),       # 100KB-1MB
                'Cancelled': (0, 100000)         # Up to 100KB
            }
            range_values = size_ranges.get(tier, (100000, 1000000))
            event['file_size_bytes'] = random.randint(*range_values)
    
    def generate_dataset(self, total_records=1000):
        """Generate the complete dataset with tier-based PLG patterns"""
        print(f"Generating {total_records} tier-aware PLG telemetry records...")
        
        # Calculate number of users needed (average events per user varies by tier)
        tier_session_counts = {
            'Premium': random.randint(4, 8),    # Heavy users
            'Basic': random.randint(2, 5),      # Moderate users
            'Free': random.randint(1, 3),       # Light users
            'Cancelled': 1                      # Minimal activity
        }
        
        avg_events_per_user = 4
        num_users = total_records // avg_events_per_user
        
        all_events = []
        tier_distribution = []
        scenario_distribution = []
        
        for user_idx in range(num_users):
            # Generate user profile with tier
            user_profile = self.generate_user_profile(user_idx)
            tier_distribution.append(user_profile['tier'])
            scenario_distribution.append(user_profile['plg_scenario'])
            
            # Determine number of sessions based on tier and segment
            base_sessions = tier_session_counts.get(user_profile['tier'], 2)
            
            # Segment adjustments
            if user_profile['segment'] == 'champion':
                session_count = base_sessions + random.randint(1, 2)
            elif user_profile['segment'] == 'at_risk':
                session_count = max(1, base_sessions - random.randint(1, 2))
            else:
                session_count = base_sessions
            
            # Generate events for this user
            user_events = self.generate_session_events(user_profile, session_count)
            all_events.extend(user_events)
            
            if len(all_events) >= total_records:
                break
        
        # Trim to exact count and sort by timestamp
        all_events = all_events[:total_records]
        all_events.sort(key=lambda x: x['timestamp'])
        
        print(f"Generated {len(all_events)} events for {num_users} users")
        
        # Print distributions
        from collections import Counter
        tier_counts = Counter(tier_distribution)
        scenario_counts = Counter(scenario_distribution)
        
        print("\n🎯 Tier Distribution:")
        for tier, count in tier_counts.items():
            percentage = (count / len(tier_distribution)) * 100
            print(f"  {tier}: {count} users ({percentage:.1f}%)")
        
        print("\n📊 PLG Scenario Distribution:")
        for scenario, count in scenario_counts.items():
            percentage = (count / len(scenario_distribution)) * 100
            print(f"  {scenario}: {count} users ({percentage:.1f}%)")
        
        # Event-level analysis
        event_df = pd.DataFrame(all_events)
        segments = event_df['user_segment'].value_counts()
        print(f"\n🔍 Event Segment Distribution:")
        for segment, count in segments.items():
            print(f"  {segment}: {count} events ({count/len(all_events)*100:.1f}%)")
        
        return event_df

# ============================================================================
# MAIN EXECUTION WITH TIER ANALYTICS
# ============================================================================

def main():
    """Main execution function with tier-focused analytics"""
    print("🚀 Tier-Aware PLG Product Telemetry Data Generator")
    print("=" * 60)
    
    # Initialize generator
    generator = PLGTelemetryGenerator()
    
    # Generate dataset
    df = generator.generate_dataset(1000)
    
    # Display comprehensive summary statistics
    print(f"\n📊 Dataset Summary:")
    print(f"Total records: {len(df)}")
    print(f"Unique users: {df['user_id'].nunique()}")
    print(f"Unique sessions: {df['session_id'].nunique()}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    # Tier-specific analytics
    print(f"\n🎯 Tier-Based Analytics:")
    tier_summary = df.groupby('subscription_tier').agg({
        'user_id': 'nunique',
        'mrr_contribution': 'mean',
        'engagement_score': 'mean',
        'churn_risk_score': 'mean',
        'conversion_propensity': 'mean'
    }).round(2)
    print(tier_summary)
    
    # PLG Scenario Analysis
    print(f"\n📈 PLG Scenario Breakdown:")
    scenario_summary = df.groupby('plg_scenario').agg({
        'user_id': 'nunique',
        'conversion_signal': 'sum',
        'expansion_signal': 'sum',
        'churn_risk_indicator': 'sum',
        'value_realization_event': 'sum'
    })
    print(scenario_summary)
    
    # Show sample records with key tier fields
    print(f"\n📋 Sample Records (Key Tier Fields):")
    sample_cols = ['event_id', 'subscription_tier', 'user_segment', 'plg_scenario', 'event_type', 'mrr_contribution', 'conversion_propensity']
    print(df[sample_cols].head(10).to_string(index=False))
    
    # Save to CSV
    filename = f'tier_aware_plg_telemetry_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(filename, index=False)
    print(f"\n💾 Dataset saved as: {filename}")
    
    # Display tier-specific PLG insights
    print(f"\n🎯 Tier-Specific PLG Insights:")
    
    # Conversion insights
    free_users = df[df['subscription_tier'] == 'Free']
    conversion_signals = free_users['conversion_signal'].sum()
    print(f"Free tier conversion signals: {conversion_signals} ({(conversion_signals/len(free_users)*100):.1f}% of Free events)")
    
    # Upsell insights  
    basic_users = df[df['subscription_tier'] == 'Basic']
    upsell_signals = basic_users['expansion_signal'].sum()
    print(f"Basic tier upsell signals: {upsell_signals} ({(upsell_signals/len(basic_users)*100):.1f}% of Basic events)")
    
    # Churn insights
    paid_users = df[df['subscription_tier'].isin(['Basic', 'Premium'])]
    churn_indicators = paid_users['churn_risk_indicator'].sum()
    print(f"Paid tier churn indicators: {churn_indicators} ({(churn_indicators/len(paid_users)*100):.1f}% of paid events)")
    
    # Revenue analysis
    total_mrr = df.groupby('user_id')['mrr_contribution'].first().sum()
    print(f"Total MRR represented: ${total_mrr:,.2f}")
    print(f"Average MRR per user: ${df.groupby('user_id')['mrr_contribution'].first().mean():.2f}")
    
    return df

# Run the generator
if __name__ == "__main__":
    telemetry_df = main()
