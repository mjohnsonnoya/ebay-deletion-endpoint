import hashlib
import requests
import json

# Test configuration
VERIFICATION_TOKEN = "D6qSdGSjCmvYFzPbqeZdse7r8Z5uMVB4JBOsF0dBz2IaOe_aMW"
ENDPOINT_URL = "https://ebay-deletion-endpoint-n6ky.onrender.com/"
LOCAL_TEST_URL = "http://localhost:5001/ebay-deletion-endpoint"

def test_challenge_response():
    """Test the challenge response functionality"""
    # Simulate eBay's challenge
    test_challenge_code = "test_challenge_123"
    
    # Calculate expected response
    hash_string = test_challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
    expected_response = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    
    print(f"Test challenge code: {test_challenge_code}")
    print(f"Expected response: {expected_response}")
    
    # Make request to local endpoint
    response = requests.get(LOCAL_TEST_URL, params={'challenge_code': test_challenge_code})
    
    if response.status_code == 200:
        response_data = response.json()
        actual_response = response_data.get('challengeResponse')
        
        print(f"Actual response: {actual_response}")
        print(f"Match: {actual_response == expected_response}")
        
        if actual_response == expected_response:
            print("✅ Challenge response test PASSED")
        else:
            print("❌ Challenge response test FAILED")
    else:
        print(f"❌ Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == '__main__':
    test_challenge_response()
