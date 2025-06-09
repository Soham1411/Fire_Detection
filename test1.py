from ultralytics import YOLO
import RPi.GPIO as GPIO
import time
from twilio.rest import Client

# Twilio credentials (Replace these with your actual Twilio account SID, Auth Token, and phone numbers)
ACCOUNT_SID = 'your_account_sid'  # Twilio Account SID
AUTH_TOKEN = 'your_auth_token'    # Twilio Auth Token
# TWILIO_PHONE_NUMBER = 'Replace wiht your Twilio no.'
# TO_PHONE_NUMBER = 'Replace with your phone number' 

# GPIO setup for the passive buzzer
BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Set up PWM (Frequency 1000 Hz, duty cycle 50%)
pwm = GPIO.PWM(BUZZER_PIN, 1000)
pwm.start(50)  # Start with 50% duty cycle (can be adjusted)

# Initialize the YOLO model
model = YOLO('best.pt')  # Path to your trained model

# Initialize Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Function to activate the buzzer for a specified duration
def activate_buzzer(duration=20):
    pwm.ChangeDutyCycle(100)  # Set to 100% duty cycle for max volume
    time.sleep(duration)      # Keep the buzzer on for 'duration' seconds
    pwm.ChangeDutyCycle(0)    # Turn off the buzzer

# Function to send an SMS when fire is detected
def send_sms():
    message = client.messages.create(
        body="Fire detected! Please take immediate action.",
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print(f"Message sent: {message.sid}")

# Function to clean up GPIO pins
def cleanup():
    pwm.stop()                # Stop PWM signal
    GPIO.cleanup()             # Reset GPIO setup

# Main script
if __name__ == "__main__":
    try:
        # Run YOLO prediction on camera feed
        results_generator = model.predict(source=0, imgsz=640, conf=0.6, show=True)
        for results in results_generator:
            for detection in results.boxes:
                label = detection.cls  # Class label index
                conf = detection.conf  # Confidence score
                if label == 0 and conf > 0.6:
                    print("Fire detected!")
                    activate_buzzer(duration=20)
                    send_sms()

    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        cleanup()