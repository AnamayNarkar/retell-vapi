from flask import Flask, request, jsonify

app = Flask(__name__)

# Existing class definitions
class RetellResponseEngine:
    def __init__(self, llm_type, llm_id, version):
        self.llm_type = llm_type
        self.llm_id = llm_id
        self.version = version

class RetellApiBody:
    def __init__(
        self,
        response_engine=None,
        voice_id="11labs-Adrian",
        voicemail_message="Hello, this is a voicemail message.",
        voice_speed=1.0,
        volume=1.0
    ):
        if response_engine is None:
            response_engine = RetellResponseEngine(
                llm_type="retell-llm",
                llm_id="llm_234sdertfsdsfsdf",
                version=0
            )
        self.response_engine = response_engine
        self.voice_id = voice_id
        self.voicemail_message = voicemail_message
        self.voice_speed = voice_speed
        self.volume = volume

class VapiModel:
    def __init__(self, model="claude-3-7-sonnet-20250219", 
                 emotionalRecognitionEnabled=True, temperature=0.0):
        self.model = model
        self.emotionalRecognitionEnabled = emotionalRecognitionEnabled
        self.temperature = temperature

class VapiVoice:
    def __init__(self, provider="11labs", voice_id="andrea", speed=1.0):
        self.provider = provider
        self.voice_id = voice_id
        self.speed = speed

class VapiApiBody:
    def __init__(self, model=None, voice=None, 
                 voicemail_message="Hello, this is a voicemail message."):
        if model is None:
            model = VapiModel()
        if voice is None:
            voice = VapiVoice()
        self.model = model
        self.voice = voice
        self.voicemailMessage = voicemail_message

# Helper function to convert objects to dictionaries
def obj_to_dict(obj):
    if hasattr(obj, '__dict__'):
        return {key: obj_to_dict(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [obj_to_dict(item) for item in obj]
    else:
        return obj

@app.route('/create_agent', methods=['POST'])
def create_agent():
    try:
        data = request.get_json()
        api_type = data.get('apiType', 'retell').lower()
        
        # Validate input parameters
        if api_type not in ['retell', 'vapi']:
            raise ValueError("Invalid apiType. Use 'retell' or 'vapi'")
        
        voicemail_message = data.get('voicemailMessage', 
                                    'Hello, this is a voicemail message.')
        voice_speed = float(data.get('voiceSpeed', 1.0))
        volume = float(data.get('volume', 1.0)) if api_type == 'retell' else None

        # Parameter validation
        if not 0.5 <= voice_speed <= 2.0:
            raise ValueError("voiceSpeed must be between 0.5 and 2.0")
            
        if volume and not 0.5 <= volume <= 2.0:
            raise ValueError("volume must be between 0.5 and 2.0")

        # Create appropriate API body
        if api_type == 'retell':
            response_engine = RetellResponseEngine(
                llm_type="retell-llm",
                llm_id="llm_234sdertfsdsfsdf",
                version=0
            )
            api_body = RetellApiBody(
                response_engine=response_engine,
                voicemail_message=voicemail_message,
                voice_speed=voice_speed,
                volume=volume
            )
        else:
            voice = VapiVoice(speed=voice_speed)
            model = VapiModel()
            api_body = VapiApiBody(
                model=model,
                voice=voice,
                voicemail_message=voicemail_message
            )

        return jsonify({
            "status": "success",
            "provider": api_type,
            "configuration": obj_to_dict(api_body)
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)