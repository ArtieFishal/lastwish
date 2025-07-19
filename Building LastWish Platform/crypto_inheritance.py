"""
Crypto Inheritance Workflow API Routes for LastWish Estate Planning Platform
Handles blockchain-based inheritance planning, smart contracts, and automated transfers
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
from decimal import Decimal
import json
import uuid
from typing import Dict, List, Optional

from models.user import db, User
from models.crypto_assets import (
    CryptoWallet, CryptoAsset, CryptoInheritancePlan, CryptoBeneficiary,
    InheritanceStatus, BlockchainNetwork
)
from utils.blockchain_integration import (
    BlockchainManager, InheritanceSmartContract, CryptoTransferManager,
    CryptoComplianceChecker, generate_inheritance_report
)

crypto_inheritance_bp = Blueprint('crypto_inheritance', __name__, url_prefix='/api/crypto/inheritance')

# Initialize blockchain utilities
blockchain_manager = BlockchainManager()
smart_contract_manager = InheritanceSmartContract(blockchain_manager)
transfer_manager = CryptoTransferManager(blockchain_manager)
compliance_checker = CryptoComplianceChecker()

@crypto_inheritance_bp.route('/plans', methods=['POST'])
@jwt_required()
def create_inheritance_plan():
    """Create a new crypto inheritance plan with blockchain integration"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['wallet_id', 'plan_name', 'beneficiaries', 'trigger_conditions']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Verify wallet ownership
        wallet = CryptoWallet.query.filter_by(id=data['wallet_id'], user_id=user_id).first()
        if not wallet:
            return jsonify({'success': False, 'error': 'Wallet not found or access denied'}), 404
        
        # Validate beneficiaries
        beneficiaries = data['beneficiaries']
        total_allocation = sum(b.get('allocation_percentage', 0) for b in beneficiaries)
        if total_allocation != 100:
            return jsonify({'success': False, 'error': 'Total beneficiary allocation must equal 100%'}), 400
        
        # Create inheritance plan
        plan = CryptoInheritancePlan(
            user_id=user_id,
            wallet_id=data['wallet_id'],
            plan_name=data['plan_name'],
            plan_description=data.get('plan_description'),
            beneficiaries=beneficiaries,
            backup_beneficiaries=data.get('backup_beneficiaries', []),
            trigger_conditions=data['trigger_conditions'],
            time_delay=data.get('time_delay', 30),
            verification_requirements=data.get('verification_requirements', {}),
            automated_execution=data.get('automated_execution', False),
            manual_approval_required=data.get('manual_approval_required', True),
            multi_signature_required=data.get('multi_signature_required', False),
            access_instructions=data.get('access_instructions', ''),
            security_questions=data.get('security_questions', []),
            emergency_contacts=data.get('emergency_contacts', []),
            legal_documentation=data.get('legal_documentation', '')
        )
        
        # Handle smart contract deployment if enabled
        if data.get('smart_contract_enabled', False):
            try:
                network = data.get('smart_contract_network', 'ethereum')
                plan.smart_contract_network = BlockchainNetwork(network)
                
                # Simulate smart contract deployment
                deployment_result = smart_contract_manager.deploy_inheritance_contract(
                    network=network,
                    owner_private_key="simulated_key",  # In real implementation, use secure key management
                    beneficiaries=beneficiaries,
                    inactivity_period_days=data['trigger_conditions'].get('inactivity_period', 365),
                    time_delay_days=data.get('time_delay', 30)
                )
                
                if deployment_result:
                    plan.smart_contract_address = deployment_result['contract_address']
                    plan.smart_contract_deployment_data = deployment_result
                    current_app.logger.info(f"Smart contract deployed: {deployment_result['contract_address']}")
                else:
                    current_app.logger.warning("Smart contract deployment failed")
                    
            except ValueError as e:
                return jsonify({'success': False, 'error': f'Invalid smart contract network: {str(e)}'}), 400
        
        db.session.add(plan)
        db.session.commit()
        
        # Update wallet inheritance status
        wallet.inheritance_status = InheritanceStatus.CONFIGURED
        db.session.commit()
        
        # Generate compliance report
        compliance_report = compliance_checker.check_inheritance_compliance({
            'total_value_usd': float(wallet.estimated_total_value or 0),
            'beneficiaries': beneficiaries
        })
        
        response_data = {
            'success': True,
            'message': 'Inheritance plan created successfully',
            'plan_id': plan.id,
            'smart_contract_address': plan.smart_contract_address,
            'compliance_report': compliance_report
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating inheritance plan: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to create inheritance plan'}), 500

@crypto_inheritance_bp.route('/plans/<int:plan_id>/smart-contract/status', methods=['GET'])
@jwt_required()
def get_smart_contract_status(plan_id):
    """Get smart contract status for inheritance plan"""
    try:
        user_id = get_jwt_identity()
        plan = CryptoInheritancePlan.query.filter_by(id=plan_id, user_id=user_id).first()
        
        if not plan:
            return jsonify({'success': False, 'error': 'Inheritance plan not found'}), 404
        
        if not plan.smart_contract_address:
            return jsonify({'success': False, 'error': 'No smart contract deployed for this plan'}), 400
        
        # Get contract status
        contract_status = smart_contract_manager.check_contract_status(
            plan.smart_contract_address,
            plan.smart_contract_network.value
        )
        
        return jsonify({
            'success': True,
            'plan_id': plan_id,
            'contract_status': contract_status
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting smart contract status: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to get contract status'}), 500

@crypto_inheritance_bp.route('/plans/<int:plan_id>/transfer/prepare', methods=['POST'])
@jwt_required()
def prepare_inheritance_transfer(plan_id):
    """Prepare inheritance transfer for execution"""
    try:
        user_id = get_jwt_identity()
        plan = CryptoInheritancePlan.query.filter_by(id=plan_id, user_id=user_id).first()
        
        if not plan:
            return jsonify({'success': False, 'error': 'Inheritance plan not found'}), 404
        
        # Get associated wallet
        wallet = CryptoWallet.query.filter_by(id=plan.wallet_id).first()
        if not wallet:
            return jsonify({'success': False, 'error': 'Associated wallet not found'}), 404
        
        # Prepare transfer plan
        transfer_result = transfer_manager.prepare_inheritance_transfer(
            wallet_address=wallet.wallet_address,
            private_key_encrypted="encrypted_key_placeholder",  # In real implementation, use secure storage
            beneficiaries=plan.beneficiaries,
            network=wallet.blockchain_network.value
        )
        
        if not transfer_result['success']:
            return jsonify(transfer_result), 400
        
        # Store transfer plan for later execution
        plan.transfer_plan_data = transfer_result['transfer_plan']
        plan.plan_status = InheritanceStatus.READY_FOR_EXECUTION
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transfer plan prepared successfully',
            'transfer_plan': transfer_result['transfer_plan']
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error preparing inheritance transfer: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to prepare transfer'}), 500

@crypto_inheritance_bp.route('/plans/<int:plan_id>/transfer/execute', methods=['POST'])
@jwt_required()
def execute_inheritance_transfer(plan_id):
    """Execute inheritance transfer (requires additional authorization)"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        plan = CryptoInheritancePlan.query.filter_by(id=plan_id, user_id=user_id).first()
        
        if not plan:
            return jsonify({'success': False, 'error': 'Inheritance plan not found'}), 404
        
        if plan.plan_status != InheritanceStatus.READY_FOR_EXECUTION:
            return jsonify({'success': False, 'error': 'Plan not ready for execution'}), 400
        
        # Verify authorization (in real implementation, this would include multiple verification steps)
        authorization_code = data.get('authorization_code')
        if not authorization_code:
            return jsonify({'success': False, 'error': 'Authorization code required'}), 400
        
        # Execute transfer
        execution_result = transfer_manager.execute_inheritance_transfer(
            transfer_plan=plan.transfer_plan_data,
            private_key_encrypted="encrypted_key_placeholder",
            encryption_key="encryption_key_placeholder"
        )
        
        if not execution_result['success']:
            return jsonify(execution_result), 400
        
        # Update plan status
        plan.plan_status = InheritanceStatus.EXECUTED
        plan.execution_date = datetime.utcnow()
        plan.execution_data = execution_result['execution_summary']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Inheritance transfer executed successfully',
            'execution_summary': execution_result['execution_summary']
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error executing inheritance transfer: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to execute transfer'}), 500

@crypto_inheritance_bp.route('/plans/<int:plan_id>/compliance', methods=['GET'])
@jwt_required()
def get_compliance_report(plan_id):
    """Get compliance report for inheritance plan"""
    try:
        user_id = get_jwt_identity()
        plan = CryptoInheritancePlan.query.filter_by(id=plan_id, user_id=user_id).first()
        
        if not plan:
            return jsonify({'success': False, 'error': 'Inheritance plan not found'}), 404
        
        # Get associated wallet for value calculation
        wallet = CryptoWallet.query.filter_by(id=plan.wallet_id).first()
        
        # Generate compliance report
        compliance_report = compliance_checker.check_inheritance_compliance({
            'total_value_usd': float(wallet.estimated_total_value or 0) if wallet else 0,
            'beneficiaries': plan.beneficiaries
        }, jurisdiction=request.args.get('jurisdiction', 'US'))
        
        return jsonify({
            'success': True,
            'plan_id': plan_id,
            'compliance_report': compliance_report
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating compliance report: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to generate compliance report'}), 500

@crypto_inheritance_bp.route('/plans/<int:plan_id>/report', methods=['GET'])
@jwt_required()
def get_comprehensive_report(plan_id):
    """Get comprehensive inheritance plan report"""
    try:
        user_id = get_jwt_identity()
        plan = CryptoInheritancePlan.query.filter_by(id=plan_id, user_id=user_id).first()
        
        if not plan:
            return jsonify({'success': False, 'error': 'Inheritance plan not found'}), 404
        
        # Get associated wallet
        wallet = CryptoWallet.query.filter_by(id=plan.wallet_id).first()
        
        # Prepare plan data for report
        inheritance_plan_data = {
            'plan_name': plan.plan_name,
            'total_value_usd': float(wallet.estimated_total_value or 0) if wallet else 0,
            'beneficiaries': plan.beneficiaries,
            'smart_contract_enabled': bool(plan.smart_contract_address)
        }
        
        # Get blockchain status if smart contract exists
        blockchain_status = {}
        if plan.smart_contract_address:
            blockchain_status = smart_contract_manager.check_contract_status(
                plan.smart_contract_address,
                plan.smart_contract_network.value
            )
        
        # Get compliance report
        compliance_report = compliance_checker.check_inheritance_compliance(
            inheritance_plan_data,
            jurisdiction=request.args.get('jurisdiction', 'US')
        )
        
        # Generate comprehensive report
        comprehensive_report = generate_inheritance_report(
            inheritance_plan_data,
            blockchain_status,
            compliance_report
        )
        
        return jsonify({
            'success': True,
            'plan_id': plan_id,
            'comprehensive_report': comprehensive_report
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating comprehensive report: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to generate report'}), 500

@crypto_inheritance_bp.route('/wallet/<int:wallet_id>/balance', methods=['GET'])
@jwt_required()
def get_wallet_balance(wallet_id):
    """Get real-time wallet balance and asset information"""
    try:
        user_id = get_jwt_identity()
        wallet = CryptoWallet.query.filter_by(id=wallet_id, user_id=user_id).first()
        
        if not wallet:
            return jsonify({'success': False, 'error': 'Wallet not found'}), 404
        
        # Get wallet balance
        balance = blockchain_manager.get_wallet_balance(
            wallet.wallet_address,
            wallet.blockchain_network.value
        )
        
        # Get gas cost estimates
        gas_estimates = blockchain_manager.estimate_gas_cost(
            wallet.blockchain_network.value,
            'transfer'
        )
        
        # Get associated assets
        assets = CryptoAsset.query.filter_by(wallet_id=wallet_id).all()
        asset_data = []
        total_value = Decimal('0')
        
        for asset in assets:
            if asset.current_value_usd:
                total_value += asset.current_value_usd
                
            asset_info = {
                'id': asset.id,
                'asset_name': asset.asset_name,
                'asset_symbol': asset.asset_symbol,
                'quantity': float(asset.quantity),
                'current_value_usd': float(asset.current_value_usd or 0),
                'inheritance_percentage': float(asset.inheritance_percentage)
            }
            asset_data.append(asset_info)
        
        return jsonify({
            'success': True,
            'wallet_info': {
                'id': wallet.id,
                'wallet_name': wallet.wallet_name,
                'wallet_address': wallet.wallet_address,
                'network': wallet.blockchain_network.value,
                'native_balance': float(balance),
                'total_value_usd': float(total_value),
                'asset_count': len(asset_data),
                'assets': asset_data,
                'gas_estimates': gas_estimates,
                'last_updated': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting wallet balance: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to get wallet balance'}), 500

@crypto_inheritance_bp.route('/beneficiaries/<int:beneficiary_id>/verify', methods=['POST'])
@jwt_required()
def verify_beneficiary(beneficiary_id):
    """Verify beneficiary for crypto inheritance"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        beneficiary = CryptoBeneficiary.query.filter_by(id=beneficiary_id, user_id=user_id).first()
        
        if not beneficiary:
            return jsonify({'success': False, 'error': 'Beneficiary not found'}), 404
        
        # Verify wallet address if provided
        if beneficiary.crypto_wallet_address:
            is_valid = blockchain_manager.validate_wallet_address(
                beneficiary.crypto_wallet_address,
                beneficiary.preferred_blockchain.value if beneficiary.preferred_blockchain else 'ethereum'
            )
            
            if not is_valid:
                return jsonify({'success': False, 'error': 'Invalid wallet address'}), 400
        
        # Update verification status
        beneficiary.verification_status = 'verified'
        beneficiary.verification_date = datetime.utcnow()
        beneficiary.verification_data = {
            'verification_method': data.get('verification_method', 'manual'),
            'verified_by': user_id,
            'verification_notes': data.get('verification_notes', ''),
            'wallet_address_verified': bool(beneficiary.crypto_wallet_address)
        }
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Beneficiary verified successfully',
            'beneficiary_id': beneficiary_id,
            'verification_date': beneficiary.verification_date.isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error verifying beneficiary: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to verify beneficiary'}), 500

@crypto_inheritance_bp.route('/analytics/portfolio', methods=['GET'])
@jwt_required()
def get_portfolio_analytics():
    """Get comprehensive portfolio analytics for crypto inheritance planning"""
    try:
        user_id = get_jwt_identity()
        
        # Get all user's crypto assets and wallets
        wallets = CryptoWallet.query.filter_by(user_id=user_id, is_active=True).all()
        assets = CryptoAsset.query.filter_by(user_id=user_id).all()
        inheritance_plans = CryptoInheritancePlan.query.filter_by(user_id=user_id).all()
        
        # Calculate portfolio metrics
        total_portfolio_value = Decimal('0')
        inheritance_coverage = Decimal('0')
        network_distribution = {}
        asset_type_distribution = {}
        
        for asset in assets:
            if asset.current_value_usd:
                total_portfolio_value += asset.current_value_usd
                
                # Calculate inheritance coverage
                if asset.inheritance_percentage > 0:
                    inheritance_coverage += asset.current_value_usd * (asset.inheritance_percentage / 100)
                
                # Network distribution
                wallet = next((w for w in wallets if w.id == asset.wallet_id), None)
                if wallet:
                    network = wallet.blockchain_network.value
                    if network not in network_distribution:
                        network_distribution[network] = Decimal('0')
                    network_distribution[network] += asset.current_value_usd
                
                # Asset type distribution
                asset_type = asset.asset_type.value
                if asset_type not in asset_type_distribution:
                    asset_type_distribution[asset_type] = Decimal('0')
                asset_type_distribution[asset_type] += asset.current_value_usd
        
        # Calculate inheritance plan statistics
        plan_stats = {
            'total_plans': len(inheritance_plans),
            'active_plans': len([p for p in inheritance_plans if p.plan_status == InheritanceStatus.ACTIVE]),
            'configured_plans': len([p for p in inheritance_plans if p.plan_status == InheritanceStatus.CONFIGURED]),
            'smart_contract_plans': len([p for p in inheritance_plans if p.smart_contract_address])
        }
        
        # Calculate coverage percentage
        coverage_percentage = float((inheritance_coverage / total_portfolio_value * 100) if total_portfolio_value > 0 else 0)
        
        analytics = {
            'portfolio_summary': {
                'total_value_usd': float(total_portfolio_value),
                'total_wallets': len(wallets),
                'total_assets': len(assets),
                'inheritance_coverage_usd': float(inheritance_coverage),
                'inheritance_coverage_percentage': coverage_percentage
            },
            'network_distribution': {k: float(v) for k, v in network_distribution.items()},
            'asset_type_distribution': {k: float(v) for k, v in asset_type_distribution.items()},
            'inheritance_plan_stats': plan_stats,
            'risk_assessment': {
                'high_value_assets': len([a for a in assets if a.current_value_usd and a.current_value_usd > 10000]),
                'unprotected_assets': len([a for a in assets if a.inheritance_percentage == 0]),
                'single_point_of_failure': len(set(w.blockchain_network.value for w in wallets)) == 1
            },
            'recommendations': [
                'Diversify across multiple blockchain networks',
                'Ensure all high-value assets have inheritance plans',
                'Regular review and update of beneficiary information',
                'Consider smart contract automation for large estates'
            ],
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'analytics': analytics
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating portfolio analytics: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to generate analytics'}), 500

# Error Handlers

@crypto_inheritance_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'success': False, 'error': 'Bad request'}), 400

@crypto_inheritance_bp.errorhandler(401)
def unauthorized(error):
    return jsonify({'success': False, 'error': 'Unauthorized access'}), 401

@crypto_inheritance_bp.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@crypto_inheritance_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

