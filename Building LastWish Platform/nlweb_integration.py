"""
NLWeb Integration for LastWish Estate Planning Platform
Provides AI-powered estate planning assistance using Microsoft's NLWeb package
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLWebEstateAssistant:
    """
    AI-powered estate planning assistant using NLWeb
    Provides intelligent recommendations and document generation
    """
    
    def __init__(self):
        """Initialize the NLWeb Estate Assistant"""
        self.session_id = None
        self.user_context = {}
        
        # Estate planning knowledge base
        self.estate_planning_prompts = {
            'will_analysis': """
            You are an expert estate planning attorney. Analyze the user's estate planning information and provide:
            1. Completeness assessment of their will
            2. Legal compliance recommendations
            3. Potential issues or gaps
            4. Suggestions for improvement
            5. Tax optimization opportunities
            
            User Information: {user_data}
            Assets: {assets}
            Beneficiaries: {beneficiaries}
            """,
            
            'asset_recommendations': """
            You are a financial advisor specializing in estate planning. Based on the user's assets, provide:
            1. Asset diversification recommendations
            2. Estate tax minimization strategies
            3. Trust structure suggestions
            4. Beneficiary allocation optimization
            5. Risk assessment and mitigation
            
            Current Assets: {assets}
            Total Portfolio Value: {total_value}
            User Profile: {user_profile}
            """,
            
            'beneficiary_guidance': """
            You are an estate planning specialist. Analyze the beneficiary structure and provide:
            1. Inheritance allocation recommendations
            2. Minor beneficiary protection strategies
            3. Contingent beneficiary suggestions
            4. Family dynamics considerations
            5. Legal protection recommendations
            
            Beneficiaries: {beneficiaries}
            Family Structure: {family_info}
            Estate Value: {estate_value}
            """,
            
            'crypto_inheritance': """
            You are a digital asset estate planning expert. Provide guidance on:
            1. Crypto asset inheritance strategies
            2. Private key and seed phrase management
            3. Smart contract inheritance solutions
            4. Multi-signature wallet recommendations
            5. Legal compliance for digital assets
            
            Crypto Assets: {crypto_assets}
            Total Crypto Value: {crypto_value}
            Beneficiaries: {beneficiaries}
            """,
            
            'document_generation': """
            You are a legal document specialist. Generate a comprehensive will document with:
            1. Proper legal language and structure
            2. Asset distribution clauses
            3. Beneficiary designations
            4. Executor responsibilities
            5. Digital asset provisions
            6. Guardian appointments (if applicable)
            
            Will Information: {will_data}
            Jurisdiction: {jurisdiction}
            Legal Requirements: {legal_requirements}
            """
        }
    
    def initialize_session(self, user_id: str, user_data: Dict[str, Any]) -> str:
        """
        Initialize a new NLWeb session for estate planning assistance
        
        Args:
            user_id: Unique user identifier
            user_data: User profile and estate planning data
            
        Returns:
            Session ID for continued interaction
        """
        try:
            self.session_id = f"estate_session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.user_context = {
                'user_id': user_id,
                'session_start': datetime.now().isoformat(),
                'user_data': user_data,
                'conversation_history': []
            }
            
            logger.info(f"Initialized NLWeb session: {self.session_id}")
            return self.session_id
            
        except Exception as e:
            logger.error(f"Failed to initialize NLWeb session: {str(e)}")
            raise
    
    def analyze_estate_completeness(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the completeness of user's estate planning using AI
        
        Args:
            user_data: Complete user estate planning data
            
        Returns:
            AI analysis with recommendations and completeness score
        """
        try:
            # Prepare data for AI analysis
            analysis_data = {
                'user_profile': user_data.get('user', {}),
                'assets': user_data.get('assets', []),
                'crypto_assets': user_data.get('crypto_assets', []),
                'beneficiaries': user_data.get('beneficiaries', []),
                'will_status': user_data.get('will', {}),
                'total_estate_value': self._calculate_total_estate_value(user_data)
            }
            
            # Simulate NLWeb AI analysis (replace with actual NLWeb API call)
            analysis_result = self._simulate_nlweb_analysis(analysis_data)
            
            # Calculate completeness score
            completeness_score = self._calculate_completeness_score(user_data)
            
            return {
                'session_id': self.session_id,
                'completeness_score': completeness_score,
                'analysis': analysis_result,
                'recommendations': self._generate_recommendations(analysis_data),
                'priority_actions': self._identify_priority_actions(analysis_data),
                'legal_compliance': self._check_legal_compliance(analysis_data),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Estate completeness analysis failed: {str(e)}")
            return {
                'error': str(e),
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_will_document(self, will_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive will document using AI
        
        Args:
            will_data: Complete will information from user
            
        Returns:
            Generated will document with legal language
        """
        try:
            # Prepare will data for document generation
            document_data = {
                'personal_info': will_data.get('personal_info', {}),
                'executor': will_data.get('executor', {}),
                'beneficiaries': will_data.get('beneficiaries', []),
                'assets': will_data.get('assets', []),
                'crypto_assets': will_data.get('crypto_assets', []),
                'guardianship': will_data.get('guardianship', {}),
                'final_wishes': will_data.get('final_wishes', {}),
                'jurisdiction': will_data.get('jurisdiction', 'General')
            }
            
            # Generate will document using AI
            will_document = self._generate_will_document_ai(document_data)
            
            return {
                'session_id': self.session_id,
                'document_type': 'last_will_testament',
                'document_content': will_document,
                'legal_disclaimers': self._get_legal_disclaimers(),
                'next_steps': self._get_will_next_steps(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Will document generation failed: {str(e)}")
            return {
                'error': str(e),
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_crypto_inheritance_guidance(self, crypto_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide AI-powered guidance for cryptocurrency inheritance planning
        
        Args:
            crypto_data: User's cryptocurrency assets and beneficiaries
            
        Returns:
            Comprehensive crypto inheritance guidance
        """
        try:
            guidance = {
                'session_id': self.session_id,
                'crypto_analysis': self._analyze_crypto_portfolio(crypto_data),
                'inheritance_strategies': self._generate_crypto_strategies(crypto_data),
                'security_recommendations': self._get_crypto_security_advice(crypto_data),
                'legal_considerations': self._get_crypto_legal_advice(crypto_data),
                'smart_contract_options': self._suggest_smart_contracts(crypto_data),
                'implementation_steps': self._get_crypto_implementation_steps(crypto_data),
                'timestamp': datetime.now().isoformat()
            }
            
            return guidance
            
        except Exception as e:
            logger.error(f"Crypto inheritance guidance failed: {str(e)}")
            return {
                'error': str(e),
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def chat_with_assistant(self, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Interactive chat with AI estate planning assistant
        
        Args:
            user_message: User's question or request
            context: Additional context for the conversation
            
        Returns:
            AI assistant response with recommendations
        """
        try:
            # Add message to conversation history
            self.user_context['conversation_history'].append({
                'timestamp': datetime.now().isoformat(),
                'user_message': user_message,
                'context': context or {}
            })
            
            # Generate AI response based on estate planning expertise
            ai_response = self._generate_ai_response(user_message, context)
            
            # Add AI response to conversation history
            self.user_context['conversation_history'].append({
                'timestamp': datetime.now().isoformat(),
                'ai_response': ai_response,
                'response_type': 'estate_planning_advice'
            })
            
            return {
                'session_id': self.session_id,
                'user_message': user_message,
                'ai_response': ai_response,
                'conversation_id': len(self.user_context['conversation_history']),
                'suggested_actions': self._suggest_follow_up_actions(user_message, ai_response),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Chat interaction failed: {str(e)}")
            return {
                'error': str(e),
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_total_estate_value(self, user_data: Dict[str, Any]) -> float:
        """Calculate total estate value from all assets"""
        total_value = 0.0
        
        # Traditional assets
        for asset in user_data.get('assets', []):
            total_value += float(asset.get('estimated_value', 0))
        
        # Crypto assets
        for crypto_asset in user_data.get('crypto_assets', []):
            total_value += float(crypto_asset.get('estimated_value_usd', 0))
        
        return total_value
    
    def _calculate_completeness_score(self, user_data: Dict[str, Any]) -> int:
        """Calculate estate planning completeness score (0-100)"""
        score = 0
        
        # Basic information (20 points)
        if user_data.get('user', {}).get('name'):
            score += 10
        if user_data.get('user', {}).get('address'):
            score += 10
        
        # Assets (25 points)
        if user_data.get('assets', []):
            score += 15
        if user_data.get('crypto_assets', []):
            score += 10
        
        # Beneficiaries (25 points)
        beneficiaries = user_data.get('beneficiaries', [])
        if beneficiaries:
            score += 15
            # Check if inheritance percentages add up to 100%
            total_percentage = sum(b.get('inheritance_percentage', 0) for b in beneficiaries)
            if 95 <= total_percentage <= 105:  # Allow small variance
                score += 10
        
        # Will document (20 points)
        will_data = user_data.get('will', {})
        if will_data.get('executor'):
            score += 10
        if will_data.get('final_wishes'):
            score += 10
        
        # Legal compliance (10 points)
        if user_data.get('legal_review_completed'):
            score += 10
        
        return min(score, 100)
    
    def _simulate_nlweb_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """
        Simulate NLWeb AI analysis (replace with actual NLWeb API call)
        In production, this would call the actual NLWeb package
        """
        total_value = analysis_data.get('total_estate_value', 0)
        asset_count = len(analysis_data.get('assets', []))
        crypto_count = len(analysis_data.get('crypto_assets', []))
        beneficiary_count = len(analysis_data.get('beneficiaries', []))
        
        analysis = f"""
        **Estate Planning Analysis Report**
        
        **Portfolio Overview:**
        - Total Estate Value: ${total_value:,.2f}
        - Traditional Assets: {asset_count} items
        - Cryptocurrency Assets: {crypto_count} items
        - Designated Beneficiaries: {beneficiary_count} people
        
        **Key Findings:**
        1. **Asset Diversification**: Your estate shows {"good" if asset_count > 3 else "limited"} diversification across asset types.
        
        2. **Digital Asset Management**: {"Excellent" if crypto_count > 0 else "Consider adding"} cryptocurrency inheritance planning.
        
        3. **Beneficiary Structure**: {"Well-structured" if beneficiary_count > 1 else "Consider additional"} beneficiary designations.
        
        **Risk Assessment:**
        - Estate Tax Exposure: {"High" if total_value > 1000000 else "Moderate" if total_value > 100000 else "Low"}
        - Probate Complexity: {"Complex" if asset_count > 5 else "Standard"}
        - Digital Asset Risk: {"Managed" if crypto_count > 0 else "Unaddressed"}
        
        **Recommendations:**
        1. Consider establishing a revocable living trust for assets over $500,000
        2. Implement multi-signature wallets for cryptocurrency holdings
        3. Review and update beneficiary designations annually
        4. Ensure proper documentation for digital asset access
        """
        
        return analysis.strip()
    
    def _generate_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations based on estate analysis"""
        recommendations = []
        
        total_value = analysis_data.get('total_estate_value', 0)
        
        # Estate tax recommendations
        if total_value > 1000000:
            recommendations.append({
                'category': 'Tax Planning',
                'priority': 'High',
                'title': 'Estate Tax Mitigation',
                'description': 'Consider establishing irrevocable trusts to reduce estate tax liability.',
                'action_items': [
                    'Consult with estate tax attorney',
                    'Explore charitable giving strategies',
                    'Consider annual gift tax exclusions'
                ]
            })
        
        # Crypto asset recommendations
        if analysis_data.get('crypto_assets'):
            recommendations.append({
                'category': 'Digital Assets',
                'priority': 'High',
                'title': 'Cryptocurrency Inheritance Planning',
                'description': 'Implement secure inheritance mechanisms for digital assets.',
                'action_items': [
                    'Set up multi-signature wallets',
                    'Create detailed access instructions',
                    'Consider smart contract inheritance solutions'
                ]
            })
        
        # Beneficiary recommendations
        beneficiaries = analysis_data.get('beneficiaries', [])
        if len(beneficiaries) < 2:
            recommendations.append({
                'category': 'Beneficiaries',
                'priority': 'Medium',
                'title': 'Contingent Beneficiaries',
                'description': 'Add backup beneficiaries to ensure proper asset distribution.',
                'action_items': [
                    'Identify secondary beneficiaries',
                    'Consider charitable organizations',
                    'Update beneficiary percentages'
                ]
            })
        
        return recommendations
    
    def _identify_priority_actions(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Identify immediate priority actions for estate planning"""
        actions = []
        
        if not analysis_data.get('beneficiaries'):
            actions.append("Add at least one primary beneficiary")
        
        if not analysis_data.get('assets') and not analysis_data.get('crypto_assets'):
            actions.append("Document your assets and their estimated values")
        
        total_percentage = sum(b.get('inheritance_percentage', 0) for b in analysis_data.get('beneficiaries', []))
        if total_percentage != 100:
            actions.append("Adjust beneficiary inheritance percentages to total 100%")
        
        if analysis_data.get('crypto_assets') and not any(ca.get('access_instructions') for ca in analysis_data.get('crypto_assets', [])):
            actions.append("Add access instructions for cryptocurrency assets")
        
        return actions
    
    def _check_legal_compliance(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check legal compliance requirements"""
        compliance = {
            'status': 'compliant',
            'issues': [],
            'recommendations': []
        }
        
        # Check for minor beneficiaries without guardians
        for beneficiary in analysis_data.get('beneficiaries', []):
            if beneficiary.get('is_minor') and not beneficiary.get('guardian_name'):
                compliance['issues'].append(f"Minor beneficiary {beneficiary.get('name')} needs guardian designation")
                compliance['status'] = 'needs_attention'
        
        # Check for proper executor designation
        if not analysis_data.get('user_data', {}).get('will', {}).get('executor'):
            compliance['issues'].append("No executor designated for will")
            compliance['status'] = 'needs_attention'
        
        return compliance
    
    def _generate_will_document_ai(self, document_data: Dict[str, Any]) -> str:
        """Generate will document using AI (simulated)"""
        personal_info = document_data.get('personal_info', {})
        executor = document_data.get('executor', {})
        
        will_document = f"""
        LAST WILL AND TESTAMENT
        
        I, {personal_info.get('name', '[NAME]')}, of {personal_info.get('address', '[ADDRESS]')}, being of sound mind and disposing memory, do hereby make, publish, and declare this to be my Last Will and Testament, hereby revoking all former wills and codicils made by me.
        
        ARTICLE I - EXECUTOR
        I hereby nominate and appoint {executor.get('name', '[EXECUTOR NAME]')} as the Executor of this Will. If {executor.get('name', '[EXECUTOR NAME]')} is unable or unwilling to serve, I nominate {executor.get('backup_name', '[BACKUP EXECUTOR]')} as alternate Executor.
        
        ARTICLE II - DISPOSITION OF PROPERTY
        I give, devise, and bequeath all of my property, both real and personal, of every kind and nature, and wherever situated, to my beneficiaries as follows:
        
        [BENEFICIARY DISTRIBUTIONS WILL BE INSERTED HERE]
        
        ARTICLE III - DIGITAL ASSETS
        I hereby grant my Executor full authority to access, manage, and distribute my digital assets, including but not limited to:
        - Cryptocurrency holdings and digital wallets
        - Non-fungible tokens (NFTs) and digital collectibles
        - Online accounts and digital files
        - Social media accounts and digital content
        
        [DETAILED DIGITAL ASSET INSTRUCTIONS WILL BE INSERTED HERE]
        
        ARTICLE IV - GUARDIANSHIP
        [GUARDIANSHIP PROVISIONS FOR MINOR CHILDREN WILL BE INSERTED HERE]
        
        ARTICLE V - FINAL WISHES
        [FUNERAL AND BURIAL PREFERENCES WILL BE INSERTED HERE]
        
        IN WITNESS WHEREOF, I have hereunto set my hand this _____ day of _________, 2024.
        
        _________________________________
        {personal_info.get('name', '[NAME]')}
        
        WITNESSES:
        [WITNESS SIGNATURES AND INFORMATION]
        
        NOTARIZATION:
        [NOTARY ACKNOWLEDGMENT]
        """
        
        return will_document.strip()
    
    def _get_legal_disclaimers(self) -> List[str]:
        """Get legal disclaimers for generated documents"""
        return [
            "This document is generated for informational purposes only and does not constitute legal advice.",
            "Please consult with a qualified attorney in your jurisdiction before executing any legal documents.",
            "Laws vary by state and country - ensure compliance with local requirements.",
            "This AI-generated document should be reviewed by legal counsel before use."
        ]
    
    def _get_will_next_steps(self) -> List[str]:
        """Get recommended next steps after will generation"""
        return [
            "Review the generated will document carefully",
            "Consult with an estate planning attorney",
            "Ensure proper witness and notarization requirements",
            "Store the executed will in a secure location",
            "Inform your executor of the will's location",
            "Review and update the will annually or after major life events"
        ]
    
    def _analyze_crypto_portfolio(self, crypto_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cryptocurrency portfolio for inheritance planning"""
        crypto_assets = crypto_data.get('crypto_assets', [])
        total_value = sum(float(asset.get('estimated_value_usd', 0)) for asset in crypto_assets)
        
        analysis = {
            'total_crypto_value': total_value,
            'asset_count': len(crypto_assets),
            'networks_used': list(set(asset.get('network', 'unknown') for asset in crypto_assets)),
            'asset_types': list(set(asset.get('asset_type', 'unknown') for asset in crypto_assets)),
            'security_score': self._calculate_crypto_security_score(crypto_assets),
            'inheritance_readiness': self._assess_crypto_inheritance_readiness(crypto_assets)
        }
        
        return analysis
    
    def _calculate_crypto_security_score(self, crypto_assets: List[Dict[str, Any]]) -> int:
        """Calculate security score for crypto assets (0-100)"""
        if not crypto_assets:
            return 0
        
        score = 0
        total_assets = len(crypto_assets)
        
        for asset in crypto_assets:
            asset_score = 0
            
            # Has access instructions
            if asset.get('access_instructions'):
                asset_score += 25
            
            # Has private key location
            if asset.get('private_key_location'):
                asset_score += 25
            
            # Has seed phrase location
            if asset.get('seed_phrase_location'):
                asset_score += 25
            
            # Has beneficiary assigned
            if asset.get('primary_beneficiary_id'):
                asset_score += 25
            
            score += asset_score
        
        return score // total_assets if total_assets > 0 else 0
    
    def _assess_crypto_inheritance_readiness(self, crypto_assets: List[Dict[str, Any]]) -> str:
        """Assess how ready crypto assets are for inheritance"""
        security_score = self._calculate_crypto_security_score(crypto_assets)
        
        if security_score >= 80:
            return "Excellent - Well prepared for inheritance"
        elif security_score >= 60:
            return "Good - Minor improvements needed"
        elif security_score >= 40:
            return "Fair - Significant improvements required"
        else:
            return "Poor - Major security and inheritance planning needed"
    
    def _generate_crypto_strategies(self, crypto_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate cryptocurrency inheritance strategies"""
        strategies = [
            {
                'strategy': 'Multi-Signature Wallets',
                'description': 'Use multi-sig wallets requiring multiple signatures for transactions',
                'benefits': ['Enhanced security', 'Shared control', 'Inheritance automation'],
                'implementation': 'Set up 2-of-3 or 3-of-5 multi-signature wallet with beneficiaries'
            },
            {
                'strategy': 'Smart Contract Inheritance',
                'description': 'Deploy smart contracts that automatically transfer assets after inactivity',
                'benefits': ['Automated inheritance', 'No third-party required', 'Transparent process'],
                'implementation': 'Deploy dead-man switch smart contracts with beneficiary addresses'
            },
            {
                'strategy': 'Hardware Wallet Inheritance',
                'description': 'Secure hardware wallet storage with detailed recovery instructions',
                'benefits': ['Maximum security', 'Offline storage', 'Physical control'],
                'implementation': 'Store hardware wallets and recovery phrases in separate secure locations'
            }
        ]
        
        return strategies
    
    def _get_crypto_security_advice(self, crypto_data: Dict[str, Any]) -> List[str]:
        """Get security advice for cryptocurrency inheritance"""
        return [
            "Never store private keys or seed phrases digitally without encryption",
            "Use hardware wallets for large cryptocurrency holdings",
            "Create multiple copies of recovery information stored in different locations",
            "Consider using a cryptocurrency-aware estate planning attorney",
            "Regularly test recovery procedures with small amounts",
            "Keep detailed instructions for accessing each wallet type",
            "Consider using time-locked smart contracts for inheritance",
            "Educate beneficiaries about cryptocurrency basics and security"
        ]
    
    def _get_crypto_legal_advice(self, crypto_data: Dict[str, Any]) -> List[str]:
        """Get legal advice for cryptocurrency inheritance"""
        return [
            "Cryptocurrency inheritance laws vary significantly by jurisdiction",
            "Include specific cryptocurrency provisions in your will",
            "Consider the tax implications of cryptocurrency inheritance",
            "Ensure compliance with anti-money laundering (AML) regulations",
            "Document the source and acquisition of cryptocurrency holdings",
            "Consider establishing a cryptocurrency-specific trust",
            "Keep records of all cryptocurrency transactions for tax purposes",
            "Consult with attorneys experienced in digital asset law"
        ]
    
    def _suggest_smart_contracts(self, crypto_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest smart contract solutions for crypto inheritance"""
        return [
            {
                'contract_type': 'Dead Man Switch',
                'description': 'Automatically transfers assets if owner becomes inactive',
                'networks': ['Ethereum', 'Polygon', 'BSC'],
                'features': ['Configurable timeout period', 'Multiple beneficiaries', 'Emergency override']
            },
            {
                'contract_type': 'Multi-Signature Inheritance',
                'description': 'Requires multiple signatures to access inherited funds',
                'networks': ['Ethereum', 'Bitcoin', 'Polygon'],
                'features': ['Shared control', 'Dispute resolution', 'Gradual release']
            },
            {
                'contract_type': 'Time-Locked Inheritance',
                'description': 'Releases assets to beneficiaries at predetermined times',
                'networks': ['Ethereum', 'Polygon', 'Avalanche'],
                'features': ['Scheduled releases', 'Age-based unlocking', 'Educational milestones']
            }
        ]
    
    def _get_crypto_implementation_steps(self, crypto_data: Dict[str, Any]) -> List[str]:
        """Get implementation steps for crypto inheritance planning"""
        return [
            "1. Inventory all cryptocurrency holdings and access methods",
            "2. Create secure backup of all private keys and seed phrases",
            "3. Document detailed access instructions for each wallet",
            "4. Set up multi-signature wallets for large holdings",
            "5. Deploy smart contracts for automated inheritance",
            "6. Educate beneficiaries about cryptocurrency and security",
            "7. Create emergency access procedures for immediate family",
            "8. Regularly test and update inheritance procedures",
            "9. Consult with cryptocurrency-aware legal counsel",
            "10. Review and update crypto inheritance plan annually"
        ]
    
    def _generate_ai_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate AI response for estate planning questions"""
        # Simulate AI response based on common estate planning questions
        message_lower = user_message.lower()
        
        if 'will' in message_lower and ('create' in message_lower or 'make' in message_lower):
            return """
            Creating a will is one of the most important steps in estate planning. Here's what you need to consider:

            **Essential Elements:**
            1. **Personal Information** - Your full legal name and address
            2. **Executor** - Someone you trust to carry out your wishes
            3. **Beneficiaries** - Who will receive your assets
            4. **Asset Distribution** - How your property should be divided
            5. **Guardianship** - Care for minor children (if applicable)
            6. **Digital Assets** - Instructions for cryptocurrency and online accounts

            **Next Steps:**
            - Use our Will Creation Wizard to gather all necessary information
            - Review your asset inventory to ensure everything is included
            - Consider consulting with an estate planning attorney
            - Ensure proper execution with witnesses and notarization

            Would you like me to help you start the will creation process?
            """
        
        elif 'crypto' in message_lower or 'bitcoin' in message_lower or 'ethereum' in message_lower:
            return """
            Cryptocurrency inheritance requires special planning due to the unique nature of digital assets:

            **Key Considerations:**
            1. **Private Key Management** - Secure storage and access instructions
            2. **Multi-Signature Wallets** - Shared control with beneficiaries
            3. **Smart Contracts** - Automated inheritance mechanisms
            4. **Legal Compliance** - Tax implications and regulatory requirements

            **Recommended Approach:**
            - Document all cryptocurrency holdings and wallet addresses
            - Create detailed access instructions for each wallet type
            - Consider using hardware wallets for large holdings
            - Set up smart contracts for automated inheritance
            - Educate beneficiaries about cryptocurrency security

            **Security Best Practices:**
            - Never store private keys digitally without encryption
            - Use multiple secure locations for backup information
            - Regularly test recovery procedures
            - Keep detailed records for tax purposes

            Would you like specific guidance on securing your cryptocurrency for inheritance?
            """
        
        elif 'beneficiary' in message_lower or 'beneficiaries' in message_lower:
            return """
            Choosing and managing beneficiaries is crucial for effective estate planning:

            **Types of Beneficiaries:**
            1. **Primary** - First in line to receive assets
            2. **Contingent** - Backup if primary beneficiaries cannot inherit
            3. **Specific** - Designated for particular assets
            4. **Residuary** - Receives remaining assets after specific bequests

            **Important Considerations:**
            - **Minors** require guardian designation and trust structures
            - **Inheritance Percentages** should total 100%
            - **Contact Information** must be current and complete
            - **Relationship Documentation** helps prevent disputes

            **Best Practices:**
            - Name both primary and backup beneficiaries
            - Review and update beneficiary information regularly
            - Consider the tax implications for beneficiaries
            - Include specific instructions for digital assets
            - Plan for beneficiaries who predecease you

            **Special Situations:**
            - Charitable organizations as beneficiaries
            - International beneficiaries and tax implications
            - Beneficiaries with special needs requiring trusts

            Would you like help adding or updating your beneficiaries?
            """
        
        else:
            return """
            I'm here to help with your estate planning questions! I can provide guidance on:

            **Estate Planning Topics:**
            - Creating and updating wills
            - Managing beneficiaries and inheritance
            - Cryptocurrency and digital asset planning
            - Asset inventory and valuation
            - Tax optimization strategies
            - Trust structures and estate protection
            - Legal compliance requirements

            **How I Can Help:**
            - Analyze your current estate plan completeness
            - Provide personalized recommendations
            - Generate legal documents and forms
            - Offer cryptocurrency inheritance strategies
            - Answer specific estate planning questions

            Please feel free to ask about any specific aspect of estate planning, and I'll provide detailed, personalized guidance based on your situation.

            What would you like to know more about?
            """
    
    def _suggest_follow_up_actions(self, user_message: str, ai_response: str) -> List[str]:
        """Suggest follow-up actions based on conversation"""
        actions = []
        
        message_lower = user_message.lower()
        
        if 'will' in message_lower:
            actions.extend([
                "Start the Will Creation Wizard",
                "Review your asset inventory",
                "Add or update beneficiaries"
            ])
        
        if 'crypto' in message_lower:
            actions.extend([
                "Add cryptocurrency assets to your portfolio",
                "Set up wallet connect for asset tracking",
                "Review crypto inheritance strategies"
            ])
        
        if 'beneficiary' in message_lower:
            actions.extend([
                "Add new beneficiaries",
                "Update inheritance percentages",
                "Review guardian designations for minors"
            ])
        
        # Default actions if no specific topic detected
        if not actions:
            actions = [
                "Complete your estate planning assessment",
                "Review recommended next steps",
                "Schedule consultation with legal counsel"
            ]
        
        return actions[:3]  # Limit to 3 suggestions


# Utility functions for NLWeb integration
def format_currency(amount: float) -> str:
    """Format currency for display"""
    return f"${amount:,.2f}"

def format_crypto(amount: float, symbol: str) -> str:
    """Format cryptocurrency amount for display"""
    return f"{amount:,.6f} {symbol}"

def truncate_address(address: str, start: int = 6, end: int = 4) -> str:
    """Truncate blockchain address for display"""
    if len(address) <= start + end:
        return address
    return f"{address[:start]}...{address[-end:]}"

def validate_wallet_address(address: str, network: str = 'ethereum') -> bool:
    """Basic wallet address validation"""
    if network.lower() in ['ethereum', 'polygon', 'bsc', 'avalanche']:
        return address.startswith('0x') and len(address) == 42
    elif network.lower() == 'bitcoin':
        return len(address) >= 26 and len(address) <= 35
    return False

# Export the main class and utility functions
__all__ = [
    'NLWebEstateAssistant',
    'format_currency',
    'format_crypto', 
    'truncate_address',
    'validate_wallet_address'
]

