from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import re

# Configure the Gemini API key
genai.configure(api_key="AIzaSyAq-sTOlMKAPXqVsl2jWH5p8baTPsArKs4")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def clean_story_text(text):
    """
    Clean the story text by removing unwanted characters and formatting.
    """
    # Remove newlines (make it paragraph)
    text = text.replace("\n", " ")
    # Remove backslashes (just in case)
    text = text.replace("\\", "")
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    return text.strip()

def generate_story(child_prompt):
    """
    Generate a short friendly story for kids using Gemini AI in Tunisian Arabic.
    """
    
    prompt = f"""
إنت حكواتي محترف للأطفال، تحب تحكي قصص للصغار باللهجة التونسية الدارجة.

رجاءً حضّرلي قصة صغيرة للصغار مستوحاة من هالفكرة: "{child_prompt}".

القصة لازم تكون باللهجة التونسية بكلمات سهلة برشا يفهموها الصغار، طولها بين 5 و 10 جمل، تبدأ بمقدمة تشد الانتباه، فيها شخصيات تحكي بحوارات بسيطة ومضحكة، مليانة خيال وضحك وأصوات أطفال كيما واو ويييي وههههه وبرافو. وختمها يكون فرحان ومضحك أو فيه مغزى صغير.

جاوب مباشرة بالقصة باللهجة التونسية من غير مقدمات.
"""
    
    # Use Gemini model
    model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
    
    response = model.generate_content(prompt)
    story = response.text.strip()
    
    return story

@app.route('/generate-story', methods=['POST'])
def generate_story_endpoint():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Please provide a prompt in the request body'}), 400
            
        prompt = data['prompt']
        story = generate_story(prompt)
        
        # Clean the story to remove \n and unwanted characters
        clean_story = clean_story_text(story)
        
        return jsonify({
            'status': 'success',
            'story': clean_story
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
