import requests
import sys

def get_retail_intelligence(city):
    """
    Fetches real-time weather data for a city using a public API 
    and transforms it into actionable retail insights.
    """
    print(f"📡 Connecting to Live Market API for: {city}...")
    
    # Using Open-Meteo Public API (Geocoding + Weather) - No API Key Required!
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        # EDGE CASE/CHAOS HANDLING 1: API Slowness Safeguard (5-second timeout)
        geo_response = requests.get(geo_url, timeout=5)
        geo_response.raise_for_status() # CHAOS HANDLING 2: Handle API internal errors
        
        geo_data = geo_response.json()
        if not geo_data.get('results'):
            print(f"❌ Input Error: The city '{city}' could not be found. Please check your spelling.")
            return None
            
        location = geo_data['results'][0]
        lat, lon = location['latitude'], location['longitude']
        country = location.get('country', 'Unknown')
        
        # Fetch current weather for coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url, timeout=5)
        weather_response.raise_for_status()
        
        weather_data = weather_response.json()
        temp = weather_data['current_weather']['temperature']
        windspeed = weather_data['current_weather']['windspeed']
        
        # DATA TRANSFORMATION: Mapping raw environmental data to Retail Indicators
        print("🧹 Running Retail Intelligence Transformations...")
        foot_traffic_modifier = "NORMAL"
        logistics_risk = "LOW"
        
        if temp < 5 or temp > 37:
            foot_traffic_modifier = "⚠️ REDUCED (Extreme Weather Deterrent)"
            logistics_risk = "MODERATE (Thermal Storage Constraints)"
        elif 15 <= temp <= 26:
            foot_traffic_modifier = "🚀 OPTIMAL (High Foot Traffic & Impulse Buys Expected)"
            
        if windspeed > 25:
            logistics_risk = "⚠️ HIGH (Potential Last-Mile Delivery Delays)"

        return {
            "city": location['name'],
            "country": country,
            "temperature": f"{temp}°C",
            "windspeed": f"{windspeed} km/h",
            "foot_traffic": foot_traffic_modifier,
            "logistics_risk": logistics_risk
        }

    except requests.exceptions.Timeout:
        print("❌ Chaos Test Passed: The external API took too long to respond. Connection safely severed.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ API Connection Error: Failed to retrieve data from the public gateway. Details: {e}")
        sys.exit(1)

def main():
    print("\n==============================================")
    print("🚀 RETAIL INTELLIGENCE INTERACTIVE CONSOLE")
    print("==============================================")
    
    # CHAOS HANDLING 3: User Bad Input Check
    user_city = input("Enter target retail market city name: ").strip()
    
    if not user_city:
        print("❌ Input Error: Node query cannot be empty.")
        return
    if any(char.isdigit() for char in user_city):
        print("❌ Input Error: Numeric digits detected. Please enter a valid city string name (e.g., London).")
        return

    metrics = get_retail_intelligence(user_city)
    
    if metrics:
        print("\n==============================================")
        print(f"📊 LIVE METRICS REPORT: {metrics['city'].upper()} ({metrics['country'].upper()})")
        print("==============================================")
        print(f"• Current Temperature : {metrics['temperature']}")
        print(f"• Wind Speed Condition : {metrics['windspeed']}")
        print(f"• Predicted Footfall   : {metrics['foot_traffic']}")
        print(f"• Supply Chain Risk    : {metrics['logistics_risk']}")
        print("==============================================\n")

if __name__ == "__main__":
    main()
