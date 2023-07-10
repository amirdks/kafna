from django.conf import settings
from sms_ir import SmsIr


def send_otp_code(phone_number, otp_code):
    try:
        sms_ir = SmsIr(
            settings.SMS_IR_API_KEY,
            # linenumber,
        )
        res = sms_ir.send_verify_code(
            number=phone_number,
            template_id=305214,
            parameters=[
                {
                    "name": "CODE",
                    "value": str(otp_code),
                },
            ],
        )
        return True
    except Exception as e:
        print(e)
        return False
