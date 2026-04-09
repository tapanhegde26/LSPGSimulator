export function generateInsights(data: any) {
  if (!data) return [];

  const insights = [];

  if (data.system_efficiency > 0.7) {
    insights.push("⚡ System is highly efficient with minimal energy loss.");
  } else {
    insights.push("⚠️ Significant energy loss detected. Consider optimizing transmission.");
  }

  if (data.transmission_loss_percent > 30) {
    insights.push("📡 Transmission loss is high. Microwave may be more stable than laser.");
  }

  if (data.total_energy_generated_gw > 10000) {
    insights.push("🌕 Large ring size is producing massive energy output.");
  }

  if (data.energy_received_gw < data.total_energy_generated_gw * 0.5) {
    insights.push("🚨 Less than 50% energy is reaching Earth — major inefficiency.");
  }

  return insights;
}
