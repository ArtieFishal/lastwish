from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.notification import Notification
from src.models.user import User, db
from src.services.notification_service import notification_service
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

notification_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user notifications with pagination"""
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status')  # pending, sent, failed, read
        notification_type = request.args.get('type')  # email, sms, push
        
        # Build query
        query = Notification.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if notification_type:
            query = query.filter_by(type=notification_type)
        
        # Order by creation date (newest first)
        query = query.order_by(Notification.created_at.desc())
        
        # Paginate
        notifications = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'notifications': [notification.to_dict() for notification in notifications.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': notifications.total,
                'pages': notifications.pages,
                'has_next': notifications.has_next,
                'has_prev': notifications.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get notifications: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve notifications'
        }), 500

@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        user_id = get_jwt_identity()
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return jsonify({
                'success': False,
                'message': 'Notification not found'
            }), 404
        
        notification.mark_read()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Failed to mark notification as read: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update notification'
        }), 500

@notification_bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_all_notifications_read():
    """Mark all user notifications as read"""
    try:
        user_id = get_jwt_identity()
        
        # Update all unread notifications for the user
        updated_count = Notification.query.filter_by(
            user_id=user_id,
            read_at=None
        ).update({
            'read_at': datetime.utcnow()
        })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Marked {updated_count} notifications as read',
            'updated_count': updated_count
        })
        
    except Exception as e:
        logger.error(f"Failed to mark all notifications as read: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update notifications'
        }), 500

@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get count of unread notifications"""
    try:
        user_id = get_jwt_identity()
        
        unread_count = Notification.query.filter_by(
            user_id=user_id,
            read_at=None
        ).count()
        
        return jsonify({
            'success': True,
            'unread_count': unread_count
        })
        
    except Exception as e:
        logger.error(f"Failed to get unread count: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get unread count'
        }), 500

@notification_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    """Get user notification preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Get notification preferences from user metadata
        preferences = user.metadata.get('notification_preferences', {
            'email_notifications': True,
            'sms_notifications': False,
            'push_notifications': True,
            'marketing_emails': False,
            'security_alerts': True,
            'payment_confirmations': True,
            'document_updates': True,
            'post_demise_notifications': True
        })
        
        return jsonify({
            'success': True,
            'preferences': preferences
        })
        
    except Exception as e:
        logger.error(f"Failed to get notification preferences: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve preferences'
        }), 500

@notification_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_notification_preferences():
    """Update user notification preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        
        # Validate preferences
        valid_preferences = {
            'email_notifications',
            'sms_notifications', 
            'push_notifications',
            'marketing_emails',
            'security_alerts',
            'payment_confirmations',
            'document_updates',
            'post_demise_notifications'
        }
        
        preferences = {}
        for key, value in data.items():
            if key in valid_preferences and isinstance(value, bool):
                preferences[key] = value
        
        # Update user metadata
        if not user.metadata:
            user.metadata = {}
        
        user.metadata['notification_preferences'] = preferences
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notification preferences updated',
            'preferences': preferences
        })
        
    except Exception as e:
        logger.error(f"Failed to update notification preferences: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update preferences'
        }), 500

@notification_bp.route('/test', methods=['POST'])
@jwt_required()
def send_test_notification():
    """Send a test notification (for development/testing)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        notification_type = data.get('type', 'email')
        
        if notification_type == 'welcome':
            success = notification_service.send_welcome_notification(user_id)
        elif notification_type == 'payment_confirmation':
            test_payment_data = {
                'plan_name': 'Test Plan',
                'amount': '0.001',
                'currency': 'BTC',
                'tx_hash': '0x' + 'a' * 64
            }
            success = notification_service.send_payment_confirmation(user_id, test_payment_data)
        elif notification_type == 'document_ready':
            test_document_data = {
                'type': 'Test Addendum',
                'asset_count': 3,
                'download_url': 'https://lastwish.app/download/test'
            }
            success = notification_service.send_document_ready_notification(user_id, test_document_data)
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid notification type'
            }), 400
        
        return jsonify({
            'success': success,
            'message': 'Test notification sent' if success else 'Failed to send test notification'
        })
        
    except Exception as e:
        logger.error(f"Failed to send test notification: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to send test notification'
        }), 500

@notification_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_notification_stats():
    """Get notification statistics for the user"""
    try:
        user_id = get_jwt_identity()
        
        # Get notification counts by status
        stats = {
            'total': Notification.query.filter_by(user_id=user_id).count(),
            'pending': Notification.query.filter_by(user_id=user_id, status='pending').count(),
            'sent': Notification.query.filter_by(user_id=user_id, status='sent').count(),
            'failed': Notification.query.filter_by(user_id=user_id, status='failed').count(),
            'read': Notification.query.filter(
                Notification.user_id == user_id,
                Notification.read_at.isnot(None)
            ).count(),
            'unread': Notification.query.filter_by(
                user_id=user_id,
                read_at=None
            ).count()
        }
        
        # Get counts by type
        type_stats = {}
        for notification_type in ['email', 'sms', 'push']:
            type_stats[notification_type] = Notification.query.filter_by(
                user_id=user_id,
                type=notification_type
            ).count()
        
        # Get recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_count = Notification.query.filter(
            Notification.user_id == user_id,
            Notification.created_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'type_stats': type_stats,
            'recent_activity': {
                'last_30_days': recent_count
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get notification stats: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve statistics'
        }), 500

# Admin routes (for system management)
@notification_bp.route('/admin/process-scheduled', methods=['POST'])
def process_scheduled_notifications():
    """Process scheduled notifications (admin endpoint)"""
    try:
        # This would typically be called by a cron job or scheduler
        # Add authentication/authorization as needed
        
        processed_count = notification_service.process_scheduled_notifications()
        
        return jsonify({
            'success': True,
            'message': f'Processed {processed_count} scheduled notifications',
            'processed_count': processed_count
        })
        
    except Exception as e:
        logger.error(f"Failed to process scheduled notifications: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to process scheduled notifications'
        }), 500

@notification_bp.route('/admin/stats', methods=['GET'])
def get_system_notification_stats():
    """Get system-wide notification statistics (admin endpoint)"""
    try:
        # Add authentication/authorization as needed
        
        # Get overall system stats
        total_notifications = Notification.query.count()
        pending_notifications = Notification.query.filter_by(status='pending').count()
        failed_notifications = Notification.query.filter_by(status='failed').count()
        
        # Get stats for last 24 hours
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        recent_notifications = Notification.query.filter(
            Notification.created_at >= twenty_four_hours_ago
        ).count()
        
        # Get scheduled notifications
        scheduled_notifications = Notification.query.filter(
            Notification.status == 'pending',
            Notification.scheduled_for.isnot(None)
        ).count()
        
        return jsonify({
            'success': True,
            'system_stats': {
                'total_notifications': total_notifications,
                'pending_notifications': pending_notifications,
                'failed_notifications': failed_notifications,
                'recent_notifications': recent_notifications,
                'scheduled_notifications': scheduled_notifications
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get system notification stats: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve system statistics'
        }), 500

