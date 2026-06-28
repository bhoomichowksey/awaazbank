"""
AwaazBank — KYC Handler
Handles Aadhaar OTP verification and selfie liveness check.
"""

import boto3
import base64
import requests
import os

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
UIDAI_OTP_URL = "https://stage1.uidai.gov.in/uidVerifyService/vid/generateOtp"


def send_aadhaar_otp(aadhaar_number: str) -> dict:
    """
    Send OTP to mobile number linked to Aadhaar.
    Returns: { "success": bool, "txn_id": str }
    """
    payload = {
        "aadhaarNumber": aadhaar_number,
        "consent": "Y",
    }
    # TODO: Call UIDAI OTP API with registered credentials
    # response = requests.post(UIDAI_OTP_URL, json=payload)
    # return response.json()

    # Stub for demo
    return {"success": True, "txn_id": "TXN12345678"}


def verify_aadhaar_otp(txn_id: str, otp: str) -> dict:
    """
    Verify OTP entered by user.
    Returns: { "verified": bool, "name": str, "dob": str }
    """
    # TODO: Call UIDAI OTP verification API
    if len(otp) == 6 and otp.isdigit():
        return {
            "verified": True,
            "name": "Ramji Prasad",
            "dob": "1985-06-15",
        }
    return {"verified": False, "name": None, "dob": None}


def check_liveness(image_base64: str) -> dict:
    """
    Run selfie liveness detection using AWS Rekognition.
    Returns: { "is_live": bool, "confidence": float }
    """
    client = boto3.client("rekognition", region_name=AWS_REGION)

    image_bytes = base64.b64decode(image_base64)

    # TODO: Uncomment when AWS credentials are set
    # response = client.detect_faces(
    #     Image={"Bytes": image_bytes},
    #     Attributes=["ALL"]
    # )
    # faces = response.get("FaceDetails", [])
    # if not faces:
    #     return {"is_live": False, "confidence": 0.0}
    # confidence = faces[0].get("Confidence", 0.0)
    # return {"is_live": confidence > 90.0, "confidence": confidence}

    # Stub for demo
    return {"is_live": True, "confidence": 97.3}


def open_account(name: str, aadhaar: str, account_type: str = "savings") -> dict:
    """
    Open SBI account via Core Banking API.
    Returns: { "success": bool, "account_number": str, "ifsc": str }
    """
    # TODO: Integrate with SBI Core Banking System API
    import random
    account_number = f"SBI{random.randint(10000000, 99999999)}"
    return {
        "success": True,
        "account_number": account_number,
        "ifsc": "SBIN0001234",
    }


if __name__ == "__main__":
    # Quick test
    otp_result = send_aadhaar_otp("XXXX-XXXX-1234")
    print("OTP sent:", otp_result)

    verify_result = verify_aadhaar_otp("TXN12345678", "123456")
    print("OTP verified:", verify_result)

    liveness_result = check_liveness(base64.b64encode(b"[fake image]").decode())
    print("Liveness:", liveness_result)

    account = open_account("Ramji Prasad", "XXXX-XXXX-1234", "savings")
    print("Account opened:", account)
