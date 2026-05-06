def generate_insights(request, response):
    insights = []

    # Efficiency insight
    if request.panel_efficiency < 0.3:
        insights.append(
            "⚠️ Panel efficiency is low. Increasing efficiency can significantly boost energy output."
        )

    # Ring width insight
    if request.ring_width_km < 100:
        insights.append(
            "📈 Increasing ring width can improve total energy generation."
        )

    # Transmission insight
    if request.transmission_type == "laser":
        insights.append(
            "🔥 Laser transmission has higher losses compared to microwave."
        )

    # Ground stations
    if request.num_ground_stations < 5:
        insights.append(
            "🌍 Increasing ground stations improves energy distribution."
        )

    # Efficiency score
    if response["system_efficiency"] > 0.8:
        insights.append(
            "✅ System is highly efficient. Great configuration!"
        )

    return insights