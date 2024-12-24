from common.config.config import ENTITY_VERSION
from common.service.service import EntityServiceImpl

service = EntityServiceImpl()


def perform_analysis(meta, data):
    # Assuming 'data' contains the household energy consumption details
    # Process the data to analyze energy consumption
    analysis_results = {}
    main_consumers = {}
    high_usage_periods = []
    outliers = []

    # Logic to analyze data (this is a placeholder example)
    total_consumption = 0
    for entry in data['household_energy_consumption']:
        time = entry['fecha_hora']
        consumption = entry['energia_activa_entrante_kWh']
        total_consumption += consumption

        # Identify main consumers and usage patterns
        if consumption > 0.1:  # Example threshold
            main_consumers[time] = consumption

        # Example logic for outlier detection
        if consumption < 0.05:
            outliers.append({
                "date_time": time,
                "consumption_kWh": consumption,
                "note": "Low usage detected, possible appliance left on."
            })

    # Calculate average or peak usage periods (this is just an example)
    high_usage_periods.append({
        "time_frame": "00:00 - 01:00",
        "average_consumption_kWh": total_consumption / len(data['household_energy_consumption'])  # Placeholder
    })

    # Prepare results
    analysis_results['main_consumers'] = main_consumers
    analysis_results['high_usage_periods'] = high_usage_periods
    analysis_results['outliers'] = outliers

    # Save the energy_analysis_report entity with the analysis results
    save_energy_analysis_report(meta, analysis_results)


def save_energy_analysis_report(meta, analysis_results):
    # Logic to save the energy_analysis_report entity
    # Example structure for saving
    energy_analysis_report = {"energy_analysis_report": {
        "main_consumers": analysis_results['main_consumers'],
        "usage_patterns": {
            "high_usage_periods": analysis_results['high_usage_periods'],
            "outliers": analysis_results['outliers']
        },
        "recommendations": [
            "Consider scheduling high-consumption appliances during off-peak hours.",
            "Regularly check and maintain appliances for optimal efficiency."
        ]
    }
    }
    service.add_item(meta['token'], 'energy_analysis_report', ENTITY_VERSION, energy_analysis_report)
    print("Energy analysis report saved:", energy_analysis_report)