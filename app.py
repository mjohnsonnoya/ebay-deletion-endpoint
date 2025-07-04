from flask import Flask, request, jsonify
import hashlib
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration - Replace these with your actual values
VERIFICATION_TOKEN = "D6qSdGSjCmvYFzPbqeZdse7r8Z5uMVB4JBOsF0dBz2IaOe_aMW"
ENDPOINT_URL = "https://ebay-deletion-endpoint-n6ky.onrender.com"

# @app.route('/ebay-deletion-endpoint', methods=['GET', 'POST'])
# def ebay_deletion_endpoint():
#     logger.info(f"Incoming {request.method} to {request.url}")
#     """
#     Endpoint to handle eBay marketplace account deletion notifications
#     - GET: Handle challenge code validation
#     - POST: Handle actual deletion notifications
#     """
#     try:
#         if request.method == 'GET':
#             return handle_challenge_code()
#         elif request.method == 'POST':
#             return handle_deletion_notification()
#     except Exception as e:
#         logger.error(f"Error in endpoint: {str(e)}")
#         return jsonify({"error": "Internal server error"}), 500

@app.route('/ebay-deletion-endpoint')
def test():
    return jsonify({"ok": True})


def handle_challenge_code():
    """Handle the challenge code validation from eBay"""
    challenge_code = request.args.get('challenge_code')
    
    if not challenge_code:
        logger.warning("No challenge code provided")
        return jsonify({"error": "No challenge code provided"}), 400
    
    try:
        # Calculate the challenge response
        # Order is critical: challengeCode + verificationToken + endpoint
        hash_string = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        
        # Create SHA256 hash
        m = hashlib.sha256(hash_string.encode('utf-8'))
        challenge_response = m.hexdigest()
        
        logger.info(f"Challenge code received: {challenge_code}")
        logger.info(f"Hash string: {hash_string}")
        logger.info(f"Challenge response: {challenge_response}")
        
        # Return the response in the required JSON format
        response_data = {
            "challengeResponse": challenge_response
        }
        
        # Ensure proper JSON content type
        response = jsonify(response_data)
        response.headers['Content-Type'] = 'application/json'
        
        return response, 200
        
    except Exception as e:
        logger.error(f"Error generating challenge response: {str(e)}")
        return jsonify({"error": "Challenge response generation failed"}), 500


def validate_configuration():
    """Validate the endpoint configuration"""
    errors = []
    
    # Validate verification token
    if not VERIFICATION_TOKEN:
        errors.append("Verification token is required")
    elif len(VERIFICATION_TOKEN) < 32 or len(VERIFICATION_TOKEN) > 80:
        errors.append("Verification token must be 32-80 characters long")
    elif not all(c.isalnum() or c in '_-' for c in VERIFICATION_TOKEN):
        errors.append("Verification token can only contain alphanumeric characters, underscore, and hyphen")
    
    # Validate endpoint URL
    if not ENDPOINT_URL:
        errors.append("Endpoint URL is required")
    elif not ENDPOINT_URL.startswith('https://'):
        errors.append("Endpoint URL must use HTTPS protocol")
    
    if errors:
        for error in errors:
            logger.error(f"Configuration error: {error}")
        raise ValueError("Configuration validation failed: " + "; ".join(errors))
    
    logger.info("Configuration validation passed")

# Add this call at the start of your application
validate_configuration()


def handle_deletion_notification():
    """Handle actual account deletion notifications"""
    try:
        # Get the JSON data from the request
        notification_data = request.get_json()
        
        if not notification_data:
            logger.warning("No notification data received")
            return jsonify({"error": "No notification data"}), 400
        
        logger.info(f"Received deletion notification: {notification_data}")
        
        # TODO: Implement actual data deletion logic here
        # For now, just acknowledge the notification
        return jsonify({"message": "Notification processed"}), 200
        
    except Exception as e:
        logger.error(f"Error processing notification: {str(e)}")
        return jsonify({"error": "Processing error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

