from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load dataset
df = pd.read_csv('crops.csv')

# Crop name to image mapping
crop_images = {
    'banana': 'https://media.istockphoto.com/id/1008848042/photo/banana-plantation.jpg?s=612x612&w=0&k=20&c=LFsEaRVEF3tBurWYnBX0hyzcp6eYtbb36USQ7IOhzxs=',
    'maize': 'https://cdn.britannica.com/36/167236-050-BF90337E/Ears-corn.jpg',
    'rice': 'https://cdn.britannica.com/89/140889-050-EC3F00BF/Ripening-heads-rice-Oryza-sativa.jpg',
    'apple': 'https://www.shutterstock.com/image-photo/autumn-day-rural-garden-frame-600nw-1798373137.jpg',
    'mango': 'https://images-cdn.ubuy.co.in/63751d7dcd47055dee73e183-mango-tree-choc-anon-miracle-mango.jpg',
    'watermelon': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8csV_EW8K6S7dMxAAZwCtF83qQbPQr9UgMQ&s',
    'grapes': 'https://www.apnikheti.com/upload/crops/1850idea99grapes.jpg',
    'papaya': 'https://plantix.net/en/library/assets/custom/crop-images/papaya.jpeg',
    'cotton': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDhnhqJIj85bgubo4cJR9FeewK6k5WEGyVJg&s',
    'coffee': 'https://rukminim2.flixcart.com/image/704/844/xif0q/shopsy-plant-sapling/h/p/t/perennial-no-yes-coffee-tree-plant-1-punarva-original-imahyxrc44rvpghk.jpeg?q=90&crop=false',
    'coconut': 'https://img-cdn.krishijagran.com/61498/coconut-farm.jpg',
    'orange': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYpKd8dTisxFjbJEfAU_Rmbdp7ZRnlFlSZ9g&s',
    'chickpea':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZbM06fj87wQAq-DO05EdnNs6enYJDQ5VKuw&s'
}

@app.route('/')
def home():
    return "✅ Crop Recommendation System is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        features = {
            'N': float(data['N']),
            'P': float(data['P']),
            'K': float(data['K']),
            'temperature': float(data['temperature']),
            'humidity': float(data['humidity']),
            'ph': float(data['ph']),
            'rainfall': float(data['rainfall']),
        }

        df['score'] = (
            abs(df['N'] - features['N']) +
            abs(df['P'] - features['P']) +
            abs(df['K'] - features['K']) +
            abs(df['temperature'] - features['temperature']) +
            abs(df['humidity'] - features['humidity']) +
            abs(df['ph'] - features['ph']) * 5 +
            abs(df['rainfall'] - features['rainfall']) / 2
        )

        top_crops = df.sort_values(by='score').head(3)['crop'].unique()

        recommendations = []
        for crop in top_crops:
            recommendations.append({
                'crop': crop,
                'image': crop_images.get(crop, 'https://via.placeholder.com/200x150?text=No+Image')
            })

        if not recommendations:
            return jsonify({'error': 'No matching crops found.'}), 404

        return jsonify({'recommendations': recommendations})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        print(f"\n📩 New Contact Message Received:")
        print(f"Name: {data.get('name')}")
        print(f"Email: {data.get('email')}")
        print(f"Message: {data.get('message')}")

        return jsonify({'status': 'Message received successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=10000)
    app.run(host='0.0.0.0', port=port, debug=True)

