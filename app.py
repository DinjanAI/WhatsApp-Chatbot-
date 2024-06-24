from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

whatsapp_token = os.environ.get("WHATSAPP_TOKEN")
verify_token = os.environ.get("VERIFY_TOKEN")

message_log_dict = {}

# Define services for machine learning and deep learning
machine_learning_services = [
    {"id": "1", "title": "Object Detection 📷"},
    {"id": "2", "title": "Object Classification🖼️"},
    {"id": "3", "title": "Object Recognition 🔍"},
    {"id": "4", "title": "Image Segmentation 🖼️🧩"},
    {"id": "5", "title": "Pose estimation 🕺"},
    {"id": "6", "title": "Video Object Tracking 🎥"},
    {"id": "7", "title": "Emotion recognition 😊"},
]

deep_learning_services = [
    {"id": "8", "title": "Neural Networks⚡"},
    {"id": "9", "title": "CNN 🔍📦"},
    {"id": "10", "title": "RNN 📥"},
    {"id": "11", "title": "GAN 🕵️"},
    {"id": "12", "title": "Autoencoders🗜️"},
    {"id": "13", "title" : "Healthcare 🏥🧬"}
]
genAI_services = [
    {"id" : "14", "title": "Image/Video Generation🎬"},
    {"id" : "15", "title": "Face Swapping👦↔️👧"},
    {"id" : "16", "title": "LLM🧠🤖"},
    {"id" : "17", "title": "Text Generation ✍️ "},
    {"id" : "18", "title": "Create Chatbot🌐🤖"}
]
    # Define responses for each service
service_responses = {
    "1": "Specializing in object detection 📸, we develop advanced algorithms for precise identification and localization of objects in images and videos 🕵️‍♂️.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "2": "Focused on Object Classification 🎯, we specialize in developing algorithms that accurately categorize objects within images and videos 🖼️🔍.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "3": "Specializing in Object Recognition 🌟, we develop cutting-edge algorithms to accurately identify and categorize objects in various environments 📸.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "4": "We specialize in image segmentation 📸✂️, creating advanced algorithms to accurately partition images into meaningful segments.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "5": "Specializing in pose estimation 🕺, we develop advanced algorithms to accurately track and analyze human body positions in images and videos 🎥.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "6": "We specialize in Video Object Tracking 🎥🔍, creating advanced algorithms to accurately track objects in real-time.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "7": "Specializing in emotion recognition 😊, we develop advanced AI algorithms to accurately identify and analyze human emotions from facial expressions and voice tones.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "8": "Specializing in Neural Networks 🧠, we develop advanced algorithms to enhance AI capabilities across industries, driving innovation and progress.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "9": "We specialize in CNN 🧠 technology for advanced image recognition and object detection 📸, pushing AI and computer vision boundaries 🌐👁️.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "10": "Focused on RNNs 🧠, we specialize in advanced algorithms for sequential data analysis, enhancing applications in NLP 📝, time series prediction ⏰, and beyond.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "11": "Specializing in GAN (Generative Adversarial Network) technology 🖼️, we innovate AI algorithms for creating realistic simulations and generating novel content across industries.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "12": "We specialize in Autoencoders 🤖 for data compression and reconstruction, enhancing applications in anomaly detection and image processing 📊🖼️.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "13": "In healthcare 🏥, we innovate with AI-driven solutions 🤖🔬 for medical imaging, patient monitoring 📊, and clinical decision support 📈, enhancing care quality and efficiency.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "14": "We specialize in image and video generation 📸🎥, leveraging advanced AI to create high-quality, realistic visuals 🤖✨ for various applications, driving innovation and creativity 🚀.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "15": "In face swapping 🎭, we specialize in developing advanced algorithms that seamlessly exchange facial features between individuals in images and videos. Our technology enhances creativity and entertainment 🎨📹, pushing the boundaries of visual storytelling and digital content creation.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "16": "In LLM (Legal Lifecycle Management) ⚖️, we optimize legal operations with solutions for contract management 📑, compliance monitoring 📅, and legal analytics 📊, enhancing organizational efficiency.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "17": "In text generation 📝, we develop AI-powered solutions for automated content creation 🖋️, enhancing communication and efficiency across industries.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
    "18": "Specializing in chatbot development 🤖, we create AI-powered conversational agents that enhance customer engagement and streamline business operations. Our solutions leverage natural language processing 🗣️ and machine learning 🧠 to deliver personalized user experiences across various platforms.\nFor more details, contact us at\nPhone:+91 98980459400\nEmail: shikha@dinjaninfotech.com",
}



def send_whatsapp_message(phone_number_id, to, message, buttons=None, list_message=False, services=None):
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
    }
    url = f"https://graph.facebook.com/v15.0/{phone_number_id}/messages"
    if list_message and services:
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": message},
                "action": {
                    "button": "Our Services",
                    "sections": [
                        {
                            "title": "Services",
                            "rows": services
                        }
                    ]
                }
            }
        }
    else:
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": message},
                "action": {"buttons": buttons}
            }
        }
    response = requests.post(url, json=data, headers=headers)
    print(f"WhatsApp response: {response.json()}")
    response.raise_for_status()

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return verify(request)
    elif request.method == "POST":
        return handle_message(request)

@app.route("/reset", methods=["GET"])
def reset():
    global message_log_dict
    message_log_dict = {}
    return "Message log resetted!"

def handle_message(request):
    body = request.get_json()
    print(f"request body: {body}")
    try:
        value = body["entry"][0]["changes"][0]["value"]
        phone_number_id = value["metadata"]["phone_number_id"]
        from_number = value["messages"][0]["from"]
        message = value["messages"][0]

        if message["type"] == "text":
            buttons = [
                {"type": "reply", "reply": {"id": "option_1", "title": "Machine Learning"}},
                {"type": "reply", "reply": {"id": "option_2", "title": "Deep Learning"}},
                {"type": "reply", "reply": {"id": "option_3", "title": "GenAI 🤖"}}
            ]
            send_whatsapp_message(phone_number_id, from_number, "Choose an option:", buttons)

        elif message["type"] == "interactive":
            if message["interactive"]["type"] == "button_reply":
                button_reply_id = message["interactive"]["button_reply"]["id"]
                if button_reply_id == "option_1":
                    send_whatsapp_message(phone_number_id, from_number, "We have these services available for machine learning.", list_message=True, services=machine_learning_services)
                elif button_reply_id == "option_2":
                    send_whatsapp_message(phone_number_id, from_number, "We have these services available for Deep learning.", list_message=True, services=deep_learning_services)
                elif button_reply_id == "option_3":
                    send_whatsapp_message(phone_number_id, from_number, "We have these services available for genAI 🤖.", list_message=True, services=genAI_services)

                elif button_reply_id == "home":
                    buttons = [
                        {"type": "reply", "reply": {"id": "option_1", "title": "Machine Learning"}},
                        {"type": "reply", "reply": {"id": "option_2", "title": "Deep Learning"}},
                        {"type": "reply", "reply": {"id": "option_3", "title": "GenAI 🤖"}}
                    ]
                    send_whatsapp_message(phone_number_id, from_number, "Welcome back to the home screen. Choose an option:", buttons)

            elif message["interactive"]["type"] == "list_reply":
                list_reply_id = message["interactive"]["list_reply"]["id"]
                response_message = service_responses.get(list_reply_id, "")
                send_whatsapp_message(phone_number_id, from_number, response_message, buttons=[
                    {"type": "reply", "reply": {"id": "home", "title": "Home"}}
                ])
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"unknown error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def verify(request):
    if request.args.get("hub.verify_token") == verify_token:
        return request.args.get("hub.challenge")
    return "Verification token mismatch", 403

if __name__ == "__main__":
    app.run(port=8000)



